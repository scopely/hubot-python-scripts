# Description:
#   None
#
# Dependencies:
#   None
#
# Configuration:
#   None
#
# Commands:
#   HU-201
#
# Author:
#   maxgoedjen

import os
from os import environ

from jira.client import JIRA

from scripts.hubot_script import *

HOST = environ.get('HUBOT_JIRA_HOSTNAME', '')
USERNAME = environ.get('HUBOT_JIRA_USERNAME', '')
PASSWORD = environ.get('HUBOT_JIRA_PASSWORD', '')


class JIRALookup(HubotScript):

    @hear('([a-z]{2,100}-[0-9]+)')
    def lookup_jira(self, message, matches):
        issue_id = matches[0]
        jira = JIRA(options={'server': HOST}, basic_auth=(USERNAME, PASSWORD))
        try:
            issue = jira.issue(issue_id)
            url = '{base}/browse/{id}'.format(base=HOST, id=issue_id)
            desc = ''
            env = ''
            assignee = 'unassigned'
            if issue.fields.description:
                desc = issue.fields.description
            if issue.fields.environment:
                env = '\n{0}'.format(issue.fields.environment)
            if hasattr(issue, 'assignee'):
                assignee = 'assigned to {assignee}'.format(
                    assignee=issue.assignee.displayName)
            return '{id}: {status}, {assignee} ({tags})\n{title}: {url}\n{desc}{env}'.format(id=issue_id.upper(), status=issue.fields.status.name, title=issue.fields.summary, desc=desc, url=url, tags=', '.join(issue.fields.labels), assignee=assignee, env=env)
        except Exception as e:
            pass
