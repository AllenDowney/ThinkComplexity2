import numpy as np

class Patrick():
    ''' TitForTat with random defection of 20% added in '''
    def step(self, history, round):
        if round == 0:
            action = 1
        else:
            opponent = history[self.order^1][round - 1]
            random_meanness = np.random.random() < .20
            
            if (random_meanness):
                action = 0
            else:
                action = opponent

        return action