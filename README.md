---
title: askquery
emoji: 🗄️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Text-to-SQL OpenEnv Environment

A natural language to SQL query generation environment for the OpenEnv hackathon.

## Overview

This environment implements a Text-to-SQL task where an agent receives a natural language question about a database and must generate a SQL query to answer it. The environment provides execution-based grading with partial rewards for semantically correct queries.

## Features

- **Read-only SQL Sandbox**: Secure SQLite execution with read-only mode and PRAGMA protections
- **Execution-based Grading**: Tiered rewards (0.0-1.0) based on result accuracy
- **18 Tasks**: 6 easy, 6 medium, 6 hard across different SQL complexities
- **OpenEnv Compatible**: Follows OpenEnv factory pattern for proper session isolation

## Action Space

```python
SQLAction(sql_query: str)
```

The agent provides a SQL query as the action.

## Observation Space

```python
SQLObservation(
    question: str,           # Natural language question
    schema_info: str,        # Database schema for context
    feedback: str,           # Execution result or error
    error: Optional[str],    # SQLite error if failed
    done: bool,              # Episode complete
    reward: Optional[float]  # Score 0.0-1.0
)
```

## State Space

```python
SQLState(
    episode_id: str,      # Unique episode identifier
    step_count: int,      # Steps taken in episode
    current_task_id: str, # Active task
    difficulty: str,      # easy/medium/hard
    attempts: int         # SQL attempts made
)
```

## Task Descriptions

### Easy (6 tasks)
Single-table SELECT with WHERE clause:
- Filter customers by state
- Filter products by category
- Filter orders by status

### Medium (6 tasks)
JOINs, GROUP BY, and Aggregations:
- Total orders per customer
- Average order value by category
- Products sold per state
- Revenue per customer

### Hard (6 tasks)
Subqueries and Window Functions:
- Customers above average spending
- Top 3 products per category
- Orders above median
- Month-over-month growth

## Setup

### Local Development

```bash
# Install dependencies
pip install -e .

# Run inference
python inference.py

# Or start the server
python -m server.app
```

### Docker

```bash
# Build image
docker build -t text-to-sql-env .

# Run container
docker run -p 7860:7860 text-to-sql-env
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_PATH` | `./database/sample.db` | Path to SQLite database |
| `API_BASE_URL` | HuggingFace Inference API | Base URL for LLM API |
| `MODEL_NAME` | `meta-llama/Llama-3.2-1B-Instruct` | Model to use |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `HF_TOKEN` | - | HuggingFace token |
| `PORT` | `7860` | Server port |
| `HOST` | `0.0.0.0` | Server host |

## Output Format

The inference script outputs in this format:

```
[START]
[STEP] step=1 action=SELECT * FROM customers WHERE state='CA' reward=1.00
[STEP] step=2 action=SELECT category, AVG(price) FROM products GROUP BY category reward=0.80
...
[END] final_score=0.85
```

## Grading

Rewards are calculated based on result comparison:

| Score | Description |
|-------|-------------|
| 1.0 | Exact match (bag equality) |
| 0.7-0.9 | Set match (same rows, different order/count) |
| 0.1-0.6 | Partial overlap (Jaccard similarity) |
| 0.0 | No overlap, syntax error, or execution failure |

## Security

The SQL sandbox includes:
- Read-only SQLite connection (`mode=ro` URI)
- `PRAGMA query_only = ON`
- SQLGlot AST validation (SELECT only)
- Execution timeout (5 seconds)
- Row limits (1000 max)

## Baseline Performance

Target scores for baseline model:
- Easy tasks: ~0.8
- Medium tasks: ~0.5
- Hard tasks: ~0.3
- Overall: ~0.5

## Project Structure

```
metahuggie/
├── __init__.py           # Package exports
├── models.py             # Pydantic models
├── sql_env.py            # Main environment class
├── database.py           # SQL sandbox
├── grader.py            # Execution-based grading
├── inference.py          # Baseline inference script
├── server/
│   └── app.py           # OpenEnv server
├── tasks/
│   ├── easy_tasks.py    # 6 easy tasks
│   ├── medium_tasks.py  # 6 medium tasks
│   └── hard_tasks.py    # 6 hard tasks
├── database/
│   ├── sample.db        # SQLite database
│   └── schema.sql       # Schema definition
├── openenv.yaml         # OpenEnv configuration
├── Dockerfile           # Container build
└── pyproject.toml      # Python dependencies
```

## License

MIT