from collections import defaultdict
import math

class MarkovScorer:
    """
    Character-level 2-gram Markov scorer.
    Used ONLY to rank passwords by likelihood.
    """

    def __init__(self):
        self.model = defaultdict(int)
        self.total = 0

    def train(self, words):
        for word in words:
            w = f"^{word}$"
            for i in range(len(w) - 1):
                pair = w[i:i+2]
                self.model[pair] += 1
                self.total += 1

    def score(self, word):
        score = 0.0
        w = f"^{word}$"
        for i in range(len(w) - 1):
            pair = w[i:i+2]
            prob = self.model.get(pair, 1) / self.total
            score += math.log(prob)
        return score
