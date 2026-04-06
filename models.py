"""Pydantic models for the Text-to-SQL OpenEnv environment."""

from typing import Optional
from pydantic import BaseModel, Field


class SQLAction(BaseModel):
    """Action model for the SQL query generation environment.

    The agent provides a SQL query as the action.
    """

    model_config = {"extra": "forbid"}

    sql_query: str = Field(description="SQL query to execute against the database")


class SQLObservation(BaseModel):
    """Observation model for the SQL query generation environment.

    Returns the current state including question, schema, and feedback.
    """

    model_config = {"extra": "forbid"}

    question: str = Field(
        description="The natural language question to answer with SQL"
    )
    schema_info: str = Field(description="Database schema information for context")
    feedback: str = Field(
        description="Execution result or error message from previous step"
    )
    error: Optional[str] = Field(
        default=None, description="SQLite error message if query failed"
    )
    done: bool = Field(default=False, description="Whether the episode is complete")
    reward: Optional[float] = Field(
        default=None, description="Reward score from 0.0 to 1.0 based on query accuracy"
    )
    metadata: dict = Field(default_factory=dict, description="Additional metadata")


class SQLState(BaseModel):
    """State model for tracking episode progress.

    Tracks the current task, difficulty, and step count.
    """

    model_config = {"extra": "allow"}

    episode_id: Optional[str] = Field(
        default=None, description="Unique episode identifier"
    )
    step_count: int = Field(
        default=0, description="Number of steps taken in the current episode"
    )
    current_task_id: str = Field(
        default="", description="Which task is currently active"
    )
    difficulty: str = Field(
        default="", description="Current difficulty level: easy, medium, or hard"
    )
    attempts: int = Field(
        default=0, description="Number of SQL attempts made in current episode"
    )
