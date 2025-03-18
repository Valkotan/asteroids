from constants import SCORE_AMOUNT

class ScoreManager:
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.score = 0
        self.score_amount = SCORE_AMOUNT
    
    def increment_score(self):  #Default score
        self.score += self.score_amount

    def get_score(self):
        return self.score
