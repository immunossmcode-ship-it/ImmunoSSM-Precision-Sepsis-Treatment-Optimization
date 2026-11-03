import torch
from torch import nn

class GatedCrossModalFusion(nn.Module):
    def __init__(self, modality_dim, fusion_dim, heads, dropout):
        super().__init__()
        self.gate = nn.Linear(modality_dim * 3, 3)
        self.projections = nn.ModuleList([nn.Linear(modality_dim, fusion_dim) for _ in range(3)])
        self.attention = nn.MultiheadAttention(fusion_dim, heads, dropout=dropout, batch_first=True)
        self.norm = nn.LayerNorm(fusion_dim)
        self.feedforward = nn.Sequential(
            nn.Linear(fusion_dim, fusion_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(fusion_dim, fusion_dim)
        )

    def forward(self, vital, biomarker, intervention):
        streams = torch.stack([vital, biomarker, intervention], dim=-2)
        weights = torch.softmax(self.gate(torch.cat([vital, biomarker, intervention], dim=-1)), dim=-1)
        weighted = sum(self.projections[index](streams[:, :, index]) * weights[..., index:index+1]
                       for index in range(len(self.projections)))
        attended, _ = self.attention(weighted, weighted, weighted, need_weights=False)
        return self.norm(weighted + self.feedforward(attended))
