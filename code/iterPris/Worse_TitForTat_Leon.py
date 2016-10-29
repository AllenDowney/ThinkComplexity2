class Worse_TitForTat_Leon():  
    def step(self, history, round):
        ''' 
        action = Your code here to determine what action your Rule will take.

        return action
        A defector will win against any other rule and tie vs itself, but it doesn't get a high number of points vs tit-for-tat.
        
        If the point is to beat other rules, we can't do better than a defector.
        
        If our goal is to earn the most points throughout the tournament, 
        a tit-for-tat rule would work better in an environment containing mostly non-defectors.
        '''
        if round == 0:
            action = 1
        elif round == 99:
            action = 0 #we try to take advantage of cooperative programs in the last round
        elif round >=90:
            if random.random()<0.95:
                action = history[self.order^1][round - 1]
            else: #versus a purely cooperative program, has a small chance of trying to take advantage near the end
                action = 0
        else:
            action = history[self.order^1][round - 1]
            # ^ is the bitwise XOR operator, for easy switching from 0 to 1.
        return action