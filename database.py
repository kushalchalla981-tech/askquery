"""SQL Sandbox - Read-only SQLite database with execution and validation."""

import sqlite3
import os
from typing import Optional
import sqlglot
from sqlglot import exp

# Configuration
MAX_ROWS = 1000
DEFAULT_TIMEOUT = 5.0


def get_readonly_connection(db_path: str) -> sqlite3.Connection:
    """Create a read-only SQLite connection with security PRAGMAs."""
    conn = sqlite3.connect(
        f"file:{db_path}?mode=ro",
        uri=True,
        timeout=5.0,
    )

    # Defense in depth: SQLite-level read-only enforcement
    conn.execute("PRAGMA query_only = ON")

    # No temp files on disk
    conn.execute("PRAGMA temp_store = MEMORY")

    # Disable extensions
    conn.enable_load_extension(False)

    return conn


def execute_query(
    db_path: str,
    sql: str,
    timeout_s: Optional[float] = DEFAULT_TIMEOUT,
    max_rows: int = MAX_ROWS,
) -> tuple[list, float]:
    """Execute SQL query and return (results, execution_time_ms).

    Args:
        db_path: Path to the SQLite database
        sql: SQL query to execute
        timeout_s: Query timeout in seconds
        max_rows: Maximum number of rows to return

    Returns:
        Tuple of (results, execution_time_ms)
    """
    import time

    conn = get_readonly_connection(db_path)
    start = time.perf_counter()

    try:
        cursor = conn.cursor()
        cursor.execute(sql)

        # Apply row limit for safety
        results = cursor.fetchmany(max_rows + 1)
        if len(results) > max_rows:
            results = results[:max_rows]
            truncated = True
        else:
            truncated = False

    finally:
        conn.close()

    exec_time = (time.perf_counter() - start) * 1000

    if truncated:
        return results, exec_time

    return results, exec_time


def validate_sql(sql: str) -> dict:
    """Validate SQL is safe to execute. Returns {valid: bool, errors: list}.

    Checks:
    - SQL parses correctly (SQLGlot)
    - Only SELECT statements (no INSERT/UPDATE/DELETE/DROP/etc.)
    - No dangerous functions

    Args:
        sql: SQL query to validate

    Returns:
        Dictionary with 'valid' boolean and 'errors' list
    """
    errors = []

    # Step 1: Parse
    try:
        statements = sqlglot.parse(sql, dialect="sqlite")
    except sqlglot.errors.ParseError as e:
        return {"valid": False, "errors": [f"Parse error: {e}"]}

    if not statements or all(s is None for s in statements):
        return {"valid": False, "errors": ["No valid SQL statements found"]}

    # Step 2: Check statement type (only SELECT allowed)
    valid_stmts = [s for s in statements if s is not None]
    if len(valid_stmts) > 1:
        return {"valid": False, "errors": ["Multiple statements not allowed"]}

    stmt = valid_stmts[0]
    if not isinstance(stmt, (exp.Select, exp.With)):
        return {
            "valid": False,
            "errors": [f"Only SELECT statements allowed, got {type(stmt).__name__}"],
        }

    # Step 3: Check for dangerous functions
    dangerous_funcs = {"load_extension", "readfile", "writefile"}
    for func in stmt.find_all(exp.Anonymous):
        if func.this.lower() in dangerous_funcs:
            errors.append(f"Dangerous function: {func.this}")

    # Step 4: Check for blocked statement types in any subqueries
    blocked = {
        exp.Insert,
        exp.Update,
        exp.Delete,
        exp.Drop,
        exp.Create,
        exp.Alter,
        exp.Attach,
    }
    for node in stmt.walk():
        if type(node) in blocked:
            errors.append(f"Blocked statement: {type(node).__name__}")

    return {"valid": len(errors) == 0, "errors": errors}


def get_schema_info(db_path: str) -> str:
    """Extract schema information for context.

    Args:
        db_path: Path to the SQLite database

    Returns:
        Formatted string with table and column information
    """
    conn = get_readonly_connection(db_path)
    cursor = conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = cursor.fetchall()
    cursor.close()

    schema_lines = []
    for table_name, create_stmt in tables:
        schema_lines.append(f"Table: {table_name}")

        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            col_name = col[1]
            col_type = col[2]
            pk = "PRIMARY KEY" if col[5] else ""
            schema_lines.append(f"  - {col_name} ({col_type}) {pk}".strip())

        schema_lines.append("")

    conn.close()
    return "\n".join(schema_lines)


def get_table_row_counts(db_path: str) -> dict:
    """Get row counts for all tables.

    Args:
        db_path: Path to the SQLite database

    Returns:
        Dictionary mapping table names to row counts
    """
    conn = get_readonly_connection(db_path)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    row_counts = {}
    for table in tables:
        cursor = conn.execute(f'SELECT COUNT(*) FROM "{table}"')
        row_counts[table] = cursor.fetchone()[0]

    conn.close()
    return row_counts
