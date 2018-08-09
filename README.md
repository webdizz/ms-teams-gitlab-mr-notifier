ms-teams-gitlab-mr-notifier
========================

This repository is a simple implementation of WebHook to notify team in [MS Teams](https://products.office.com/en-us/microsoft-teams/group-chat-software) channel if there is Merge Request in [GitLab](https://about.gitlab.com/).

Prerequisite
------------------------

* GCP account as implementation is based on [Google Cloud Functions](https://cloud.google.com/functions/) with [Python 3](https://www.python.org/download/releases/3.0/) runtime
* [Python 3](https://www.python.org/download/releases/3.0/) and [Flask](http://flask.pocoo.org/)

Deployment
------------------------

    gcloud beta functions deploy gitlab_merge_request_notify --runtime python37 --trigger-http --region europe-west1 --memory=128