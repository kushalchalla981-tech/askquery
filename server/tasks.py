"""Task registry for OpenEnv hackathon validation.

This module defines the task structure that the validator checks.
Each task must be associated with a grader for validation.
"""

from tasks import ALL_TASKS, EASY_TASKS, MEDIUM_TASKS, HARD_TASKS


# Task definitions with grader association
# The validator checks that these tasks have graders defined
TASK_REGISTRY = {
    "easy": [
        {
            "id": task["id"],
            "difficulty": "easy",
            "question": task["question"],
            "grader": "execution_based",
            "grader_module": "graders",
            "grader_function": "grade_sql_query",
        }
        for task in EASY_TASKS
    ],
    "medium": [
        {
            "id": task["id"],
            "difficulty": "medium",
            "question": task["question"],
            "grader": "execution_based",
            "grader_module": "graders",
            "grader_function": "grade_sql_query",
        }
        for task in MEDIUM_TASKS
    ],
    "hard": [
        {
            "id": task["id"],
            "difficulty": "hard",
            "question": task["question"],
            "grader": "execution_based",
            "grader_module": "graders",
            "grader_function": "grade_sql_query",
        }
        for task in HARD_TASKS
    ],
}


def get_task_by_id(task_id: str):
    """Get task by ID from the registry.

    Args:
        task_id: Task identifier (e.g., 'easy_001')

    Returns:
        Task dict or None if not found
    """
    for difficulty_tasks in TASK_REGISTRY.values():
        for task in difficulty_tasks:
            if task["id"] == task_id:
                return task
    return None


def get_all_task_ids():
    """Get all task IDs from the registry.

    Returns:
        List of all task IDs
    """
    return [task["id"] for tasks in TASK_REGISTRY.values() for task in tasks]


def get_tasks_with_graders():
    """Get all tasks that have graders defined.

    This is what the validator checks - at least 3 tasks with graders.

    Returns:
        List of task dicts with grader information
    """
    tasks_with_graders = []
    for difficulty_tasks in TASK_REGISTRY.values():
        tasks_with_graders.extend(difficulty_tasks)
    return tasks_with_graders


# Export for validator
__all__ = [
    "TASK_REGISTRY",
    "get_task_by_id",
    "get_all_task_ids",
    "get_tasks_with_graders",
    "ALL_TASKS",
    "EASY_TASKS",
    "MEDIUM_TASKS",
    "HARD_TASKS",
]
