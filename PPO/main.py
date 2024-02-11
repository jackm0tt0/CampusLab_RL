from env import VentilationEnv
import numpy as np
from agent import Agent
from utils import learning_curve
from canvas import show_canvas

if __name__ == '__main__':
    env = VentilationEnv()
    canvas = show_canvas()
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0003
    agent = Agent(n_actions=2, batch_size=batch_size,
                  alpha=alpha, n_epochs=n_epochs,
                  input_dims=2)
    n_games = 10

    best_score = env.reward_range[0]
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = 0

    for i in range(n_games):
        observation = env.reset()
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
            canvas.update(action,env.T_inside,env.T_outside,n_steps)

        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        if avg_score > best_score:
            best_score = avg_score
            agent.save_models()

        print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score,
              'time_steps', n_steps, 'learning_steps', learn_iters)
    x = [i+1 for i in range(len(score_history))]
    lc = learning_curve()
    lc.draw_learning_curve(x,score_history)