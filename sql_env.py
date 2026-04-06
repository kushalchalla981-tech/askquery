"""Main environment class for Text-to-SQL OpenEnv environment.

This module implements the Gymnasium-style environment interface with:
- reset() - Initialize episode with a task
- step() - Execute SQL query and return observation with reward
- state() - Return current episode state
"""

import os
import uuid
from typing import Optional

from models import SQLAction, SQLObservation, SQLState
import database
import grader
from tasks import get_random_task


# Default database path
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "database", "sample.db")


class SQLQueryEnv:
    """Text-to-SQL environment with execution-based grading.

    This environment:
    1. Loads a random task on reset()
    2. Executes the agent's SQL query on step()
    3. Grades the result against ground truth
    4. Returns observation with reward
    """

    def __init__(self, db_path: str = None):
        """Initialize the environment.

        Args:
            db_path: Path to SQLite database (defaults to database/sample.db)
        """
        self._db_path = db_path or os.getenv("DB_PATH", DEFAULT_DB_PATH)
        self._state = SQLState()
        self._current_task = None
        self._expected_result = None
        self._schema_info = None

    def reset(
        self, seed: Optional[int] = None, episode_id: Optional[str] = None, **kwargs
    ) -> SQLObservation:
        """Initialize episode with random task.

        Args:
            seed: Random seed for reproducibility
            episode_id: Unique episode identifier (generated if not provided)
            task: Optional task dict to use instead of random selection
            difficulty: Optional difficulty level ('easy', 'medium', 'hard')

        Returns:
            SQLObservation with question, schema, and feedback
        """
        # Set up state
        self._state = SQLState(
            episode_id=episode_id or str(uuid.uuid4()),
            step_count=0,
        )

        # Get task - either from kwargs or random
        task = kwargs.get("task")
        if task is None:
            difficulty = kwargs.get("difficulty")
            self._current_task = get_random_task(difficulty=difficulty)
        else:
            self._current_task = task

        # Store task info in state
        self._state.current_task_id = self._current_task["id"]
        self._state.difficulty = self._current_task["difficulty"]

        # Get expected result by executing ground truth SQL
        try:
            result, _ = database.execute_query(
                self._db_path, self._current_task["ground_truth_sql"]
            )
            self._expected_result = result
        except Exception as e:
            # If ground truth fails, store empty result
            self._expected_result = []

        # Get schema info for observation
        self._schema_info = database.get_schema_info(self._db_path)

        return SQLObservation(
            done=False,
            reward=None,
            question=self._current_task["question"],
            schema_info=self._schema_info,
            feedback="Ready. Execute a SQL query to answer the question.",
        )

    def step(
        self, action: SQLAction, timeout_s: Optional[float] = 5.0, **kwargs
    ) -> SQLObservation:
        """Execute SQL query and return observation with reward.

        Args:
            action: SQLAction containing sql_query
            timeout_s: Query timeout in seconds

        Returns:
            SQLObservation with feedback, reward, and done status
        """
        self._state.step_count += 1
        self._state.attempts += 1

        # Validate SQL first
        validation = database.validate_sql(action.sql_query)
        if not validation["valid"]:
            return SQLObservation(
                done=True,
                reward=0.0,
                question=self._current_task["question"],
                schema_info="",
                feedback=f"SQL validation error: {validation['errors']}",
                error=validation["errors"][0]
                if validation["errors"]
                else "Unknown error",
                metadata={"step": self._state.step_count},
            )

        # Execute query
        try:
            result, exec_time = database.execute_query(
                self._db_path, action.sql_query, timeout_s=timeout_s
            )
        except Exception as e:
            return SQLObservation(
                done=True,
                reward=0.0,
                question=self._current_task["question"],
                schema_info="",
                feedback=f"SQL execution error: {str(e)}",
                error=str(e),
                metadata={"step": self._state.step_count, "execution_time_ms": 0},
            )

        # Grade result
        reward = grader.grade_result(result, self._expected_result)

        # Format feedback
        row_count = len(result) if result else 0
        feedback = f"Query executed in {exec_time:.2f}ms. Returned {row_count} row(s)."

        return SQLObservation(
            done=True,
            reward=reward,
            question=self._current_task["question"],
            schema_info="",
            feedback=feedback,
            metadata={
                "step": self._state.step_count,
                "execution_time_ms": exec_time,
                "row_count": row_count,
            },
        )

    @property
    def state(self) -> SQLState:
        """Return current episode state.

        Returns:
            SQLState with current task, difficulty, step count
        """
        return self._state

    def get_task(self) -> Optional[dict]:
        """Get the current task.

        Returns:
            Current task dictionary or None if not initialized
        """
        return self._current_task

    def get_expected_result(self) -> list:
        """Get the expected result for the current task.

        Returns:
            List of tuples representing expected query results
        """
        return self._expected_result or []


# Factory function for OpenEnv
def create_env():
    """Factory function for OpenEnv - creates new environment instance per session.

    Returns:
        New SQLQueryEnv instance
    """
    db_path = os.getenv("DB_PATH", DEFAULT_DB_PATH)
    return SQLQueryEnv(db_path=db_path)


# Alias for compatibility
create_environment = create_env
