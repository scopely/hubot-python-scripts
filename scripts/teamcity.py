import json
import difflib
from os import environ

import requests
from requests.auth import HTTPBasicAuth

HOST = environ.get('HUBOT_TEAMCITY_HOSTNAME', '')
USERNAME = environ.get('HUBOT_TEAMCITY_USERNAME', '')
PASSWORD = environ.get('HUBOT_TEAMCITY_PASSWORD', '')
PROJECTS = [x.strip() for x in environ.get('HUBOT_TEAMCITY_PROJECTS', '').split(',')]

HEADERS = {'Accept': 'application/json'}
AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

from scripts.hubot_script import *

class TeamCity(HubotScript):

    @respond('(?:teamcity )?list projects')
    def hubot_list_projects(self, message, matches):
        projects = ''
        for x in self.get_buildtypes():
            projects += '{0}\n'.format(x[0])
        return projects
    

    @respond('(?:teamcity )?(?:build|deploy) (.*)')
    def hubot_build(self, message, matches):
        return str(matches)
        return build(name=matches[1])

    def build(self, name=''):
        closest = get_closest_buildtype(name)
        if not closest:
            return 'No projects found for {name}'.format(name=name)
        closest_name, closest_id = closest
        url = '/httpAuth/action.html?add2Queue={buildtype}'.format(buildtype=closest_id)
        r = request(url)
        if r.status_code == 200:
            return 'Building {name}'.format(name=closest_name)
        else:
            return 'Error building {name}'.format(name=closest_name)

    def get_buildtypes(self):
        all_buildtypes = {}
        for project in PROJECTS:
            url = '/httpAuth/app/rest/projects/name:{project}/buildTypes'.format(project=project)
            r = request(url)
            data = json.loads(r.text)
            for x in data['buildType']:
                all_buildtypes[x['name']] = x['id']
        return all_buildtypes

    def get_closest_buildtype(self, name=''):
        buildtypes = get_buildtypes()
        matches = difflib.get_close_matches(name, buildtypes.keys(), 1, .3)
        if matches:
            return (matches[0], buildtypes[matches[0]])

    def request(self, url):
    return requests.get('http://{host}{url}'.format(host=HOST, url=url), headers=HEADERS, auth=AUTH)
