import os

import psycopg2 as pg


def connect_postgres(schema, autocommit=False):
    """Function to create connection with Postgres database"""

    # Defining parameters for connection:
    db_name = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")

    # Modifying database to dev depending on environment:
    if get_environment() == "dev":
        db_name += "-dev"

    # Connecting to database:
    try:
        conn = pg.connect(
            dbname=db_name,
            user=username,
            password=password,
            host=host,
            port=port,
            options=f"-c search_path={schema}",
        )
    except Exception as err:
        raise ConnectionError(f"PostgreSQL connection failed: {str(err)}") from err

    if autocommit:
        conn.set_session(autocommit=autocommit)

    return conn


def get_environment():
    """Function to retrieve current environment based on environment variable"""

    # Value for HOSTING_INSTANCE is "cloud,<env>" e.g.: "cloud,prod"):
    env = os.environ.get("HOSTING_INSTANCE").split(",")[-1]

    print("ENV:::", env)

    return env
