"""Main script to run database setup operations"""

import os
import warnings

from infra.postgres_setup.utils.connect_postgres import connect_postgres

from infra.postgres_setup.create_tables import create_tables
from infra.postgres_setup.insert_values import insert_values
from infra.postgres_setup.fetch_data import fetch_table, fetch_table_names

import infra.postgres_setup.globals as g


warnings.filterwarnings("ignore")

SCHEMA = os.environ.get("DB_SCHEMA")

# Establishing connection with PostgreSQL:
conn = connect_postgres(schema=SCHEMA, autocommit=True)


def create_and_populate(run_create_tables=True, run_populate_data=False):
    """Function to create tables and views and populate database with dummy data"""

    # Running create tables function:
    if run_create_tables:
        create_tables(
            tables_scripts_folder=g.CREATE_TABLES_FOLDER, schema=SCHEMA, conn=conn
        )

    # Running insert values function:
    if run_populate_data:
        insert_values(
            dummy_data_folder=g.DUMMY_DATA_FOLDER,
            conn=conn,
            population_order=g.POPULATION_ORDER,
            include_id=g.INCLUDE_ID,
        )


def fetch_data(tables=None, include_views=False):
    """Function to fetch data from database tables"""

    if not tables:
        tables, views = fetch_table_names(
            conn=conn, schema=SCHEMA, include_views=include_views
        )

    for table in tables:
        fetch_table(table=table, conn=conn, table_type="table")

    for view in views:
        fetch_table(table=view, conn=conn, table_type="view")
