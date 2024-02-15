from env import VentilationEnv, SimpleGrasshopperEnv
import numpy as np
from agent import Agent
from utils import plot_learning_curve
import os
import tensorflow as tf

if __name__ == '__main__':

    #GPU check
    tf.debugging.set_log_device_placement(False) #see if tasks are assigned to GPU or CPU
    
    if len(tf.config.list_physical_devices('GPU')):
        print("\nGPU Found", tf.config.list_physical_devices('GPU')[0], "\n")
    else:
        print("\nNO GPU FOUND\n")

    env = SimpleGrasshopperEnv()
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=2, batch_size=batch_size,
                  alpha=alpha, n_epochs=n_epochs,
                  input_dims=2)
    
    n_games = 100

    figure_file = r'plots/gh_env.png'
    #make sure it exists
    if not os.path.exists("./plots/"):
        os.mkdir("./plots")

    if not os.path.exists("./post/"):
        os.mkdir("./post")


    best_score = env.reward_range[0]
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        observation = env.reset(i)
        done = False
        score = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            n_steps += 1
            score += reward
            agent.store_transition(observation, action,
                                   prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)
    x = [i+1 for i in range(len(score_history))]
    plot_learning_curve(x, score_history, figure_file)