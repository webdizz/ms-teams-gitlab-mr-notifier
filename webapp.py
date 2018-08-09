from flask import Flask, url_for, request
from main import *

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_notification():
    return gitlab_merge_request_notify(request)