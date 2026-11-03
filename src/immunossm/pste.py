from .persistent_ssm import PersistentStateSpaceTrajectoryEngine

def build_pste(model_dim, state_dim, layers, dropout):
    return PersistentStateSpaceTrajectoryEngine(model_dim, state_dim, layers, dropout)
