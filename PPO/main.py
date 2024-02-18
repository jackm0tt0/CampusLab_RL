from env import VentilationEnv, SimpleGrasshopperEnv
import numpy as np
from agent import Agent
from utils import learning_curve
import os
import tensorflow as tf
import datetime
from keras.callbacks import  TensorBoard

if __name__ == '__main__':

    #GPU check
    tf.debugging.set_log_device_placement(False) #see if tasks are assigned to GPU or CPU
    
    if len(tf.config.list_physical_devices('GPU')):
        print("\nGPU Found", tf.config.list_physical_devices('GPU')[0], "\n")
    else:
        print("\nNO GPU FOUND\n")


    env = SimpleGrasshopperEnv()
    learning_curve = learning_curve()
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=2, batch_size=batch_size,
                  alpha=alpha, n_epochs=n_epochs,
                  input_dims=2)
    
    n_games = 500

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    game_score = r'plots/game_score.png'
    game_episode = r'plots/game_episode.png'
    #make sure it exists
    if not os.path.exists("./plots/"):
        os.mkdir("./plots")

    if not os.path.exists("./post/"):
        os.mkdir("./post")


    best_score = env.reward_range[0]
    score_history = []
    episode_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    # TensorBoard callback
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1, update_freq='epoch')
    tensorboard_callback.set_model(model = agent.actor)

    for i in range(n_games):
        observation = env.reset()
        done = False
        score = 0
        episode_len = 0
        while not done:
            action, prob, val = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            n_steps += 1
            episode_len += 1
            score += reward
            agent.store_transition(observation, action,
                                   prob, val, reward, done)

            if n_steps % N == 0:
                agent.learn(callback=tensorboard_callback)
                learn_iters += 1
            observation = observation_


        score_history.append(score)
        episode_history.append(episode_len)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)

    print(score_history)
    x = [i+1 for i in range(len(score_history))]
    learning_curve.game_score(x, score_history, game_score)
    learning_curve.game_score(x, episode_history, game_episode)
