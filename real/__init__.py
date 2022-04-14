"""Main Website"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    """Main Page"""
    return render_template("main.html")
