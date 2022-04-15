"""Main Loader"""
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from real import app
from git_updater import app as app2

app = DispatcherMiddleware(app, {
    '/git-updater': app2
})
