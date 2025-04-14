"""
PROPRIETARY SOFTWARE - NOT FOR DISTRIBUTION
Copyright © 2025 Naman Singhal

This code is protected under a strict proprietary license.
Unauthorized use, reproduction, or distribution is prohibited.
For licensing inquiries or authorized access, visit:
https://github.com/namansnghl/Pawsistant
"""

# Do not change, intentionally running argparse before imports
import argparse
import os

parser = argparse.ArgumentParser(description="RAG Chatbot System")

# Create a mutually exclusive group for the two main options
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--pipeline", action="store_true",
                   help="Rerun the data pipeline (scrapping and preprocessing)")
group.add_argument("--chatbot", type=str, choices=["claude", "gpt"], default="claude",
                   help="Start the RAG chatbot on CLI")
group.add_argument("--server", action="store_true",
                   help="Start the RAG flask server")

# Parse arguments
args = parser.parse_args()


import utils  # This loads vars, do not remove
import scrapper
import preprocessing
import model


def run_data_pipeline():
    scrapper.run_scrapper()
    preprocessing.run_cleaner()


if __name__ == "__main__":
    # Execute the selected option
    if args.pipeline:
        print("Running data pipeline...")
        run_data_pipeline()
        print("Data pipeline completed successfully!")
    elif args.server:
        from backend import husky_app
        print(f"Starting flask server with {os.getenv('ACTIVE_MODEL')} model...")
        husky_app.run()
    elif args.chatbot:
        print("Starting RAG chatbot...")
        if args.chatbot.lower() == "claude":
            print("Using Claude model...")
            model.run_rag_claude()
        elif args.chatbot.lower() == "gpt":
            print("Using GPT model...")
            model.run_rag_openai()