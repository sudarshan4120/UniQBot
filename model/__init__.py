import os

if not os.getenv('ENV_STATUS') == '1':
    import utils  # This loads vars, do not remove
from model.claude import *

# Global chat engine variable
_chat_engine = None


def build_chat_engine(rebuild=False, index_name="claude_index", chunked_dir=''):
    """
    Build or load the RAG chat engine.

    Args:
        rebuild (bool): Force rebuild the index if True
        index_name (str): Name of the index directory
        chunked_dir (str): Directory containing chunked HTML files

    Returns:
        The initialized chat engine object
    """
    global _chat_engine

    # Return existing engine if already initialized and not forcing rebuild
    if _chat_engine is not None and not rebuild:
        return _chat_engine

    if not chunked_dir:
        chunked_dir = os.getenv('CHUNKDATA_DIR')

    print("Building Chat Engine...")
    if rebuild or not index_exists(index_name):
        # Read all chunks from the HTML files
        print("Reading chunked HTML files...")
        chunks = read_chunked_html(chunked_dir)
        print(f"Found {len(chunks)} chunks across all files")

        # Build the RAG index
        print("Building RAG index...")
        index = build_rag_index(chunks, index_name=index_name)
        print("Index built successfully!")
    else:
        print(f"Using existing index from {index_name}")

    # Create chat engine
    _chat_engine = create_chat_engine(index_name=index_name)
    return _chat_engine


def run_rag_query(query, rebuild=False, index_name="claude_index", chunked_dir=''):
    """
    Process a single query using the RAG system

    Args:
        query (str): The user's query to process
        rebuild (bool): Force rebuild the index if True
        index_name (str): Name of the index directory
        chunked_dir (str): Directory containing chunked HTML files

    Returns:
        str: The response from the RAG system
    """
    # Ensure chat engine is initialized
    engine = build_chat_engine(rebuild, index_name, chunked_dir)

    try:
        response = engine.chat(query)
        return response.response
    except Exception as e:
        print(f"ERROR: {e}")
        return f"An error occurred: {str(e)}"


def run_rag_claude(rebuild=False, index_name="claude_index", chunked_dir=''):
    """
    Run the RAG Chat System with the specified parameters.

    Args:
        rebuild (bool): Force rebuild the index if True
        index_name (str): Name of the index directory
        chunked_dir (str): Directory containing chunked HTML files
    """
    # Ensure chat engine is initialized
    build_chat_engine(rebuild, index_name, chunked_dir)

    # Interactive chat loop
    print("\nRAG Chat System Ready! Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break

        try:
            response = run_rag_query(user_input, False, index_name, chunked_dir)
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"ERROR: {e}")