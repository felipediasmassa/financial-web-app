from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base


def automap_db(engine, schema):
    """Function to automatically map all tables from schema"""

    # Generate declarative base from the database schema:
    Base = automap_base()
    # metadata = MetaData(schema=schema)
    # Base = automap_base(bind=engine, metadata=metadata)
    Base.prepare(engine, reflect=True, schema=schema, filter_names=["transactions"])

    # Get the tables objects:
    dm = DataModel(Base.classes)

    return dm


class DataModel:

    """Class to generate data models for all tables in database"""

    def __init__(self, base_classes):
        self.base_classes = base_classes

        self.Expense = base_classes.get("expenses")
