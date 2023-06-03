from sqlalchemy import MetaData, text
from sqlalchemy.ext.automap import automap_base


def automap_db(engine, schema):
    """Function to automatically map all tables from schema"""

    # Reflect each table individually
    with engine.connect() as conn:
        query = text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
        table_names = conn.execute(query).fetchall()
        print(table_names)

    # # Generate declarative base from the database schema:
    # Base = automap_base()
    # metadata = MetaData()
    # metadata.reflect(bind=engine)
    # Base = automap_base(metadata=metadata)
    # Base.prepare()
    # # Base.prepare(engine, reflect=True, schema=schema)

    # # Get the tables objects:
    # dm = DataModel(Base.classes)

    # return dm


class DataModel:

    """Class to generate data models for all tables in database"""

    def __init__(self, base_classes):
        self.base_classes = base_classes

        self.Expense = base_classes.get("expenses")
