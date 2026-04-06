"""Task definitions for Text-to-SQL OpenEnv environment."""

from tasks.easy_tasks import EASY_TASKS
from tasks.medium_tasks import MEDIUM_TASKS
from tasks.hard_tasks import HARD_TASKS
import random


ALL_TASKS = {"easy": EASY_TASKS, "medium": MEDIUM_TASKS, "hard": HARD_TASKS}


def get_task(difficulty: str, task_id: str):
    """Retrieve a specific task by difficulty and task ID.

    Args:
        difficulty: One of 'easy', 'medium', or 'hard'
        task_id: The task identifier (e.g., 'easy_001')

    Returns:
        The task dictionary, or None if not found
    """
    if difficulty not in ALL_TASKS:
        return None
    for task in ALL_TASKS[difficulty]:
        if task["id"] == task_id:
            return task
    return None


def get_random_task(difficulty: str = None):
    """Get a random task, optionally filtered by difficulty.

    Args:
        difficulty: Optional difficulty level ('easy', 'medium', or 'hard')

    Returns:
        A random task dictionary
    """
    if difficulty is None:
        difficulty = random.choice(["easy", "medium", "hard"])
    if difficulty not in ALL_TASKS:
        difficulty = random.choice(list(ALL_TASKS.keys()))
    return random.choice(ALL_TASKS[difficulty])


def get_all_tasks_by_difficulty(difficulty: str):
    """Get all tasks for a given difficulty level.

    Args:
        difficulty: One of 'easy', 'medium', or 'hard'

    Returns:
        List of task dictionaries for that difficulty
    """
    return ALL_TASKS.get(difficulty, [])


__all__ = [
    "ALL_TASKS",
    "EASY_TASKS",
    "MEDIUM_TASKS",
    "HARD_TASKS",
    "get_task",
    "get_random_task",
    "get_all_tasks_by_difficulty",
]
