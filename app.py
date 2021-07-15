import logging
from datetime import datetime, timedelta

from flask import Flask, render_template

import settings
import toggl_track
from duration import duration_string

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def index():
    workspace_id = settings.TOGGL_TRACK_WORKSPACE_ID
    users = toggl_track.users(workspace_id)
    projects = toggl_track.projects(workspace_id)
    items = []
    shown_user_ids = []
    now = datetime.utcnow()
    shift = settings.TOGGL_TRACK_RUNNING_DURATION_SHIFT_SECONDS
    for activity in toggl_track.activity(workspace_id)['activity']:
        user_id = activity['user_id']
        if user_id in settings.IGNORE_USER_IDS:
            continue
        if user_id in shown_user_ids:
            continue
        shown_user_ids.append(user_id)
        duration = activity['duration']
        stop = activity['stop']
        if stop:
            stopped = datetime.fromisoformat(stop).replace(tzinfo=None)
            stopped = duration_string(now - stopped)
            duration = duration_string(timedelta(seconds=duration))
        else:
            stopped = 'Running...'
            duration = datetime.fromtimestamp(-duration) - timedelta(seconds=shift)
            duration = now - duration
            duration = duration_string(duration)
        items.append(dict(
            user=users.get(user_id) or 'N/A',
            project=projects.get(activity['project_id']) or 'N/A',
            description=activity['description'],
            duration=duration,
            stopped=stopped,
        ))
    return render_template('activity.html', items=items)
