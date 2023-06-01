import glob


def create_tables(tables_scripts_folder, schema, conn):

    str_query = ""

    # Iterating through SQL scripts that create tables:
    for file in glob.glob(tables_scripts_folder + "/*_tables.sql"):
        f = open(file, "r")
        str_query += f.read()

    # Iterating through SQL scripts that create foreign keys:
    for file in glob.glob(tables_scripts_folder + "/*_constraints.sql"):
        f = open(file, "r")
        str_query += f.read()

    # Splitting each SQL statement into a dedicated string to execute queries:
    str_statements = [
        f"""
        DROP SCHEMA IF EXISTS {schema} CASCADE;
        CREATE SCHEMA {schema};
        """
    ]  # drop all existing tables
    str_statements += str_query.split(";")
    str_statements = [
        statement for statement in str_statements if statement.strip() != ""
    ]

    # Creating cursor on connection:
    cur = conn.cursor()

    # Executing each query:
    for query in str_statements:
        print(query)
        cur.execute(query)

    return
