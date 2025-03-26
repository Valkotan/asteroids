from constants import SCORE_AMOUNT

class ScoreManager:
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.score = 0
        self.score_amount = SCORE_AMOUNT
    
    def increment_score(self, extra_points=0):  # Allows for additional points
        self.score += self.score_amount + extra_points

    def get_score(self):
        return self.score