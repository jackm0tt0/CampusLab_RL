import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time


class VentilationEnv(gym.Env):
    def __init__(self):
        # Action space: 0-close window, 1-open window
        self.action_space = spaces.Discrete(2)

        # Observation space: [outside temperature, inside temperature]
        self.observation_space = spaces.Box(low=np.array([-50, -50]), high=np.array([50, 50]), dtype=np.float32)

        # Initial state
        self.reset()

        # Reward rules parameters
        self.T_min = 18
        self.T_max = 25

        # Episode termination conditions
        self.max_episode_length = 10
        self.delta_T_threshold = 10

    def reset(self):
        self.T_outside = np.random.uniform(13, 30)
        self.T_inside = self.T_outside + np.random.uniform(-5, 5)
        self.T_inside_base = self.T_inside
        self.episode_length = 0
        return np.array([self.T_outside, self.T_inside], dtype=np.float32)

    def step(self, action):
        # Apply action: 0-close window, 1-open window
        if action == 1:
            delta = self.T_outside - self.T_inside
            if delta > 0:
                self.T_inside += 1  # Adjust as needed
            elif delta == 0:
                self.T_inside += 0
            else:
                self.T_inside -= 1

        # Temperature constraints
        reward = 0
        if abs(self.T_inside - self.T_min)>5 or abs(self.T_inside - self.T_max)>5:
            reward -=1
        if self.T_inside < self.T_min:
            if self.T_inside_base < self.T_inside:
                reward += 0.2
            else:
                reward -= 0.2
        if self.T_inside > self.T_min:
            if self.T_inside_base > self.T_inside:
                reward += 0.2
            else:
                reward -= 0.2

        # Update episode length
        self.episode_length += 1

        # Check termination conditions
        done = (abs(self.T_inside - self.T_outside) > self.delta_T_threshold) or (
                    self.episode_length >= self.max_episode_length)

        time.sleep(0.01)

        return np.array([self.T_outside, self.T_inside], dtype=np.float32), reward, done, {}

    def render(self, mode='human'):
        print(f"Outside Temperature: {self.T_outside}°C, Inside Temperature: {self.T_inside}°C")

