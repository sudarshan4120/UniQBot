"""
PROPRIETARY SOFTWARE - NOT FOR DISTRIBUTION
Copyright © 2025 Naman Singhal

This code is protected under a strict proprietary license.
Unauthorized use, reproduction, or distribution is prohibited.
For licensing inquiries or authorized access, visit:
https://github.com/namansnghl/Pawsistant
"""

import os

if not os.getenv('ENV_STATUS') == '1':
    import utils  # This loads vars, do not remove
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from preprocessing.main import run_cleaner
