"""Main Website"""
from flask import Flask, render_template, request
from .jsondb import usersdb


app = Flask(__name__)


@app.route("/")
def main():
    """Main page"""
    if "key" in request.args:
        if request.args["key"] in usersdb.users:
            pass
        else:
            return render_template("index-invalid-user.html"), 404
    return render_template("index.html")


@app.route("/", subdomain="<category>")
def main_category(category: str):
    """Main page for categories"""
    return category
