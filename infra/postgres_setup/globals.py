"""Global constants"""


CREATE_TABLES_FOLDER = "infra/postgres_setup/create_tables/sql_scripts"
DUMMY_DATA_FOLDER = "infra/postgres_setup/insert_values/dummy_data"

POPULATION_ORDER = ["transactions", "categories"]
INCLUDE_ID = POPULATION_ORDER  # keep indices from CSV
NA_VALUES = [
    "",
    "#N/A",
    "#N/A N/A",
    "#NA",
    "-1.#IND",
    "-1.#QNAN",
    "-NaN",
    "-nan",
    "1.#IND",
    "1.#QNAN",
    "<NA>",
    # "N/A",
    "NA",
    "NULL",
    "NaN",
    "n/a",
    "nan",
    "null",
]
