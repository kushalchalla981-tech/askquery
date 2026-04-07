"""Server module for Text-to-SQL OpenEnv environment.

This module provides the OpenEnv factory pattern for serving the environment
via HTTP/WebSocket. Uses openenv-core's create_app for proper session isolation.
"""

import os
from typing import Optional

# Import environment components
from sql_env import create_env, SQLQueryEnv
from models import SQLAction, SQLObservation


# Configuration
DB_PATH = os.getenv(
    "DB_PATH", os.path.join(os.path.dirname(__file__), "database", "sample.db")
)
ENV_NAME = os.getenv("ENV_NAME", "text-to-sql")
MAX_CONCURRENT_ENVS = int(os.getenv("MAX_CONCURRENT_ENVS", "64"))


def create_app():
    """Create and configure the OpenEnv application.

    Uses openenv-core's create_app factory to provide:
    - HTTP/WebSocket endpoints for reset/step/state
    - Session isolation via factory function
    - Health checks and validation

    Returns:
        Configured FastAPI application
    """
    try:
        from openenv.core.env_server import create_app as openenv_create_app

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
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="Text-to-SQL Environment (Dev Mode)")

    @app.get("/health")
    async def health():
        return {"status": "healthy", "env": ENV_NAME}

    @app.post("/reset")
    async def reset(episode_id: Optional[str] = None, difficulty: Optional[str] = None):
        env = create_env()
        obs = env.reset(episode_id=episode_id, difficulty=difficulty)
        return obs.model_dump()

    @app.post("/step")
    async def step(sql_query: str, episode_id: Optional[str] = None):
        env = create_env()
        env.reset(episode_id=episode_id)
        action = SQLAction(sql_query=sql_query)
        obs = env.step(action)
        return obs.model_dump()

    @app.get("/state")
    async def state():
        env = create_env()
        return env.state.model_dump()

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
