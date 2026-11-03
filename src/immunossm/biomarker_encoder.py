import torch
from torch import nn

class BiomarkerEncoder(nn.Module):
    def __init__(self, input_dim, embedding_dim, dropout):
        super().__init__()
        self.value_projection = nn.Linear(input_dim, embedding_dim)
        self.freshness_projection = nn.Linear(input_dim, embedding_dim)
        self.norm = nn.LayerNorm(embedding_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, values, confidence):
        # confidence encodes observation freshness for each biomarker channel
        encoded = self.value_projection(values) + self.freshness_projection(confidence)
        return self.dropout(self.norm(torch.nn.functional.gelu(encoded)))
