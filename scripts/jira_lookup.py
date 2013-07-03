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
            if issue.fields.description:
                desc = issue.fields.description
            return '{id} ({status}): {title} ({url})\n{desc}'.format(id=issue_id.upper(), status=issue.fields.status.name, title=issue.fields.summary, desc=desc,url=url)
        except Exception as e:
            pass
