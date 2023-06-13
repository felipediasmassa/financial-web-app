import os


def get_environment():
    """Function to retrieve current environment based on environment variable"""

    # Value for HOSTING_INSTANCE is "cloud,<env>" e.g.: "cloud,prod"):
    env = os.environ.get("HOSTING_INSTANCE").split(",")[-1]

    print("ENV:::", env)

    return env
