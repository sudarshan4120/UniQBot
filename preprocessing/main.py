"""
PROPRIETARY SOFTWARE - NOT FOR DISTRIBUTION
Copyright © 2025 Naman Singhal

This code is protected under a strict proprietary license.
Unauthorized use, reproduction, or distribution is prohibited.
For licensing inquiries or authorized access, visit:
https://github.com/namansnghl/Pawsistant
"""

import os
from preprocessing.cleaning import process_cleaning
from preprocessing.chunking import process_files


def run_cleaner():
    raw_html_dir = os.getenv('RAWDATA_DIR')
    cleaned_html_dir = os.getenv('CLEANDATA_DIR')
    chunked_output_dir = os.getenv('CHUNKDATA_DIR')

    print("Cleaning extracted HTML files...")
    process_cleaning(raw_html_dir, cleaned_html_dir)

    print("Chunking cleaned HTML files...")
    process_files(cleaned_html_dir, chunked_output_dir)

    print("Cleaning pipeline completed successfully!")
