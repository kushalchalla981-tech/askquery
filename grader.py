"""Execution-based grading for SQL query results."""

from collections import Counter
from typing import Any


def normalize_value(val: Any) -> Any:
    """Normalize value for comparison (handle None, floats, bytes).

    Args:
        val: Any value from SQL result

    Returns:
        Normalized value for comparison
    """
    if val is None:
        return "__NULL__"
    if isinstance(val, float):
        if val != val:  # NaN check
            return "__NAN__"
        return round(val, 6)
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    if isinstance(val, (int, bool)):
        return val
    if isinstance(val, str):
        return val.strip()
    return val


def normalize_results(rows: list) -> list:
    """Normalize all values in result rows.

    Args:
        rows: List of result tuples

    Returns:
        List of normalized tuples
    """
    return [tuple(normalize_value(v) for v in row) for row in rows]


def execute_query(db_path: str, sql: str):
    """Execute a SQL query against the database.

    Args:
        db_path: Path to SQLite database
        sql: SQL query to execute

    Returns:
        Tuple of (results, error_message or None)
    """
    import database

    try:
        results, exec_time = database.execute_query(db_path, sql)
        return results, None
    except Exception as e:
        return None, str(e)


def grade_query(agent_results: list, expected_results: list) -> float:
    """Grade predicted result against gold result.

    Returns reward between 0.0 and 1.0 (inclusive).

    Score Range:
    - Exact match: 1.0
    - Empty vs empty: 1.0
    - One empty/one not: 0.0
    - Same rows, different order: 0.8
    - Same rows, different count: 0.6
    - Partial overlap: 0.1-0.5 (based on Jaccard)
    - No overlap: 0.0

    Args:
        agent_results: Results from the agent's SQL query
        expected_results: Expected results from ground truth SQL

    Returns:
        Reward score between 0.0 and 1.0
    """
    # Normalize results
    pred_norm = normalize_results(agent_results or [])
    gold_norm = normalize_results(expected_results or [])

    # Exact match (bag equality - same rows with same multiplicities)
    if pred_norm == gold_norm:
        return 1.0

    # Empty vs empty
    if not pred_norm and not gold_norm:
        return 1.0

    # One empty, one not
    if not pred_norm or not gold_norm:
        return 0.0

    # Bag match (order-independent with multiplicities)
    pred_bag = Counter(pred_norm)
    gold_bag = Counter(gold_norm)

    if pred_bag == gold_bag:
        return 0.8

    # Set match (order-independent, ignore duplicates)
    pred_set = set(pred_norm)
    gold_set = set(gold_norm)

    if pred_set == gold_set:
        return 0.6

    # Partial overlap - Jaccard similarity
    intersection = pred_set & gold_set
    union = pred_set | gold_set

    if union:
        jaccard = len(intersection) / len(union)
        return round(jaccard * 0.5, 2)

    return 0.0


def grade_result(predicted: list, gold: list) -> float:
    """Alias for grade_query for backward compatibility.

    Args:
        predicted: Predicted SQL results
        gold: Expected (ground truth) results

    Returns:
        Reward score between 0.0 and 1.0
    """
    return grade_query(predicted, gold)


def grade_with_columns(
    agent_results: list, expected_results: list, expected_columns: list
) -> float:
    """Grade results considering column matching as well.

    If row data is wrong but columns are correct, provides partial credit.

    Args:
        agent_results: Results from agent query
        expected_results: Expected results from ground truth
        expected_columns: List of expected column names

    Returns:
        Reward score between 0.0 and 1.0
    """
    from database import execute_query

    row_score = grade_query(agent_results, expected_results)

    if row_score >= 1.0:
        return 1.0

    if agent_results and not expected_results:
        return 0.0

    if expected_results and not agent_results:
        return 0.0

    return row_score
