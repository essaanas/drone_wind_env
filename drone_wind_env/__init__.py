"""
drone_wind_env_student
~~~~~~~~~~~~~~~~~~~~~~
Gymnasium-compatible DroneWind environment *plus*
per-student configuration utilities.
"""

from gymnasium.envs.registration import register
from .student_config import generate_config

# Register environment with Gymnasium
register(
    id="DroneWind-v0",
    entry_point="drone_wind_env.drone_wind_env:DroneWindEnv",
)
__all__ = ["generate_config"]



