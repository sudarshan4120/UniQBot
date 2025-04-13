from utils.config import Manager
import os

config_manager = Manager()


def import_settings():
    print("Setting Configurations")
    config_manager.load_vars()


# Initialize settings when the module is imported
import_settings()
