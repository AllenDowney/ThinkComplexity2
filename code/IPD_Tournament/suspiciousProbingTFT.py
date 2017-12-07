import random
class SPTFT():
    ''' Suspicious, Probing TitForTat will replicate its opponent's last move, start by defecting, and occasionally make a random move '''
    def step(self, history, round):
        if round == 0:
            action = 0
            
        elif random.random() < 0.125:
                action = random.choice([0,1])
        else:
            action = history[self.order^1][round - 1]
            # ^ is the bitwise XOR operator, for easy switching from 0 to 1.
        return action
