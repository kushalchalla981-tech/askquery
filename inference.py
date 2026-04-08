#!/usr/bin/env python3
"""Baseline inference script for Text-to-SQL OpenEnv environment.

This script:
1. Loads environment variables for API configuration
2. Creates an OpenAI-compatible client
3. Runs episodes against the SQL environment
4. Outputs results in the required format

Environment Variables (in order of priority):
- OPENAI_API_KEY: OpenAI API key
- HF_TOKEN: HuggingFace token for Inference API
- API_BASE_URL: Base URL for API (defaults to HF Inference API)
- MODEL_NAME: Model name to use

Output Format:
  [START]
  [STEP] step=X action=Y reward=Z
  [END] final_score=X

Runtime target: < 20 minutes on vcpu=2, memory=8gb
"""

import os
import sys
import json
from typing import Optional

# Configuration
DEFAULT_API_BASE = "https://router.huggingface.co/models"
DEFAULT_MODEL = "meta-llama/Llama-3.2-1B-Instruct"
USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"


def get_client():
    """Create OpenAI-compatible client or local model based on environment variables.

    Returns:
        Either (OpenAI client, model_name) or (None, local_model_pipeline)
    """
    global USE_LOCAL_MODEL

    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")
    api_base = os.getenv("API_BASE_URL")
    model_name = os.getenv("MODEL_NAME")

    if not model_name:
        model_name = DEFAULT_MODEL

    if USE_LOCAL_MODEL:
        from transformers import pipeline

        pipe = pipeline(
            "text-generation", model=model_name, torch_dtype="auto", device_map="auto"
        )
        return None, pipe

    if not api_key:
        return None, None

    if not api_base:
        api_base = DEFAULT_API_BASE

    from openai import OpenAI

    if "openai" not in api_base.lower() and api_base != DEFAULT_API_BASE:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
    else:
        client = OpenAI(
            api_key=api_key,
            base_url="https://router.huggingface.co/v1",
        )

    return client, model_name


def build_prompt(question: str, schema: str) -> str:
    """Build the prompt for the SQL generation model.

    Args:
        question: Natural language question
        schema: Database schema information

    Returns:
        Formatted prompt for the model
    """
    return f"""You are a SQL expert. Given the following database schema and question, 
write a correct SQLite SQL query to answer the question.

Database Schema:
{schema}

Question: {question}

Write only the SQL query, nothing else:"""


def call_model(client, model: str, prompt: str) -> str:
    """Call the model to generate a SQL query.

    Args:
        client: OpenAI-compatible client (or None if using local model)
        model: Model name (or pipeline for local model)
        prompt: Formatted prompt

    Returns:
        Generated SQL query string
    """
    try:
        if client is None:
            output = model(
                prompt,
                max_new_tokens=500,
                temperature=0.1,
                do_sample=True,
            )
            content = output[0]["generated_text"]
            if prompt in content:
                content = content[len(prompt) :]
            return content.strip()
        else:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500,
            )

            content = response.choices[0].message.content
            if content is None:
                return ""
            return content.strip()

    except Exception as e:
        print(f"Error calling model: {type(e).__name__}", file=sys.stderr)
        return ""


def extract_sql(response: str) -> str:
    """Extract SQL query from model response.

    Handles common formats like ```sql ... ``` blocks.

    Args:
        response: Model response string

    Returns:
        Extracted SQL query
    """
    if not response:
        return ""

    response = response.strip()

    if response.startswith("```sql"):
        response = response[6:]
        if response.startswith("\n"):
            response = response[1:]
        if response.endswith("```"):
            response = response[:-3]
    elif response.startswith("```"):
        response = response[3:]
        if response.startswith("\n"):
            response = response[1:]
        if response.endswith("```"):
            response = response[:-3]
    elif response.startswith("sql\n"):
        response = response[4:]
    elif response.startswith("SQL\n"):
        response = response[4:]

    response = response.strip()

    if not response or response == "?" or response == "?" * len(response):
        return ""

    if response.startswith("SELECT") or response.startswith("select"):
        return response

    for prefix in ["Query:", "SQL:", "The query:", "Answer:"]:
        if response.startswith(prefix):
            response = response[len(prefix) :].strip()
            break

    return response.strip()


def run_episode(env, difficulty: str = None) -> tuple[str, float]:
    """Run a single episode in the environment.

    Args:
        env: SQLQueryEnv instance
        difficulty: Optional difficulty level

    Returns:
        Tuple of (sql_query, reward)
    """
    obs = env.reset(difficulty=difficulty)

    prompt = build_prompt(obs.question, obs.schema_info)
    client, model = get_client()

    if client is None and model is None:
        return "SELECT 1", 0.0

    response = call_model(client, model, prompt)
    sql = extract_sql(response)

    if not sql:
        sql = "SELECT 1"

    from models import SQLAction

    action = SQLAction(sql_query=sql)
    result = env.step(action)

    return sql, result.reward or 0.0


def run_inference(
    num_episodes: int = 18, difficulties: list = None, output_format: str = "text"
) -> dict:
    """Run inference across multiple episodes.

    Args:
        num_episodes: Number of episodes to run
        difficulties: List of difficulties to cycle through
        output_format: 'text' or 'json'

    Returns:
        Dictionary with results and statistics
    """
    from sql_env import SQLQueryEnv

    if difficulties is None:
        difficulties = ["easy", "medium", "hard"]

    # Create environment
    env = SQLQueryEnv()

    results = []
    total_reward = 0.0

    print("[START]")

    for i in range(num_episodes):
        difficulty = difficulties[i % len(difficulties)]

        try:
            sql, reward = run_episode(env, difficulty=difficulty)

            print(f"[STEP] step={i + 1} action={sql[:100]}... reward={reward:.2f}")

            results.append(
                {
                    "step": i + 1,
                    "difficulty": difficulty,
                    "sql": sql,
                    "reward": reward,
                }
            )

            total_reward += reward

        except Exception as e:
            print(f"[STEP] step={i + 1} action=ERROR reward=0.0", file=sys.stderr)
            print(f"Error: {e}", file=sys.stderr)

            results.append(
                {
                    "step": i + 1,
                    "difficulty": difficulty,
                    "sql": "",
                    "reward": 0.0,
                    "error": str(e),
                }
            )

    avg_reward = total_reward / num_episodes if num_episodes > 0 else 0.0

    print(f"[END] final_score={avg_reward:.2f}")

    return {
        "results": results,
        "total_reward": total_reward,
        "avg_reward": avg_reward,
        "num_episodes": num_episodes,
    }


def main():
    """Main entry point for inference script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run inference on Text-to-SQL environment"
    )
    parser.add_argument(
        "--episodes",
        "-n",
        type=int,
        default=18,
        help="Number of episodes to run (default: 18)",
    )
    parser.add_argument(
        "--output",
        "-o",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--difficulty",
        "-d",
        choices=["easy", "medium", "hard", "mixed"],
        default="mixed",
        help="Difficulty level (default: mixed)",
    )

    args = parser.parse_args()

    # Determine difficulties
    if args.difficulty == "mixed":
        difficulties = ["easy", "medium", "hard"]
    else:
        difficulties = [args.difficulty]

    # Run inference
    results = run_inference(
        num_episodes=args.episodes, difficulties=difficulties, output_format=args.output
    )

    # Print JSON output if requested
    if args.output == "json":
        print(json.dumps(results, indent=2))

    # Return exit code based on performance
    if results["avg_reward"] >= 0.7:
        return 0
    elif results["avg_reward"] >= 0.4:
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
