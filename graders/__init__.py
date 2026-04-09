"""Graders package for the Text-to-SQL OpenEnv environment.

Exports graders for each difficulty level:
- EasyGrader: SQL execution grading for easy tasks
- MediumGrader: SQL execution grading for medium tasks
- HardGrader: SQL execution grading for hard tasks
"""

import grader as grading_module


class EasyGrader:
    """Grader for easy difficulty SQL tasks."""

    def __init__(self):
        self.last_breakdown = {}

    def grade(self, predicted_result: list, expected_result: list) -> float:
        """Grade SQL query results for easy tasks.

        Returns score strictly between 0.0 and 1.0 for OpenEnv validation.
        """
        score = grading_module.grade_result(predicted_result, expected_result)
        self.last_breakdown = {
            "predicted_count": len(predicted_result or []),
            "expected_count": len(expected_result or []),
            "score": score,
        }
        return score


class MediumGrader:
    """Grader for medium difficulty SQL tasks."""

    def __init__(self):
        self.last_breakdown = {}

    def grade(self, predicted_result: list, expected_result: list) -> float:
        """Grade SQL query results for medium tasks.

        Returns score strictly between 0.0 and 1.0 for OpenEnv validation.
        """
        score = grading_module.grade_result(predicted_result, expected_result)
        self.last_breakdown = {
            "predicted_count": len(predicted_result or []),
            "expected_count": len(expected_result or []),
            "score": score,
        }
        return score


class HardGrader:
    """Grader for hard difficulty SQL tasks."""

    def __init__(self):
        self.last_breakdown = {}

    def grade(self, predicted_result: list, expected_result: list) -> float:
        """Grade SQL query results for hard tasks.

        Returns score strictly between 0.0 and 1.0 for OpenEnv validation.
        """
        score = grading_module.grade_result(predicted_result, expected_result)
        self.last_breakdown = {
            "predicted_count": len(predicted_result or []),
            "expected_count": len(expected_result or []),
            "score": score,
        }
        return score


__all__ = ["EasyGrader", "MediumGrader", "HardGrader"]
