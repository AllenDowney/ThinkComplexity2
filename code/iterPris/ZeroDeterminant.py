"""
Hugely inspired by the Zero Determinant Implementations found in the Python-Axelrod library

http://axelrod.readthedocs.io/en/latest/reference/overview_of_strategies.html#zdgtft-2
https://github.com/Axelrod-Python/Axelrod/blob/master/axelrod/strategies/memoryone.py
"""
import random

C = 1
D = 0

class ZeroDeterminant():
    """It uses transition probabilities based on the last round of play by both players.
    This strategy came in 1st in average score during a 2012 run of a tournament"""

    probs = [1, 1/8., 1, 1/4.]

    def __init__(self):
        self.four_vector = dict(zip([(C,C),(C,D),(D,C),(D,D)], self.probs))

    def step(self, history, round):
        if round == 0:
            action = C
        else:
            probC = self.four_vector[(history[self.order][round-1], history[self.order^1][round-1])]
            action = int(random.random() <= probC)
        return action

if __name__ == "__main__":
    zd = ZeroDeterminant()
    zd.order = 0
    print zd.step([[0],[0]], 1)
    print zd.step([[0],[1]], 1)
    print zd.step([[1],[0]], 1)
    print zd.step([[1],[1]], 1)
