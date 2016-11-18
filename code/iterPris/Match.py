class Match():
    ''' Defines a match which takes two rules and facilitates a game of iterated
        prisoner's dilemma between them.
    '''
    def __init__(self, ruleA, ruleB, length):
        ''' Init method for Match class.

            ruleA, ruleB: instances of rules
            length (int): the number of rounds to be played in this match
        '''

        order = [ruleA, ruleB]
        self.rule0 = order[0]
        self.rule0.order = 0

        self.rule1 = order[1]
        self.rule1.order = 1

        self.round = 0
        self.length = length
        self.history = [[],[]]

        self.name = name(self.rule0) + '-' + name(self.rule1)

    def run(self):
        while True:
            self.step_round()
            if self.round >= self.length:
                break

    def halted_run(self):
        while True:
            self.step_round()
            if self.round >= self.length:
                break
            print(self.history)
            print(self.score())
            input()

    def step_round(self):
        ''' Runs one round of iterated prisoners dilemma by running the step
            functions of each rule and adding them to the history, then
            advancing a round.
        '''

        action0 = self.rule0.step(self.history, self.round)
        action1 = self.rule1.step(self.history, self.round)

        if (action0 not in [0, 1]):
            raise ValueError(name(self.rule0) + 'did not provide a valid action')
        if (action1 not in [0, 1]):
            raise ValueError(name(self.rule1) + 'did not provide a valid action')

        self.history[0].append(action0)
        self.history[1].append(action1)

        self.round += 1

    def score(self):
        ''' Calculate scores for the match based on the history.

            Both cooperate: 3 points for both.
            One cooperates, one defects: 5 points for the one who defected, 0
                for the other.
            Both defect: 1 point for both.
         '''

        outcome = [[[1,1], [5,0]], [[0,5], [3,3]]]
        scoring = [0, 0]

        for i in range(len(self.history[0])):
            round_score = outcome[self.history[0][i]][self.history[1][i]]
            scoring[0] += round_score[0]
            scoring[1] += round_score[1]

        return scoring

def name(rule):
    n = type(rule).__name__
    return n

def print_history(match):
    print(match.name)
    for i in range(len(match.history[0])):
        print('    ' + str(match.history[0][i]) + '        ' + str(match.history[1][i]))