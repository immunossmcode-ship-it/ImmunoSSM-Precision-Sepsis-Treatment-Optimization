import torch
from torch import nn
from torch.distributions import Categorical, kl_divergence

class PrecisionTreatmentOptimizationNetwork(nn.Module):
    """Categorical logged-action policy with behavior cloning and KL control."""
    def __init__(self, state_dim, action_cardinalities, hidden_dim):
        super().__init__()
        self.action_cardinalities = list(action_cardinalities)
        self.trunk = nn.Sequential(nn.Linear(state_dim, hidden_dim), nn.GELU())
        self.policy_heads = nn.ModuleList([nn.Linear(hidden_dim, n) for n in self.action_cardinalities])
        self.value_head = nn.Linear(hidden_dim, 1)

    def distributions(self, state):
        features = self.trunk(state)
        return [Categorical(logits=head(features)) for head in self.policy_heads]

    def forward(self, state):
        features = self.trunk(state)
        return self.distributions(state), self.value_head(features).squeeze(-1)

    def behavior_cloning_loss(self, state, logged_actions):
        distributions, _ = self(state)
        return sum(-dist.log_prob(logged_actions[..., index]).mean()
                   for index, dist in enumerate(distributions))

    def policy_kl(self, state, behavior_logits):
        learned, _ = self(state)
        return sum(kl_divergence(policy, Categorical(logits=reference)).mean()
                   for policy, reference in zip(learned, behavior_logits))

    def select_actions(self, state, deterministic=False):
        distributions, _ = self(state)
        if deterministic:
            return torch.stack([dist.logits.argmax(dim=-1) for dist in distributions], dim=-1)
        return torch.stack([dist.sample() for dist in distributions], dim=-1)
