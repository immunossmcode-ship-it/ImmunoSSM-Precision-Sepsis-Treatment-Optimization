import torch
from src.immunossm.hippo import hippo_legs_matrix

def test_hippo_matrix_shape_and_finite():
    matrix = hippo_legs_matrix(5)
    assert matrix.shape == (5, 5)
    assert torch.isfinite(matrix).all()
