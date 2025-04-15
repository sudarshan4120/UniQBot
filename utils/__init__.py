"""
PROPRIETARY SOFTWARE - NOT FOR DISTRIBUTION
Copyright © 2025 Naman Singhal

This code is protected under a strict proprietary license.
Unauthorized use, reproduction, or distribution is prohibited.
For licensing inquiries or authorized access, visit:
https://github.com/namansnghl/Pawsistant
"""

from utils.config import Manager
import os

config_manager = Manager()


def import_settings():
    print("Setting Configurations")
    config_manager.load_vars()
    Manager.load_prereqs()


# Initialize settings when the module is imported
import_settings()
