# from utils.config import Manager
# import os

# def import_settings():
#     print("Setting Configurations")
#     config_manager = Manager()
#     config_manager.load_vars()

# import_settings()

from utils.config import Manager
import os

# Create a global instance of the config manager
config_manager = Manager()

def import_settings():
    print("Setting Configurations")
    config_manager.load_vars()

# Initialize settings when the module is imported
import_settings()

# Function to get the current selected model
def get_selected_model():
    return config_manager.get_model()

# Function to set the selected model
def set_selected_model(model_name):
    config_manager.set_model(model_name)