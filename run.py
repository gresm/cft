"""Run project"""
from flask import Flask
from main import app as dispatch_app


app = Flask(__name__)
app.wsgi_app = dispatch_app
app.run()
