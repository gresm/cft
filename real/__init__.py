"""Main Website"""
from flask import Flask, render_template
from werkzeug.exceptions import Forbidden
from config import config
from .validate import validate, current_user
from .jsondb import challengesdb


app = Flask(__name__)
if config["debug"]:
    app.config[
        "SERVER_NAME"
    ] = f"{config['debug_server_name']}:{config['debug_server_port']}"


@app.route("/")
@validate(missing_template="index-missing.html")
def main():
    """Main page"""
    return render_template("index.html", user=current_user())


@app.route("/<category>")
@validate
def main_category(category: str):
    """Main page for categories"""
    if not challengesdb.get_category(category):
        raise Forbidden
    if category not in current_user().access:
        raise Forbidden

    challenges = set()

    # for solved in current_user().access[category]:
    #     name = f"{category}:{solved}"
    #     challenges.update(challengesdb.get_challenge_trace(name))

    return render_template(
        "category-index.html",
        challenges=challenges,
    )
