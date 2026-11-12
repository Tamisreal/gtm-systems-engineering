"""Three ways to rank accounts, from simplest to most flexible.

1. Static ICP rule: what most teams start with. Core industry and 50 to 1,000 employees.
2. Lookalike (nearest neighbors): how similar is this account to accounts that bought?
   Needs no labels for losses, explains itself by naming the similar customers.
3. Logistic regression: learns weights from wins AND losses, outputs a probability
   that can be calibrated, and its coefficients are readable.
"""

import math


class RuleICP:
    """Score 1 if the account matches the written ICP, else 0. A baseline, not a model."""

    def __init__(self, industries: set[str], min_emp: int = 50, max_emp: int = 1000):
        self.industries, self.min_emp, self.max_emp = industries, min_emp, max_emp

    def score(self, accounts: list[dict]) -> list[float]:
        return [1.0 if a["industry"] in self.industries and self.min_emp <= a["employees"] <= self.max_emp else 0.0
                for a in accounts]


def _cosine(u: list[float], v: list[float]) -> float:
    dot = sum(a * b for a, b in zip(u, v))
    nu, nv = math.sqrt(sum(a * a for a in u)), math.sqrt(sum(b * b for b in v))
    return dot / (nu * nv) if nu and nv else 0.0


class Lookalike:
    """Mean cosine similarity to the k most similar closed-won accounts."""

    def __init__(self, k: int = 10):
        self.k = k

    def fit(self, X: list[list[float]], y: list[int], ids: list[str]) -> "Lookalike":
        self.won = [(x, i) for x, label, i in zip(X, y, ids) if label == 1]
        return self

    def neighbors(self, x: list[float]) -> list[tuple[float, str]]:
        sims = sorted(((_cosine(x, w), wid) for w, wid in self.won), reverse=True)
        return sims[: self.k]

    def score(self, X: list[list[float]]) -> list[float]:
        return [sum(s for s, _ in self.neighbors(x)) / self.k for x in X]


class LogisticRegression:
    """Batch gradient descent with L2 regularization. Small data, so plain Python is enough."""

    def __init__(self, lr: float = 0.1, epochs: int = 1500, l2: float = 0.01):
        self.lr, self.epochs, self.l2 = lr, epochs, l2

    @staticmethod
    def _sigmoid(z: float) -> float:
        z = max(-35.0, min(35.0, z))
        return 1 / (1 + math.exp(-z))

    def fit(self, X: list[list[float]], y: list[int]) -> "LogisticRegression":
        n, d = len(X), len(X[0])
        self.w, self.b = [0.0] * d, 0.0
        for _ in range(self.epochs):
            grad_w, grad_b = [0.0] * d, 0.0
            for xi, yi in zip(X, y):
                err = self._sigmoid(sum(w * v for w, v in zip(self.w, xi)) + self.b) - yi
                for j in range(d):
                    grad_w[j] += err * xi[j]
                grad_b += err
            self.w = [w - self.lr * (g / n + self.l2 * w) for w, g in zip(self.w, grad_w)]
            self.b -= self.lr * grad_b / n
        return self

    def predict_proba(self, X: list[list[float]]) -> list[float]:
        return [self._sigmoid(sum(w * v for w, v in zip(self.w, x)) + self.b) for x in X]

    def contributions(self, x: list[float], names: list[str], top: int = 3) -> list[tuple[str, float]]:
        """Largest positive per-feature contributions (weight x standardized value) for one account."""
        parts = sorted(((n, w * v) for n, w, v in zip(names, self.w, x)), key=lambda t: t[1], reverse=True)
        return [(n, round(c, 2)) for n, c in parts[:top] if c > 0]
