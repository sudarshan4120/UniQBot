from flask import Flask, send_from_directory, request, jsonify, make_response
from model import run_rag_query, build_chat_engine

build_chat_engine()
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
        response = run_rag_query(user_message)
        return jsonify({"response": response})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500