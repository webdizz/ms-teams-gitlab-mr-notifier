def gitlab_merge_request_notify(request):
    """Handles any HTTP request, however responds only to interested in.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>`.
    """
    from flask import abort
    import json
    import requests
    import os
    import logging
    logger = logging.getLogger('gitlab_merge_request_notify')

    DEV_CHANNEL_URL = os.environ.get('DEV_CHANNEL_URL', 'MS Teams Developers channel URL')
    QA_CHANNEL_URL = os.environ.get('QA_CHANNEL_URL', 'MS Teams QAs channel URL')
    BRANCH_NAME = os.environ.get('BRANCH_NAME', 'hupg/')

    if request.method == 'POST' and request.headers['content-type'] == 'application/json':
        mr = request.get_json()

        logger.info(json.dumps(mr))

        if mr['object_kind'] == 'merge_request' and BRANCH_NAME in mr['object_attributes']['target_branch']:
            msg_title =  "MR {} created by {}".format(mr['object_attributes']['id'], mr['user']['name'])
            msg_text = "MR contains: {}".format(mr['object_attributes']['title'])
            msg_last_commit = "Last commit: {}".format(mr['object_attributes']['last_commit']['message'])
            msg_review = "{} please review MR {}".format(mr['assignee']['name'], mr['object_attributes']['id'])
            msg = {
                '@context': 'http://schema.org/extensions',
                '@type': 'MessageCard',
                'themeColor': '0072C6',
                "title": msg_title,
                "text": msg_text,
                "potentialAction": [
                    {
                    "@type": "OpenUri",
                    "name": msg_review,
                    "targets": [
                        { "os": "default", "uri": '{}/diffs'.format(mr['object_attributes']['url']) }
                    ]
                    }
                ],
                "sections": [
                    {
                    "activityTitle": mr['user']['name'],
                    "activitySubtitle": msg_last_commit,
                    "activityImage": mr['user']['avatar_url'],
                    "facts": [
                        {
                        "name": "Source branch:",
                        "value": mr['object_attributes']['source_branch']
                        },
                        {
                        "name": "Target branch:",
                        "value": mr['object_attributes']['target_branch']
                        },
                        {
                        "name": "Status:",
                        "value": mr['object_attributes']['state']
                        }
                    ],
                    }
                ]
            }
            response = json.dumps(msg)
            logger.info(response)
            requests.post(DEV_CHANNEL_URL, data = response)
            # notify QAs that feature was merged
            if mr['object_attributes']['state'] == 'merged':
                requests.post(QA_CHANNEL_URL, data = response)
            
        return "Merge request {} handled".format(mr['object_attributes']['id'])
    else:
        return abort(405)