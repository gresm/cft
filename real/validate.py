"""Utility functions for validating requests"""
from __future__ import annotations
from typing import Callable
from flask import request, render_template

try:
    from .jsondb import usersdb
except ImportError:
    from jsondb import usersdb


INVALID_TOKEN = "invalid-token.html"
MISSING_TOKEN = "missing-token.html"


def validate(
    func: Callable | None = None,
    /,
    *,
    invalid_template: str | None = None,
    missing_template: str | None = None,
):
    """
    Decorator for functions that require special verification to get access.
    """

    def internal_def(*args, **kwargs):
        """Internal function"""
        if "key" in request.args:
            if request.args["key"] in usersdb.users:
                return func(*args, **kwargs)
            return render_template(INVALID_TOKEN), 404
        return render_template(MISSING_TOKEN), 403

    def internal_set(func):
        """Internal function"""

        invalid = invalid_template if invalid_template else INVALID_TOKEN
        missing = missing_template if missing_template else MISSING_TOKEN

        def nested(*args, **kwargs):
            """Nested internal function"""
            if "key" in request.args:
                if request.args["key"] in usersdb.users:
                    return func(*args, **kwargs)
                return render_template(invalid), 404
            return render_template(missing), 403

        return nested

    if func:
        return internal_def
    return internal_set


def current_user():
    """
    Get identifier of current user in request, returns None if there is no
    """
    if "key" in request.args and request.args["key"] in usersdb.users:
        return request.args["key"]
    return None
