from flask import Flask

husky_app = Flask(__name__)


@husky_app.route("/")
def index():
    return "This is home page"


if __name__ == "__main__":
    husky_app.run()
