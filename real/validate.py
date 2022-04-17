"""Utility functions for validating requests"""
from __future__ import annotations
from typing import Callable
from flask import request, render_template

from config import config

try:
    from .jsondb import usersdb
except ImportError:
    from jsondb import usersdb


INVALID_TOKEN = "invalid-token.html"
MISSING_TOKEN = "missing-token.html"
query_key = config["user_token_query"]


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
            if request.args[query_key] in usersdb.users:
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
                if request.args[query_key] in usersdb.users:
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
    if query_key in request.args:
        return usersdb.get_user(request.args[query_key])
    return None


def fix_subdomain_route(name: str, alternative: Callable):
    """Fix subdomain route for production"""

    def internal(func):
        """Internal"""

        def internal(*args, **kwargs):
            """Internal of internal"""
            if config["debug"]:
                return func(*args, **kwargs)

            if name in kwargs:
                val = kwargs[name]
                kwa = True
            else:
                kwa = False
                val = args[0]

            prod_splt = config["production_sub_domain"].split(".")
            splt = val.split(".")
            fix = ".".join(splt[: -len(prod_splt)])

            if not fix:
                if kwa:
                    del kwargs[name]
                else:
                    args = args[1:]

                return alternative(*args, **kwargs)

            if kwa:
                kwargs[name] = fix
            else:
                args = (fix, *args[1:])

            return func(*args, **kwargs)

        if getattr(func, "__doc__", None):
            internal.__doc__ = func.__doc__

        return internal

    return internal
