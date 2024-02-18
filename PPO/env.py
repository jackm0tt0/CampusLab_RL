import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time
import os
from epw import weather_data



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
        self.max_episode_length = 50
        self.delta_T_threshold = 10

        self.weather = weather_data(self.path)

    def reset(self,i_path,game_round):
        # Read T_outside from an EPW file
        temperature, humidity, wind_direction, wind_speed = self.weather.get_weather_data(game_round)
        self.T_outside = temperature

        # Set T_inside as T_outside + random(-5, 5)
        self.T_inside = self.T_outside + np.random.uniform(-5, 5)
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
        if self.T_min < self.T_inside < self.T_max:
            reward += 1
        if abs(self.T_inside - self.T_min) > 5:
            reward -= 1
        if abs(self.T_inside - self.T_max) > 5:
            reward -= 1

        # Update episode length
        self.episode_length += 1

        # Check termination conditions
        done = (abs(self.T_inside - self.T_outside) > self.delta_T_threshold) or (
                    self.episode_length >= self.max_episode_length)

        return np.array([self.T_outside, self.T_inside], dtype=np.float32), reward, done, {}

    def render(self, mode='human'):
        print(f"Outside Temperature: {self.T_outside}°C, Inside Temperature: {self.T_inside}°C")

class SimpleGrasshopperEnv(gym.Env):
    def __init__(self):
        # Action space: 0-close window, 1-open window
        self.action_space = spaces.Discrete(2)

        # Observation space: [outside temperature, inside temperature]
        self.observation_space = spaces.Box(low=np.array([-50, -50]), high=np.array([50, 50]), dtype=np.float32)

        # set intial internal temperature
        # keeps temp from last time and adapts
        # self.T_inside = np.random.uniform(10, 38)
        self.T_inside = None

        # Initial state
        self.path = 'E:\\ITECH\\23W\\Studio\\CampusLab_RL\\epw\\DEU_BW_Stuttgart-Schnarrenberg.107390_TMYx.epw'
        self.reset(0)

        # Reward rules parameters
        self.T_min = 18
        self.T_max = 25

        # Episode termination conditions
        self.max_episode_length = 5
        self.delta_T_threshold = 10

        self.weather = weather_data(self.path)

    def reset(self, game_round):
        # Read T_outside from an EPW file
        temperature, humidity, wind_direction, wind_speed = self.weather.get_weather_data(game_round)
        self.T_outside = temperature

        # Set T_inside as T_outside + random(-5, 5)
        if self.T_inside == None:
            self.T_inside = self.T_outside + np.random.uniform(-5, 5)
        self.episode_length = 0
        return np.array([self.T_outside, self.T_inside], dtype=np.float32)

    def step(self, action):

        request_path = r'post/request.txt' 
        reply_path = r'post/reply.txt' 

        #when was the reply last modified?
        initial_mtime = os.path.getmtime(reply_path)

        #create a request to the gh file   

        #make 
        max_attempts = 3
        for i in range(max_attempts+1):
            try:
                with open(request_path, 'w') as file:
                    txt = ""
                    txt += str(self.T_min)+"\n"
                    txt += str(self.T_max)+"\n"
                    txt += str(self.T_outside)+"\n"
                    txt += str(self.T_inside)+"\n"
                    txt += str(action)+"\n"
                    file.write(txt)
                    file.close()              
                print("Request Sent", end='',flush = True)
                break

            except (PermissionError, FileNotFoundError) as e:
                if i == max_attempts:
                    print("Max attempts reached. Unable to read file.")
                    raise(e)
                else:
                    print(f"{request_path} is unavailable. Attempt {i}: {e}")
                    time.sleep(.2)  # Wait for a short duration before retrying
        
        
        #wait for the gh script to write a reply
        max_response_time = 5
        response_time = 0
        while response_time <= max_response_time:
            sleep_time = .1
            response_time += sleep_time
            time.sleep(sleep_time)
            print(".",end='',flush = True)
            current_mtime = os.path.getmtime(reply_path)
            if current_mtime != initial_mtime:
                break
        if current_mtime == initial_mtime:
            raise Exception("""
            Maximimum Response Time Exceeded
            [1] is the grasshopper file open?
            [2] is the file path set correctly?
            [3] is the file set to synchronize?
            [4] does the simulation require more time? --> change max_response time""")
           
        with open(reply_path, 'r') as file:
            txt = file.readlines()
            if len(txt) is not 0:
                self.T_inside = float(txt[0])
                reward = float(txt[1])
                print(f"Reply: Reward = {reward}")
            else:
                print("Simulation Failed: Reward = 0")
                reward = 0

            file.close()

        # Update episode length
        self.episode_length += 1

        # Check termination conditions
        done = (abs(self.T_inside - self.T_outside) > self.delta_T_threshold) or (
                    self.episode_length >= self.max_episode_length)

        return np.array([self.T_outside, self.T_inside], dtype=np.float32), reward, done, {}

    def render(self, mode='human'):
        print(f"Outside Temperature: {self.T_outside}°C, Inside Temperature: {self.T_inside}°C")


class Simulation_GrasshopperEnv(gym.Env):
    def __init__(self):
        # Action space: 0-close window, 1-open window
        self.action_space = spaces.Discrete(2)

        # Observation space: [outside temperature, inside temperature]
        self.observation_space = spaces.Box(low=np.array([-50, -50]), high=np.array([50, 50]), dtype=np.float32)
        # set intial internal temperature
        # keeps temp from last time and adapts
        # self.T_inside = np.random.uniform(10, 38)
        # Initial state
        self.path = 'E:\\ITECH\\23W\\Studio\\CampusLab_RL\\epw\\DEU_BW_Stuttgart-Schnarrenberg.107390_TMYx.epw'
        self.weather = weather_data(self.path)
        self.reset()
        self.T_inside = self.T_outside + np.random.uniform(-5, 5)

        # # Reward rules parameters
        # self.T_min = 18
        # self.T_max = 25

        # Episode termination conditions
        self.max_episode_length = 5
        self.delta_T_threshold = 30

    def reset(self):

        # Read T_outside from an EPW file
        index = np.random.randint(0, 8759)
        month, day, hour = self.weather.get_period(index)
        temperature, humidity, wind_direction, wind_speed = self.weather.get_weather_data(index)
        self.T_outside = temperature
        self.month = month
        self.day = day
        self.hour = hour

        if not hasattr(self, 'T_inside') :
            self.T_inside = self.T_outside + np.random.uniform(-5, 5)

        self.episode_length = 0
        return np.array([self.T_outside, self.T_inside], dtype=np.float32)

    def step(self, action):
        request_path = r'post/request.txt'
        reply_path = r'post/reply.txt'

        # when was the reply last modified?
        initial_mtime = os.path.getmtime(reply_path)

        # create a request to the gh file

        # make
        max_attempts = 3
        for i in range(max_attempts + 1):
            try:
                with open(request_path, 'w') as file:
                    txt = ""
                    # txt += str(self.T_min) + "\n"
                    # txt += str(self.T_max) + "\n"
                    # txt += str(self.T_outside) + "\n"
                    txt += str(self.T_inside) + "\n"
                    txt += str(action) + "\n"
                    txt += str(self.month) + "\n"
                    txt += str(self.day) + "\n"
                    txt += str(self.hour) + "\n"
                    file.write(txt)
                    file.close()
                print("Request Sent", end='', flush=True)
                break

            except (PermissionError, FileNotFoundError) as e:
                if i == max_attempts:
                    print("Max attempts reached. Unable to read file.")
                    raise (e)
                else:
                    print(f"{request_path} is unavailable. Attempt {i}: {e}")
                    time.sleep(.2)  # Wait for a short duration before retrying


        # wait for the gh script to write a reply
        max_response_time = 10
        response_time = 0
        while response_time <= max_response_time:
            sleep_time = .1
            response_time += sleep_time
            time.sleep(sleep_time)
            print(".", end='', flush=True)

            current_mtime = os.path.getmtime(reply_path)
            if current_mtime != initial_mtime:
                break
        if current_mtime == initial_mtime:
            raise Exception("""
            Maximimum Response Time Exceeded
            [1] is the grasshopper file open?
            [2] is the file path set correctly?
            [3] is the file set to synchronize?
            [4] does the simulation require more time? --> change max_response time""")

        with open(reply_path, 'r') as file:
            txt = file.readlines()
            if len(txt) is not 0:
                self.T_inside = float(txt[0])
                reward = float(txt[1])
                print(f"Reply: Reward = {reward}")
            else:
                print("Simulation Failed: Reward = 0")
                reward = 0

            file.close()

        #Update episode length
        self.episode_length += 1

        # Check termination conditions
        done = (abs(self.T_inside - self.T_outside) > self.delta_T_threshold) or (
                self.episode_length >= self.max_episode_length)

        return np.array([self.T_outside, self.T_inside], dtype=np.float32), reward, done, {}

    def render(self, mode='human'):
        print(f"Outside Temperature: {self.T_outside}°C, Inside Temperature: {self.T_inside}°C")