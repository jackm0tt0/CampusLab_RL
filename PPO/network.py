import keras
from keras.layers import  Dense


class ActorNetwork(keras.Model):
    def __init__(self, fc1_dims=64, fc2_dims=64, n_actions=2):
        super(ActorNetwork, self).__init__()

        self.fc1 = Dense(fc1_dims, activation='relu')
        self.fc2 = Dense(fc2_dims, activation='relu')
        self.output_layer = Dense(n_actions, activation='softmax')

    def call(self, state):
        x = self.fc1(state)
        x = self.fc2(x)
        actions_prob = self.output_layer(x)

        return actions_prob

class CriticNetwork(keras.Model):
    def __init__(self, fc1_dims=64, fc2_dims=64):
        super(CriticNetwork, self).__init__()

        self.fc1 = Dense(fc1_dims, activation='relu')
        self.fc2 = Dense(fc2_dims, activation='relu')
        self.q = Dense(1, activation=None)

    def call(self, state):
        x = self.fc1(state)
        x = self.fc2(x)
        q_value = self.q(x)

        return q_value