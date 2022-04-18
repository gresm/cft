"""Main Website"""
from flask import Flask, render_template, request
from werkzeug.exceptions import Forbidden, NotFound, BadRequest
from config import config
from .validate import validate, current_user
from .jsondb import challengesdb, usersdb, savedb


app = Flask(__name__)
if config["debug"]:
    app.config[
        "SERVER_NAME"
    ] = f"{config['debug_server_name']}:{config['debug_server_port']}"


@app.route("/")
@validate(missing_template="index-missing.html")
def main():
    """Main page"""
    return render_template("index.html", user=current_user())


@app.route("/<path>")
@validate
def main_tasks(path: str):
    """main route for tasks"""

    if "action" in request.args:
        if request.args["action"] == "view":
            print("view")
            return render_task(path)
        if request.args["action"] == "submit":
            print("submit")
            if "flag" not in request.args:
                raise BadRequest
            return submit_flag(path, request.args["flag"])
    print("list all")
    return view_tasks(path)


def render_task(path: str):
    """Render specified task"""
    task = challengesdb.get_challenge(path)

    if not task:
        raise NotFound

    if not task.can_user_see(current_user()):
        raise Forbidden

    return render_template("task-view.html", task=task, user=current_user())


def generate_url_parameters(para: dict[str, str]) -> str:
    """Creates url parameters from dict"""
    ret = "?"

    for key in para:
        ret += f"{key}={para[key]}&"

    ret = ret[:-1]

    if para:
        return ret
    return ""


def submit_flag(path: str, flag: str):
    """Submit flag"""
    print("submitting")

    current = challengesdb.get_challenge(path)

    if not current:
        raise NotFound

    if not current.can_user_see(current_user()):
        raise Forbidden

    if flag == current.flag:
        current.solve(current_user())
        savedb(usersdb)
        return render_template(
            "redirect.html",
            path="/" + path,
            args=generate_url_parameters(
                {config["user_token_query"]: current_user().identifier}
            ),
        )
    return render_template("incorrect-flag.html", flag=flag)


def view_tasks(path: str):
    """View tasks"""

    if len(path.split(":")) == 1:
        return groups(path)

    return tasks(path)


def groups(category: str):
    """Return rendered hml for wieving the group"""
    if not challengesdb.get_category(category):
        raise NotFound
    if category not in current_user().access:
        raise Forbidden

    return render_template(
        "category-index.html",
        challenges=challengesdb.get_category(category).challenges.values(),
        user=current_user(),
    )


def tasks(identifier: str):
    """Return rendered html for wieving the task"""
    current = challengesdb.get_challenge(identifier)

    if not current:
        raise NotFound

    if (not current.can_user_see(current_user())) or not current.is_solved(
        current_user()
    ):
        raise Forbidden

    if current.sub_challenges is None:
        return (
            render_template(
                "category-no-sub-challenges.html", sub_challenge=identifier
            ),
            404,
        )

    chals = current.sub_challenges.challenges

    return render_template(
        "category-index.html", challenges=chals.values(), user=current_user()
    )
