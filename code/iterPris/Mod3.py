class Mod3():
    ''' Loop through defecting 1 time and then cooperating 2 times. '''
    def step(self, history, round):
        action = round%3
        if action==2:
        	action = 1
        return action