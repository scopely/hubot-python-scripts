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
#   #HU-201
#
# Author:
#   maxgoedjen

import os
from os import environ

HOST = environ.get('HUBOT_JIRA_HOSTNAME', '')
USERNAME = environ.get('HUBOT_JIRA_USERNAME', '')
PASSWORD = environ.get('HUBOT_JIRA_PASSWORD', '')

from jira.client import JIRA

from scripts.hubot_script import *

class JIRALookup(HubotScript):
    
    @hear('([a-zA-z]{2,100}-[0-9]*)')
    def lookup_jira(self, message, matches):
        issue_id = matches[0]
        jira = JIRA(options={'server': BASE}, basic_auth=(USER, PWD))
        issue = jira.issue(issue_id)
        if issue:
            url = '{base}/browse/{id}'.format(base=HOST, id=issue_id)
            return '{title} ({url})\n{desc}'.format(title=issue.fields.summary, desc=issue.fields.description)
