# from flask import Flask, send_from_directory, request, jsonify, make_response
# from model import run_rag_query, build_chat_engine

# build_chat_engine()
# husky_app = Flask(__name__)


# # Route for homepage
# @husky_app.route("/")
# def index():
#     return send_from_directory("frontend", 'index.html')


# # Catch-all route for all other files
# @husky_app.route("/<path:filename>")
# def frontend_files(filename):
#     return send_from_directory("frontend", filename)


# @husky_app.route("/api/chat", methods=["POST"])
# def chat_api():
#     if request.method == "OPTIONS":  # Handle preflight requests
#         response = make_response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add("Access-Control-Allow-Headers", "Content-Type")
#         response.headers.add("Access-Control-Allow-Methods", "POST")
#         return response

#     data = request.json
#     user_message = data.get("message", "")

#     if not user_message:
#         return jsonify({"error": "No message provided"}), 400

#     try:
#         # Process the message using your RAG system
#         response = run_rag_query(user_message)
#         return jsonify({"response": response})
#     except Exception as e:
#         print("Error:", e)
#         return jsonify({"error": str(e)}), 500

from flask import Flask, send_from_directory, request, jsonify, make_response
from model import run_rag_query, build_chat_engine
from app2 import RAGChatbot
import os
import utils

build_chat_engine()
husky_app = Flask(__name__)

# Initialize GPT chatbot
try:
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    gpt_chatbot = RAGChatbot(
        openai_api_key=openai_api_key,
        model_name="gpt-3.5-turbo",
        faiss_index_path="/Users/sudarshanp/Desktop/shreya_bot/data/faiss_index-shreya.index",
        chunks_folder="/Users/sudarshanp/Desktop/shreya_bot/data/chunks",
        max_chunks=5,
        max_context_tokens=10000
    )
    print("GPT chatbot initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize GPT chatbot: {e}")
    gpt_chatbot = None

# Route for homepage
@husky_app.route("/")
def index():
    return send_from_directory("frontend", 'index.html')


# Catch-all route for all other files
@husky_app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)


@husky_app.route("/api/chat", methods=["POST"])
def chat_api():
    if request.method == "OPTIONS":  # Handle preflight requests
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    data = request.json
    user_message = data.get("message", "")
    model_choice = data.get("model", "claude")  # Default to claude if not specified

    print(f"Received message, using model: {model_choice}")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        if model_choice == "gpt" and gpt_chatbot:
            # Use GPT model
            print("Using GPT model")
            response = gpt_chatbot.chat(user_message)
        else:
            # Use Claude model
            print("Using Claude model")
            response = run_rag_query(user_message)
            
        return jsonify({"response": response})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


def run():
    # Access model selection preference if it's available
    model_choice = getattr(utils, 'selected_model', 'claude')
    print(f"Starting server with {model_choice} model as default")
    
    # Start the Flask server
    husky_app.run(debug=True, host='0.0.0.0', port=5000)