"""
PROPRIETARY SOFTWARE - NOT FOR DISTRIBUTION
Copyright © 2025 Naman Singhal

This code is protected under a strict proprietary license.
Unauthorized use, reproduction, or distribution is prohibited.
For licensing inquiries or authorized access, visit:
https://github.com/namansnghl/Pawsistant
"""

from flask import Flask, send_from_directory, request, jsonify, make_response
from model import run_rag_query, run_rag_query_openai, build_chat_engine, build_chat_engine_openai
import os
import utils

build_chat_engine()
build_chat_engine_openai()
husky_app = Flask(__name__)

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

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Process the message using your RAG system
        if os.getenv("ACTIVE_MODEL") == 'claude':
            response = run_rag_query(user_message)
        else:
            response = run_rag_query_openai(user_message)
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