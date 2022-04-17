"""Main Website"""
from flask import Flask, render_template
from config import config
from .validate import validate, current_user


app = Flask(__name__)
app.config[
    "SERVER_NAME"
] = f"{config['debug_server_name']}:{config['debug_server_port']}"


@app.route("/")
@validate(missing_template="index-missing.html")
def main():
    """Main page"""
    return render_template("index.html", user=current_user())


@app.route("/", subdomain="test")
# @validate
def main_category():
    """Main page for categories"""
    return "aaaa"
