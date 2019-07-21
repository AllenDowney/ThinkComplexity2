class AverageTitForTat():
 
    def step(self, history, round):
        import math
        if round == 0:
            action = 0
        else:
            past = []
            for act in history[self.order^1]:
                past.append(act)
            past = sum(past)/len(past)
            action = int(math.floor(past))

        return action
