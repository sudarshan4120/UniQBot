"""
PROPRIETARY SOFTWARE - NOT FOR DISTRIBUTION
Copyright © 2025 Naman Singhal

This code is protected under a strict proprietary license.
Unauthorized use, reproduction, or distribution is prohibited.
For licensing inquiries or authorized access, visit:
https://github.com/namansnghl/Pawsistant
"""

import time
from functools import wraps


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.2f} seconds to execute")
        return result

    return wrapper
