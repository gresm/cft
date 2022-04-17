"""Main Website"""
from flask import Flask, render_template
from .validate import validate


app = Flask(__name__)


@app.route("/")
@validate(missing_template="index-missing.html")
def main():
    """Main page"""
    return render_template("index.html")


@app.route("/", subdomain="<category>")
@validate
def main_category(category: str):
    """Main page for categories"""
    return category
