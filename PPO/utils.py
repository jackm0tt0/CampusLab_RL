import numpy as np
import matplotlib.pyplot as plt
import time

def plot_learning_curve(x, scores, figure_file):

    running_avg = np.zeros(len(scores))
    for i in range(len(running_avg)):
        running_avg[i] = np.mean(scores[max(0, i-100):(i+1)])
    plt.plot(x, running_avg)
    plt.title('Running average of previous 100 scores')
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