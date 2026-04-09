"""Server module for Text-to-SQL OpenEnv environment.

This module provides the OpenEnv factory pattern for serving the environment
via HTTP/WebSocket. Uses openenv-core's create_app for proper session isolation.
"""

import os
from typing import Optional

# Configuration
DB_PATH = os.getenv(
    "DB_PATH", os.path.join(os.path.dirname(__file__), "..", "database", "sample.db")
)
ENV_NAME = os.getenv("ENV_NAME", "text-to-sql")
MAX_CONCURRENT_ENVS = int(os.getenv("MAX_CONCURRENT_ENVS", "64"))


def get_env_module():
    """Lazy load environment module."""
    from sql_env import create_env, SQLQueryEnv

    return create_env, SQLQueryEnv


def get_models():
    """Lazy load models."""
    from models import SQLAction, SQLObservation

    return SQLAction, SQLObservation


def create_app():
    """Create and configure the OpenAPI application.

    Uses openenv-core's create_app factory to provide:
    - HTTP/WebSocket endpoints for reset/step/state
    - Session isolation via factory function
    - Health checks and validation

    Returns:
        Configured FastAPI application
    """
    try:
        from openenv.core.env_server import create_app as openenv_create_app
        from sql_env import create_env
        from models import SQLAction, SQLObservation

        # Create the app with factory function for session isolation
        app = openenv_create_app(
            create_env,  # Factory function, not instance
            SQLAction,
            SQLObservation,
            env_name=ENV_NAME,
            max_concurrent_envs=MAX_CONCURRENT_ENVS,
        )

        return app

    except ImportError:
        # Fallback for development without openenv-core
        return _create_dev_app()


def _create_dev_app():
    """Create a minimal development app when openenv-core is not available.

    This provides a basic FastAPI app for local development.
    """
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse

    app = FastAPI(title="Text-to-SQL Environment")

    @app.get("/health")
    async def health():
        return {"status": "healthy", "env": ENV_NAME}

    @app.get("/tasks")
    async def get_tasks():
        """Return all tasks with grader information."""
        try:
            from tasks import ALL_TASKS

            all_tasks = []
            for difficulty, tasks in ALL_TASKS.items():
                for task in tasks:
                    all_tasks.append(
                        {
                            "id": task["id"],
                            "difficulty": difficulty,
                            "question": task["question"],
                            "grader": "execution_based",
                        }
                    )
            return {"tasks": all_tasks, "total": len(all_tasks)}
        except Exception as e:
            return {"tasks": [], "total": 0, "error": str(e)}

    @app.post("/reset")
    async def reset(episode_id: Optional[str] = None, difficulty: Optional[str] = None):
        try:
            from sql_env import create_env

            env = create_env()
            obs = env.reset(episode_id=episode_id, difficulty=difficulty)
            return obs.model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/step")
    async def step(action: dict):
        try:
            from sql_env import create_env
            from models import SQLAction

            sql_query = action.get("sql_query", "")
            env = create_env()
            env.reset(episode_id=action.get("episode_id"))
            sql_action = SQLAction(sql_query=sql_query)
            obs = env.step(sql_action)
            return obs.model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/state")
    async def state():
        try:
            from sql_env import create_env

            env = create_env()
            return env.state.model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


# For direct execution
def main():
    """Run the server with uvicorn."""
    import uvicorn

    app = create_app()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "7860"))

    print(f"Starting Text-to-SQL environment on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()


# Expose key attributes for OpenEnv compatibility
SUPPORTS_CONCURRENT_SESSIONS = True
