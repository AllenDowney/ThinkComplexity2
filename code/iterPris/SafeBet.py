import random

class Trustworthy():
    ''' Will hopefully pose as trustworthy to other prisoners
    '''
    def step(self, history, round):
	    if round%5 == 4:
	    	return 0
	    else: return 1 