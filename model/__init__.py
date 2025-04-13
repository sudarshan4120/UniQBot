import os

if not os.getenv('ENV_STATUS') == '1':
    import utils  # This loads vars, do not remove
from model.claude import *
from model.openai import *
from model.openai_dataindex import build_knowledge_base

# Global chat engine variable [claude, gpt]
_chat_engine = [None, None]


def build_chat_engine(rebuild=False, index_name="claude_index", chunked_dir=''):
    """
    Build or load the RAG chat engine. (claude)

    Args:
        rebuild (bool): Force rebuild the index if True
        index_name (str): Name of the index directory
        chunked_dir (str): Directory containing chunked HTML files

    Returns:
        The initialized chat engine object
    """
    global _chat_engine

    # Return existing engine if already initialized and not forcing rebuild
    if _chat_engine[0] is not None and not rebuild:
        return _chat_engine[0]

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
    _chat_engine[0] = create_chat_engine(index_name=index_name)
    return _chat_engine[0]


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


def build_chat_engine_openai():
    global _chat_engine
    if _chat_engine[1] is not None:
        return _chat_engine[1]

    build_knowledge_base()

    # Initialize the GPT chatbot with config values
    _chat_engine[1] = RAGChatbot(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL"),
        faiss_index_path=os.path.join(os.getenv("HOME_DIR"), "faiss_index.index"),
        chunks_folder=os.getenv("CHUNKDATA_DIR")
    )
    return _chat_engine[1]


def run_rag_openai():
    try:
        chatbot = build_chat_engine_openai()
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


def run_rag_query_openai(query):
    try:
        chatbot = build_chat_engine_openai()
        return chatbot.chat(query)
    except Exception as e:
        return f"Error initializing GPT chatbot: {e}"
