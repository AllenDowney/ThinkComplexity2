import random

class TFTMemory():
    """ TFTMemory is similar to TitForTat, but it calculates its move based on
    all of its opponents' previous moves, instead of just the most recent one. """
    def step(self, history, round):
        if round == 0:
            action = random.randint(0, 1)
        else:
            past = sum(history[self.order^1])
            action = int(past > round / 2.0)
        return action
