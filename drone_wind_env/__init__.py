from gymnasium.envs.registration import register

register(
    id="DroneWind-v0",
    entry_point="drone_wind_env.drone_wind_env:DroneWindEnv",
)
