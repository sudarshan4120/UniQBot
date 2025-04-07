"""
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


"""
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
# Add model selection argument
parser.add_argument("--model", type=str, choices=["claude", "gpt"], default="claude",
                   help="Select the model to use (claude or gpt)")
# Parse arguments
args = parser.parse_args()
import utils  # This loads vars, do not remove
import scrapper
import preprocessing
import model
from app2 import RAGChatbot  # Import the GPT model implementation

def run_data_pipeline():
    scrapper.run_scrapper()
    preprocessing.run_cleaner()

def run_rag_model():
    """Run the appropriate RAG model based on command-line argument"""
    if args.model == "claude":
        print("Using Claude model...")
        model.run_rag_claude()
    else:  # args.model == "gpt"
        print("Using GPT model...")
        # Initialize and run the GPT-based chatbot
        try:
            import os
            
            # Get the OpenAI API key
            openai_api_key = os.getenv("OPENAI_API_KEY","")
            
            # Initialize the GPT chatbot with config values
            chatbot = RAGChatbot(
                openai_api_key=openai_api_key,  # Pass the API key from config
                model_name="gpt-3.5-turbo",  # Use model from config
                faiss_index_path="/Users/sudarshanp/Desktop/shreya_bot/data/faiss_index-shreya.index",
                chunks_folder="/Users/sudarshanp/Desktop/shreya_bot/data/chunks",
                max_chunks=5,
                max_context_tokens=10000
            )
            
            print("RAG GPT Chatbot initialized. Type 'exit' to quit.")
            while True:
                query = input("\nYou: ")
                if query.lower() in ["exit", "quit", "bye", "thanks"]:
                    break
                
                print("\nThinking...")
                response = chatbot.chat(query)
                print(f"\nChatbot: {response}")
        
        except Exception as e:
            print(f"Error initializing GPT chatbot: {e}")

if __name__ == "__main__":
    # Execute the selected option
    if args.pipeline:
        print("Running data pipeline...")
        run_data_pipeline()
        print("Data pipeline completed successfully!")
    elif args.chatbot:
        print("Starting RAG chatbot...")
        run_rag_model()  # Use the new function instead of directly calling model.run_rag_claude()
    elif args.server:
        from backend import husky_app
        
        # Set the model choice as an environment variable or global variable
        # instead of passing it as a parameter to run()
        print(f"Starting flask server with {args.model} model...")
        
        # Set the model choice before running the Flask app
        utils.selected_model = args.model  # Assuming utils has a variable to store this
        
        # Run the Flask app normally without extra parameters
        husky_app.run()

