# Cooperating twice in a row has better payoff than cooperating once and then betraying

class ResponsiveTFTMod():
    """
    Cooperate until opponent defects.
    Then run TitForTat but throw the sequence every
    three rounds to prevent oscillation.
    Even with defect, beats others, low total score
    """
    def step(self, history, round):
        if round == 1:
            action = 1
        if round % 3 == 0:
            action = 0
        else:
            # Check if the opponent has defected before - no forgivness version
            opp_defect_count = 0
            for opp_move in history[self.order^1]:
                if opp_move == 0:
                    opp_defect_count += 1

            if opp_defect_count > 0:
                action = history[self.order^1][round - 1]
            else:
                action = 1

        return action