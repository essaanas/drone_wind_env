import gymnasium as gym
from gymnasium import spaces
import numpy as np


class DroneWindEnv(gym.Env):
    """
    2-D Drone navigation with wind; 4 discrete thrust actions.
    Accepts optional `config` dict for per-student variability.
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, config=None):
        super().__init__()
        self.render_mode = render_mode

        # ----- Fixed arena limits -----
        self.x_bounds = (-10.0, 10.0)
        self.y_bounds = (-10.0, 10.0)
        self.goal = np.array([5.0, 5.0])

        # ----- Action & observation spaces -----
        self.action_space = spaces.Discrete(4)  # 0=Up,1=Down,2=Left,3=Right
        high = np.array([10, 10, 5, 5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        # ----- Default dynamics -----
        self.max_speed = 2.0
        self.wind_scale = 1.0
        self.wind_update_interval = 10

        # ----- Allow per-student overrides -----
        self.start_position = np.array([0.0, 0.0], dtype=np.float32)
        if config:
            self.apply_student_config(config)

        self.reset()

    # --------------------------------------------------------------------- #
    # Utilities                                                             #
    # --------------------------------------------------------------------- #
    def apply_student_config(self, cfg: dict):
        if "start_position" in cfg:
            self.start_position = np.array(cfg["start_position"], dtype=np.float32)
        if "wind_scale" in cfg:
            self.wind_scale = float(cfg["wind_scale"])
        if "wind_update_interval" in cfg:
            self.wind_update_interval = int(cfg["wind_update_interval"])

    def _random_wind(self):
        # wind ∈ [-0.2, 0.2] × scale
        return self.wind_scale * np.random.uniform(-0.2, 0.2, size=2)

    # --------------------------------------------------------------------- #
    # Gym API                                                               #
    # --------------------------------------------------------------------- #
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.pos = self.start_position.copy()
        self.vel = np.zeros(2, dtype=np.float32)
        self.steps = 0
        self.wind = self._random_wind()
        return self._get_obs(), {}

    def step(self, action: int):
        thrust = np.zeros(2)
        if action == 0:   # Up
            thrust[1] += 1.0
        elif action == 1:  # Down
            thrust[1] -= 1.0
        elif action == 2:  # Left
            thrust[0] -= 1.0
        elif action == 3:  # Right
            thrust[0] += 1.0

        # Dynamics
        self.vel += 0.1 * (thrust + self.wind)
        self.vel = np.clip(self.vel, -self.max_speed, self.max_speed)
        self.pos += 0.5 * self.vel
        self.pos[0] = np.clip(self.pos[0], *self.x_bounds)
        self.pos[1] = np.clip(self.pos[1], *self.y_bounds)

        # Wind update
        self.steps += 1
        if self.steps % self.wind_update_interval == 0:
            self.wind = self._random_wind()

        # Reward & termination
        distance = np.linalg.norm(self.pos - self.goal)
        terminated = distance < 0.5
        reward = 100.0 if terminated else -1.0

        obs = self._get_obs()
        return obs, reward, terminated, False, {}

    def _get_obs(self):
        return np.concatenate([self.pos, self.vel]).astype(np.float32)

    def render(self):
        if self.render_mode == "human":
            print(
                f"pos={self.pos}, vel={self.vel}, wind={self.wind}, steps={self.steps}"
            )

    def close(self):
        pass
