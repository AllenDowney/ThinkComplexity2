import numpy as np

class CheckAndChoose():
    ''' CheckAndChoose will cooperate 5 times, defect 5 times, then choose which had the best average score. '''
    def step(self, history, round):
        if round < 5:
            action = 1 # Cooperate
        elif round < 10: 
            action = 0 # Defect
        elif round == 10:
            outcome = [[[1,1], [5,0]], [[0,5], [3,3]]]
            c_score = 0
            d_score = 0
            for i in range (0,10):
                if i < 5:
                    score = outcome[history[0][i]][history[1][i]]
                    c_score +=  score[self.order]
                    
                else:
                    score = outcome[history[0][i]][history[1][i]]
                    d_score +=  score[self.order]
            if c_score > d_score:
                action = 1
            else:
                action = 0
            
        else: 
            action =  history[self.order][round - 1]
                       
        return action

