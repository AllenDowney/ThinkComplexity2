class fifty_is_good():
    def step(self, history, round_num):
        other_idx = 1 - self.order
        try:
            prob = sum(history[other_idx])/len(history[other_idx])
        except ZeroDivisionError:
            prob = 0
        if prob >= 0.5:
            return 0
        else:
            return 1
        