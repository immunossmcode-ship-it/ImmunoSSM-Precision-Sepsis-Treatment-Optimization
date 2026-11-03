"""Conditional affine autoregressive flow building block for trajectory synthesis."""
import torch
from torch import nn

class ConditionalAffineCoupling(nn.Module):
    def __init__(self, feature_dim, condition_dim, hidden_dim, mask):
        super().__init__()
        self.register_buffer("mask", mask)
        self.network = nn.Sequential(
            nn.Linear(feature_dim + condition_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, feature_dim * 2)
        )

    def forward(self, x, condition):
        masked = x * self.mask
        shift, log_scale = self.network(torch.cat([masked, condition], dim=-1)).chunk(2, dim=-1)
        active = 1 - self.mask
        log_scale = torch.tanh(log_scale) * active
        transformed = masked + active * (x * torch.exp(log_scale) + shift)
        log_det = log_scale.sum(dim=-1)
        return transformed, log_det

    def inverse(self, z, condition):
        masked = z * self.mask
        shift, log_scale = self.network(torch.cat([masked, condition], dim=-1)).chunk(2, dim=-1)
        active = 1 - self.mask
        log_scale = torch.tanh(log_scale) * active
        recovered = masked + active * ((z - shift) * torch.exp(-log_scale))
        return recovered, -log_scale.sum(dim=-1)

class CounterfactualTrajectorySynthesizer(nn.Module):
    def __init__(self, feature_dim, condition_dim, hidden_dim, masks):
        super().__init__()
        self.layers = nn.ModuleList([
            ConditionalAffineCoupling(feature_dim, condition_dim, hidden_dim, mask)
            for mask in masks
        ])

    def forward(self, noise, condition):
        value, total_log_det = noise, noise.new_zeros(noise.shape[:-1])
        for layer in self.layers:
            value, log_det = layer(value, condition)
            total_log_det = total_log_det + log_det
        return value, total_log_det

    def sample(self, noise, condition):
        return self.forward(noise, condition)[0]
