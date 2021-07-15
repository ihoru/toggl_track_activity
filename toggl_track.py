import functools
import logging

import requests

import settings

logger = logging.getLogger(__name__)


def request(path):
    assert bool(settings.TOGGL_TRACK_TOKEN), 'Toggl Track token should be provided in settings'

    response = requests.get(
        'https://api.track.toggl.com/api/v8/' + path,
        auth=(settings.TOGGL_TRACK_TOKEN, 'api_token'),
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


@functools.lru_cache()
def projects(workspace_id):
    projects = request('workspaces/{}/projects'.format(workspace_id))
    return dict(
        (project['id'], project['name'])
        for project in projects
    )


@functools.lru_cache()
def users(workspace_id):
    users = request('workspaces/{}/workspace_users'.format(workspace_id))
    return dict(
        (user['uid'], user['name'])
        for user in users
    )


def activity(workspace_id):
    return request('dashboard/{}'.format(workspace_id))
