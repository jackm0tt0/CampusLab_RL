import numpy as np
import matplotlib.pyplot as plt
import time

class learning_curve:

    def __init__(self):
        pass

    def game_score(self, x, scores):
        running_avg = np.zeros(len(scores))
        for i in range(len(running_avg)):
            running_avg[i] = np.mean(scores[max(0, i - 500):(i + 1)])
        self.plot(x, running_avg)
        self.set_title('Running average of previous 500 scores')
        self.savefig(self.path)

    def game_episodelength(self,x,episode,figure_file):
        episode_len = np.zeros(len(episode))
        for i in range(len(episode)):
            episode_len[i] = episode_len[i]
        plt.plot(x, episode_len)
        plt.title('Episode length in each game')
        plt.savefig(figure_file)

def safe_read_file(file_path, max_attempts=3):
    attempt = 1
    while attempt <= max_attempts:
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            return data
        except (PermissionError, FileNotFoundError) as e:
            print(f"Attempt {attempt}: {e}")
            attempt += 1
            time.sleep(1)  # Wait for a short duration before retrying
    print("Max attempts reached. Unable to read file.")
    return None