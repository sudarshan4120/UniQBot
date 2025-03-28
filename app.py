# Do not change, intentionally running argparse before imports
import argparse
parser = argparse.ArgumentParser(description="RAG Chatbot System")

# Create a mutually exclusive group for the two main options
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--pipeline", action="store_true",
                   help="Rerun the data pipeline (scrapping and preprocessing)")
group.add_argument("--chatbot", action="store_true",
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
    elif args.chatbot:
        print("Starting RAG chatbot...")
        model.run_rag_claude()
    elif args.server:
        from backend import husky_app
        print("Starting flask server...")
        husky_app.run()