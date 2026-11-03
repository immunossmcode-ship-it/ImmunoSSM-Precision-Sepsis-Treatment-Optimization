from torch import nn
from .vital_encoder import VitalSignEncoder
from .biomarker_encoder import BiomarkerEncoder
from .intervention_encoder import InterventionEncoder
from .fusion import GatedCrossModalFusion
from .pste import build_pste

def _required(config, section, key):
    value = config.get(section, {}).get(key)
    if value is None:
        raise ValueError(f"Set configs/model_config.yaml: {section}.{key} from the verified study implementation.")
    return value

class ImmunoSSM(nn.Module):
    """Composable ImmunoSSM research model; see IMPLEMENTATION_STATUS.md for scope."""
    def __init__(self, config):
        super().__init__()
        a = config["architecture"]
        vital = config["vital_encoder"]
        required_arch = ["vital_input_dim", "biomarker_input_dim", "intervention_input_dim",
                         "modality_embedding_dim", "fusion_dim", "state_dim", "pste_layers",
                         "ssm_heads", "dropout"]
        missing = [key for key in required_arch if a.get(key) is None]
        if missing:
            raise ValueError(f"Complete manuscript-verified architecture fields in model_config.yaml: {missing}")
        if vital.get("kernel_size") is None:
            raise ValueError("Set vital_encoder.kernel_size from the verified study implementation.")
        d = int(a["modality_embedding_dim"])
        dropout = float(a["dropout"])
        self.vital_encoder = VitalSignEncoder(
            int(a["vital_input_dim"]), d, dropout,
            vital["dilation_rates"], int(vital["kernel_size"])
        )
        self.biomarker_encoder = BiomarkerEncoder(int(a["biomarker_input_dim"]), d, dropout)
        self.intervention_encoder = InterventionEncoder(int(a["intervention_input_dim"]), d, dropout)
        self.fusion = GatedCrossModalFusion(d, int(a["fusion_dim"]), int(a["ssm_heads"]), dropout)
        self.pste = build_pste(int(a["fusion_dim"]), int(a["state_dim"]),
                               int(a["pste_layers"]), dropout)
        self.mortality_head = nn.Linear(int(a["fusion_dim"]), 1)
        self.trajectory_head = nn.Linear(int(a["fusion_dim"]), int(a["biomarker_input_dim"]))

    def forward(self, vital, biomarker, biomarker_confidence, intervention):
        vital_embedding = self.vital_encoder(vital)
        biomarker_embedding = self.biomarker_encoder(biomarker, biomarker_confidence)
        intervention_embedding = self.intervention_encoder(intervention)
        fused = self.fusion(vital_embedding, biomarker_embedding, intervention_embedding)
        trajectory = self.pste(fused)
        return {
            "latent_trajectory": trajectory,
            "mortality_logits": self.mortality_head(trajectory),
            "biomarker_forecast": self.trajectory_head(trajectory),
        }
