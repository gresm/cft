from werkzeug.middleware.dispatcher import DispatcherMiddleware
from real import app as app1
from git_updater import app as app2

app = DispatcherMiddleware(app1, {
    '/git-updater': app2
})
