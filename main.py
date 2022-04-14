"""Main Loader"""
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from real import app
from git_updater import app as app2

dispatch_app = DispatcherMiddleware(app, {
    '/git-updater': app2
})

app.wsgi_app = dispatch_app
