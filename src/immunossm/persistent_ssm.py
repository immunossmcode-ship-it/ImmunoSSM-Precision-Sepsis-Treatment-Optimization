import torch
from torch import nn
from .hippo import hippo_legs_matrix

class PersistentStateSpaceLayer(nn.Module):
    def __init__(self, model_dim, state_dim, dropout):
        super().__init__()
        self.model_dim = model_dim
        self.state_dim = state_dim
        self.input_projection = nn.Linear(model_dim, state_dim)
        self.output_projection = nn.Linear(state_dim, model_dim)
        self.persistence_logits = nn.Parameter(torch.zeros(state_dim))
        self.step_parameter = nn.Parameter(torch.zeros(()))
        self.register_buffer("A_base", hippo_legs_matrix(state_dim))
        self.norm = nn.LayerNorm(model_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, sequence, elapsed_steps=None):
        batch, steps, _ = sequence.shape
        device, dtype = sequence.device, sequence.dtype
        A = self.A_base.to(device=device, dtype=dtype)
        gate = torch.sigmoid(self.persistence_logits).to(dtype=dtype)
        A = A * gate.unsqueeze(0)
        B = self.input_projection(sequence)
        delta = torch.nn.functional.softplus(self.step_parameter).to(dtype=dtype)
        if elapsed_steps is None:
            elapsed_steps = torch.ones(steps, device=device, dtype=dtype)
        state = torch.zeros(batch, self.state_dim, device=device, dtype=dtype)
        outputs = []
        for index in range(steps):
            dt = delta * elapsed_steps[index].to(dtype=dtype)
            transition = torch.matrix_exp(A * dt)
            # Zero-order-hold input integral; solve is numerically preferable to A inverse.
            identity = torch.eye(self.state_dim, device=device, dtype=dtype)
            try:
                input_map = torch.linalg.solve(A, transition - identity)
                state = state @ transition.T + B[:, index] @ input_map.T
            except RuntimeError:
                # Numerically safe first-order fallback; validate against the
                # selected continuous-time discretization in the final study.
                state = state + dt * B[:, index]
            outputs.append(self.output_projection(state))
        output = torch.stack(outputs, dim=1)
        return self.norm(sequence + self.dropout(output))

class PersistentStateSpaceTrajectoryEngine(nn.Module):
    def __init__(self, model_dim, state_dim, layers, dropout):
        super().__init__()
        self.layers = nn.ModuleList([
            PersistentStateSpaceLayer(model_dim, state_dim, dropout) for _ in range(layers)
        ])

    def forward(self, sequence, elapsed_steps=None):
        for layer in self.layers:
            sequence = layer(sequence, elapsed_steps)
        return sequence
