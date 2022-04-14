from flask import Flask, request
import git
import hmac
import hashlib
import os


w_secret = os.getenv("PROJECT_UPDATE_SECRET")
repo_location = os.getenv("PROJECT_REPO")


def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


app = Flask(__name__)


@app.route("/")
def main():
    return "hello from sub app: git-updater"


@app.route('/update', methods=['POST'])
def webhook():
    if request.method == 'POST':
        x_hub_signature = request.headers.get("X-Hub-Signature")

        if not is_valid_signature(x_hub_signature, request.data, w_secret):
            return "Signature Invalid", 400

        repo = git.Repo(repo_location)
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
