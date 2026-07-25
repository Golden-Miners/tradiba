from typing import Any

def calculate_accuracy(predictions: list[Any], labels: list[Any]) -> float:
    """Calculate basic classification accuracy."""
    if not predictions:
        return 0.0
    correct = sum(1 for p, lbl in zip(predictions, labels) if p == lbl)
    return correct / len(predictions)

def calculate_mse(predictions: list[float], labels: list[float]) -> float:
    """Calculate Mean Squared Error for regression."""
    if not predictions:
        return 0.0
    errors = [(p - lbl) ** 2 for p, lbl in zip(predictions, labels)]
    return sum(errors) / len(predictions)
