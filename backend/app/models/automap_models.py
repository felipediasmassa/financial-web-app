"""Models mapped from database"""


class MappedModels:

    """Class to generate data models for all tables in database"""

    def __init__(self, base_classes):
        self.base_classes = base_classes

        self.Transaction = base_classes.get("transactions")
        self.Category = base_classes.get("categories")
