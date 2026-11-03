import torch
import torch.nn.functional as F

def weighted_binary_classification_loss(logits, targets, weights=None):
    loss = F.binary_cross_entropy_with_logits(logits, targets.float(), reduction="none")
    if weights is not None:
        loss = loss * weights
    return loss.mean()

def weighted_trajectory_loss(prediction, target, channel_weights=None, observation_mask=None):
    error = (prediction - target).abs()
    if channel_weights is not None:
        error = error * channel_weights
    if observation_mask is not None:
        error = error * observation_mask
        denominator = observation_mask.sum().clamp_min(1)
        return error.sum() / denominator
    return error.mean()

def propensity_loss(logits, treatment):
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), treatment.reshape(-1).long())

def combine_objectives(losses, configured_weights):
    if set(losses) != set(configured_weights):
        raise ValueError("Every task loss must have a corresponding configured weight.")
    return sum(losses[name] * configured_weights[name] for name in losses)
