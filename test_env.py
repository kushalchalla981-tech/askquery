#!/usr/bin/env python3
"""Simple test script to verify the environment works in Docker."""

import os
import sys

print("[START]")

# Test 1: Import all modules
print("Testing imports...")
try:
    from models import SQLAction, SQLObservation, SQLState
    from sql_env import SQLQueryEnv
    from database import execute_query, validate_sql
    from grader import grade_query

    print("  All imports OK")
except Exception as e:
    print(f"  Import error: {e}")
    print("[END] error=import_failed")
    sys.exit(1)

# Test 2: Create environment and run a simple episode
print("Testing environment...")
try:
    env = SQLQueryEnv()
    obs = env.reset()
    print(f"  Reset OK - Question: {obs.question[:50]}...")

    # Test with a simple SQL query
    action = SQLAction(sql_query="SELECT * FROM customers LIMIT 3")
    result = env.step(action)
    print(f"  Step OK - Reward: {result.reward}")

except Exception as e:
    print(f"  Environment error: {e}")
    import traceback

    traceback.print_exc()
    print("[END] error=environment_failed")
    sys.exit(1)

# Test 3: Test database
print("Testing database...")
try:
    result, exec_time = execute_query(
        "database/sample.db", "SELECT COUNT(*) FROM customers"
    )
    print(f"  Database OK - {result[0][0]} customers")
except Exception as e:
    print(f"  Database error: {e}")
    print("[END] error=database_failed")
    sys.exit(1)

print("[END] final_score=1.0")
print("All tests passed!")
