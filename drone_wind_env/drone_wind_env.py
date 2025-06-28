import gymnasium as gym
from gymnasium import spaces
import numpy as np


class DroneWindEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode

        self.x_limit = (-10, 10)
        self.y_limit = (-10, 10)

        self.target = np.array([5.0, 5.0])

        self.action_space = spaces.Discrete(4)  # Up, Down, Left, Right

        high = np.array([10, 10, 5, 5], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.max_speed = 2.0
        self.wind = np.zeros(2)
        self.wind_change_interval = 10

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.pos = np.array([0.0, 0.0])
        self.vel = np.array([0.0, 0.0])
        self.steps = 0
        self._update_wind()

        obs = np.concatenate([self.pos, self.vel]).astype(np.float32)
        return obs, {}

    def _update_wind(self):
        self.wind = np.random.uniform(-0.2, 0.2, size=2)

    def step(self, action):
        force = np.zeros(2)
        if action == 0:  # Up
            force[1] += 1.0
        elif action == 1:  # Down
            force[1] -= 1.0
        elif action == 2:  # Left
            force[0] -= 1.0
        elif action == 3:  # Right
            force[0] += 1.0

        self.vel += force * 0.1 + self.wind * 0.1
        self.vel = np.clip(self.vel, -self.max_speed, self.max_speed)

        self.pos += self.vel * 0.5

        self.pos = np.clip(self.pos, self.x_limit[0], self.x_limit[1])

        self.steps += 1
        if self.steps % self.wind_change_interval == 0:
            self._update_wind()

        dist_to_target = np.linalg.norm(self.pos - self.target)
        done = False
        reward = -1

        if dist_to_target < 0.5:
            reward = 100
            done = True
        elif (
            self.pos[0] <= self.x_limit[0]
            or self.pos[0] >= self.x_limit[1]
            or self.pos[1] <= self.y_limit[0]
            or self.pos[1] >= self.y_limit[1]
        ):
            reward = -50
            done = True

        obs = np.concatenate([self.pos, self.vel]).astype(np.float32)

        return obs, reward, done, False, {}

    def render(self):
        print(f"Position: {self.pos}, Velocity: {self.vel}, Wind: {self.wind}")

    def close(self):
        pass
