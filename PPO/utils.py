import numpy as np
import matplotlib.pyplot as plt

class learning_curve:
    def __init__(self):
        self.path = 'cartpole.png'
        self.figure1, self.ax1 = plt.subplots()

    def draw_learning_curve(self, x, scores):
        running_avg = np.zeros(len(scores))
        for i in range(len(running_avg)):
            running_avg[i] = np.mean(scores[max(0, i-100):(i+1)])
        self.ax1.plot(x, running_avg)
        self.ax1.set_title('Running average of previous 100 scores')
        self.figure1.savefig(self.path)

