"""Main Loader"""
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask  # , request, redirect
from flask_talisman import Talisman
from real import app as app1
from git_updater import app as app2


app_dispatcher = DispatcherMiddleware(app1, {"/git-updater": app2})
app = Flask(__name__)
app.wsgi_app = app_dispatcher
talisman = Talisman(app)


# @app.before_request
# def force_https():
#     """Force https request"""
#     if request.endpoint in app.view_functions and not request.is_secure:
#         return redirect(request.url.replace("http://", "https://"))
#     return None
