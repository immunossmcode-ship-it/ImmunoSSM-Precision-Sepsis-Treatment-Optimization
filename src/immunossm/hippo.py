import torch

def hippo_legs_matrix(state_dim, device=None, dtype=None):
    """Construct a continuous-time HiPPO-LegS transition matrix.

    The state dimension is supplied by the external model configuration.
    Verify the matrix convention against the manuscript's displayed equation
    and the intended HiPPO-LegS reference implementation before experiments.
    """
    n = torch.arange(state_dim, device=device, dtype=dtype)
    row, col = n[:, None], n[None, :]
    matrix = torch.zeros((state_dim, state_dim), device=device, dtype=dtype)
    mask = row > col
    matrix[mask] = -torch.sqrt(2 * row[mask] + 1) * torch.sqrt(2 * col[mask] + 1)
    diagonal = -(n + 1)
    indices = torch.arange(state_dim, device=device)
    matrix[indices, indices] = diagonal
    return matrix
