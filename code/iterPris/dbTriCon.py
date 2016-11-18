import random

class dbTriCon():
    '''
        author: Daniel Bishop
        This rule looks at the last 3 moves made by the opponent and chooses the most commonly made one.
        If there are less than 3 moves made, it randomly chooses a move.
    '''
    def step(self, history, round):
        if round < 3:
            action = random.randint(0, 1)
        else:
            # Counter wasn't working for me
            data = history[self.order^1]
            last3 = data[round - 1] + data[round - 2] + data[round - 3]
            if (last3 < 2):
                action = 0
            else:
                action = 1
        
        return action