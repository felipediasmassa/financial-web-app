"""Utility functions to initialize database parameters"""

import os

from sqlalchemy import text, MetaData
from sqlalchemy.ext.automap import automap_base

from models.automap_models import MappedModels
from utils import get_environment


DB_NAME = os.environ.get("DB_NAME")
USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
SCHEMA = os.environ.get("DB_SCHEMA")
HOST = os.environ.get("DB_HOST")
PORT = os.environ.get("DB_PORT")

# Modifying database to dev depending on environment:
if get_environment() == "dev":
    DB_NAME += "-dev"


def get_tables(engine, schema):
    """Function to retrieve list of table names in database"""

    with engine.connect() as conn:
        query = text(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}';"
        )
        table_names = conn.execute(query).fetchall()
        table_names = [table[0] for table in table_names]

    return table_names


def reflect_metadata(engine, schema, tables):
    """Function to reflect tables in schema into metadata object"""

    # Create an empty SQLAlchemy metadata
    metadata = MetaData()

    for table in tables:
        metadata.reflect(bind=engine, schema=schema, only=[table])

    return metadata


def automap_db(engine, schema):
    """Function to automatically map all tables from schema"""

    # Getting tables from db:
    table_names = get_tables(engine, schema)

    # Creating metadata based on existing tables:
    metadata = reflect_metadata(engine, schema, table_names)

    # Create the automap base:
    Base = automap_base(metadata=metadata)
    Base.prepare()

    # Get the tables objects:
    dm = MappedModels(Base.classes)

    return dm


def get_db_url(
    username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db_name=DB_NAME
):
    """Function to return database url given parameters"""

    return f"cockroachdb://{username}:{password}@{host}:{port}/{db_name}"
