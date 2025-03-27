from flask import Flask, send_from_directory

husky_app = Flask(__name__)


# Route for homepage
@husky_app.route("/")
def index():
    return send_from_directory("frontend", 'index.html')


# Catch-all route for all other files
@husky_app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)


if __name__ == "__main__":
    husky_app.run(debug=True)
