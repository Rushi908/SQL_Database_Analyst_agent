from typing import Any

from langchain.tools import tool
from sqlalchemy import create_engine, inspect, text


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = "sqlite:///sql_agent_demo.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# ============================================================
# TOOL 1: GET DATABASE TABLES
# ============================================================

@tool
def get_database_schema() -> str:
    """
    Get the complete database schema.

    Returns:
        List of tables, columns, data types, primary keys,
        and foreign key relationships.
    """

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if not tables:
        return "No tables found in the database."

    schema = []

    for table_name in tables:

        columns = inspector.get_columns(table_name)

        primary_key = inspector.get_pk_constraint(
            table_name
        )

        foreign_keys = inspector.get_foreign_keys(
            table_name
        )

        table_info = {
            "table_name": table_name,
            "columns": [],
            "primary_keys": primary_key.get(
                "constrained_columns",
                [],
            ),
            "foreign_keys": [],
        }

        for column in columns:

            table_info["columns"].append(
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                }
            )

        for foreign_key in foreign_keys:

            table_info["foreign_keys"].append(
                {
                    "columns": foreign_key[
                        "constrained_columns"
                    ],
                    "referred_table": foreign_key[
                        "referred_table"
                    ],
                    "referred_columns": foreign_key[
                        "referred_columns"
                    ],
                }
            )

        schema.append(table_info)

    return str(schema)


# ============================================================
# TOOL 2: GET SPECIFIC TABLE SCHEMA
# ============================================================

@tool
def get_table_schema(table_name: str) -> str:
    """
    Get detailed schema information for a specific table.

    Args:
        table_name: Name of the database table.
    """

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if table_name not in tables:

        return (
            f"Table '{table_name}' does not exist. "
            f"Available tables: {tables}"
        )

    columns = inspector.get_columns(
        table_name
    )

    primary_key = inspector.get_pk_constraint(
        table_name
    )

    foreign_keys = inspector.get_foreign_keys(
        table_name
    )

    result = {
        "table_name": table_name,
        "columns": [],
        "primary_keys": primary_key.get(
            "constrained_columns",
            [],
        ),
        "foreign_keys": [],
    }

    for column in columns:

        result["columns"].append(
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
            }
        )

    for foreign_key in foreign_keys:

        result["foreign_keys"].append(
            {
                "columns": foreign_key[
                    "constrained_columns"
                ],
                "referred_table": foreign_key[
                    "referred_table"
                ],
                "referred_columns": foreign_key[
                    "referred_columns"
                ],
            }
        )

    return str(result)


# ============================================================
# TOOL 3: EXECUTE READ-ONLY SQL
# ============================================================

@tool
def execute_sql(query: str) -> str:
    """
    Execute a READ-ONLY SQL query against the database.

    Only SELECT and WITH queries are allowed.

    Args:
        query: SQL query to execute.
    """

    query_clean = query.strip()

    if not query_clean:

        return "ERROR: SQL query is empty."

    query_lower = query_clean.lower()

    # --------------------------------------------------------
    # Only SELECT / WITH
    # --------------------------------------------------------

    if not (
        query_lower.startswith("select")
        or query_lower.startswith("with")
    ):

        return (
            "ERROR: Only SELECT and WITH queries "
            "are allowed."
        )

    # --------------------------------------------------------
    # Block dangerous operations
    # --------------------------------------------------------

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
        "merge",
        "grant",
        "revoke",
        "attach",
        "detach",
    ]

    for keyword in blocked_keywords:

        if keyword in query_lower:

            return (
                f"ERROR: Forbidden SQL operation "
                f"detected: {keyword}"
            )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text(query_clean)
            )

            rows = result.fetchall()

            columns = list(result.keys())

            # Convert SQL rows into dictionaries
            data = []

            for row in rows:

                row_data = {}

                for index, column in enumerate(columns):

                    value = row[index]

                    # Convert non-JSON-friendly values
                    if hasattr(value, "isoformat"):

                        value = value.isoformat()

                    row_data[column] = value

                data.append(row_data)

            # ------------------------------------------------
            # No results
            # ------------------------------------------------

            if not data:

                return "Query executed successfully. No rows found."

            # ------------------------------------------------
            # Limit result size returned to LLM
            # ------------------------------------------------

            max_rows = 100

            if len(data) > max_rows:

                data = data[:max_rows]

                return (
                    f"Query returned more than {max_rows} "
                    f"rows. Showing first {max_rows} rows:\n"
                    f"{data}"
                )

            return str(data)

    except Exception as exc:

        return (
            f"SQL execution error: {str(exc)}"
        )


# ============================================================
# TOOL LIST
# ============================================================

database_tools = [
    get_database_schema,
    get_table_schema,
    execute_sql,
]