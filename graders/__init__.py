"""Grader definitions for OpenEnv hackathon validation.

This module exposes grader functions that the validator checks.
Each task must have an associated grader.
"""

import grader as grading_module


# Grader functions exposed for validation
def grade_sql_query(predicted_results: list, expected_results: list) -> float:
    """Grade SQL query execution results.

    Returns score in range (0.0, 1.0) - strictly between 0 and 1.
    """
    return grading_module.grade_result(predicted_results, expected_results)


# Registry of graders per task type
GRADERS = {
    "execution_based": grade_sql_query,
}


__all__ = ["grade_sql_query", "GRADERS"]
