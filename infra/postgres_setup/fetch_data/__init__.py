import pandas.io.sql as sqlio


def fetch_table(table, conn, table_type):

    """Function to fetch one table from database"""

    if table_type == "table":
        sql = f"SELECT * FROM {table}"
    elif table_type == "view":
        sql = f'SELECT * FROM "{table}"'

    # Fetching data:
    dat = sqlio.read_sql_query(sql, conn)

    # Displaying data:
    print(f"### {table.upper()}")
    print(dat, "\n")

    return dat


def fetch_table_names(conn, schema, include_views):

    """Function to fetch all tables at once"""

    tables_query = f"""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = '{schema}' AND table_type = 'BASE TABLE'
    """

    curs = conn.cursor()
    curs.execute(tables_query)
    all_tables = [table[0] for table in curs.fetchall()]

    if include_views:
        views_query = f"""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = '{schema}' AND table_type = 'VIEW'
        """
        curs = conn.cursor()
        curs.execute(views_query)
        all_views = [table[0] for table in curs.fetchall()]

    else:
        all_views = []

    return all_tables, all_views
