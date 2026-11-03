from torch import nn

class InterventionEncoder(nn.Module):
    def __init__(self, input_dim, embedding_dim, dropout):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, embedding_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.LayerNorm(embedding_dim)
        )

    def forward(self, intervention_events):
        return self.encoder(intervention_events)
