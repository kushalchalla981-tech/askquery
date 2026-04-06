# Text-to-SQL Environment Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DB_PATH=/app/database/sample.db \
    ENV_NAME=text-to-sql \
    MAX_CONCURRENT_ENVS=64 \
    HOST=0.0.0.0 \
    PORT=7860

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY openenv.yaml .
COPY models.py .
COPY sql_env.py .
COPY database.py .
COPY grader.py .
COPY inference.py .
COPY database/ ./database/
COPY tasks/ ./tasks/
COPY server/ ./server/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose port for HuggingFace Spaces
EXPOSE 7860

# Set entry point to run inference by default
ENTRYPOINT ["python", "inference.py"]