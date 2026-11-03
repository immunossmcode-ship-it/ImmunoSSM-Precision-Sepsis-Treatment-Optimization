import torch
from torch import nn

class VitalSignEncoder(nn.Module):
    """Causal temporal convolutional encoder for vital-sign trajectories."""
    def __init__(self, input_dim, embedding_dim, dropout, dilation_rates, kernel_size):
        super().__init__()
        layers = []
        channels = input_dim
        for dilation in dilation_rates:
            padding = (kernel_size - 1) * dilation
            layers.extend([
                nn.Conv1d(channels, embedding_dim, kernel_size=kernel_size,
                          padding=padding, dilation=dilation),
                nn.GELU(),
                nn.Dropout(dropout),
            ])
            channels = embedding_dim
        self.network = nn.Sequential(*layers)
        self.dilations = tuple(dilation_rates)
        self.kernel_size = kernel_size

    def forward(self, x):
        # x: batch x time x channels; right-padding is cropped to preserve causality.
        y = self.network(x.transpose(1, 2))
        return y[..., :x.shape[1]].transpose(1, 2)
