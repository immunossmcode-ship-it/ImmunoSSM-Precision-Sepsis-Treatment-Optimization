import torch
from src.immunossm.pton import PrecisionTreatmentOptimizationNetwork

def test_policy_output_contract():
    model = PrecisionTreatmentOptimizationNetwork(state_dim=6, action_cardinalities=[3, 4], hidden_dim=8)
    state = torch.randn(2, 6)
    distributions, value = model(state)
    assert len(distributions) == 2
    assert value.shape[0] == 2
