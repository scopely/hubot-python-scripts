import json
import difflib
from os import environ

import requests
from requests.auth import HTTPBasicAuth
from scripts.hubot_script import *

HOST = environ.get('HUBOT_TEAMCITY_HOSTNAME', '')
USERNAME = environ.get('HUBOT_TEAMCITY_USERNAME', '')
PASSWORD = environ.get('HUBOT_TEAMCITY_PASSWORD', '')
PROJECTS = [x.strip() for x in environ.get('HUBOT_TEAMCITY_PROJECTS', '').split(',')]

HEADERS = {'Accept': 'application/json'}
AUTH = HTTPBasicAuth(USERNAME, PASSWORD)


class TeamCity(HubotScript):

    @respond('list (?:teamcity )?projects')
    def hubot_list_projects(self, message, matches):
        projects = ''
        for x in self.get_buildtypes():
            projects += '{0}\n'.format(x)
        return projects
    
    @respond('(?:teamcity )?(?:build|deploy) ([^ ]*)(?: (.*))?')
    def hubot_build(self, message, matches):
        return self.build(name=matches[0], matches[1])

    def build(self, name='', branch=''):
        closest = self.get_closest_buildtype(name)
        if not closest:
            return 'No projects found for {name}'.format(name=name)
        closest_name, closest_id = closest
        branchstr = ''
        if branch:
            branchstr = '&branchName={branch}'.format(branch=branch)
        url = '/httpAuth/action.html?add2Queue={buildtype}&moveToTop=true{branchstr}'.format(buildtype=closest_id)
        r = self.request(url)
        if r.status_code == 200:
            return 'Building {name}'.format(name=closest_name)
        else:
            return 'Error building {name}'.format(name=closest_name)

    def get_buildtypes(self):
        all_buildtypes = {}
        for project in PROJECTS:
            url = '/httpAuth/app/rest/projects/name:{project}/buildTypes'.format(project=project)
            r = self.request(url)
            data = json.loads(r.text)
            for x in data['buildType']:
                all_buildtypes[x['name']] = x['id']
        return all_buildtypes

    def get_closest_buildtype(self, name=''):
        buildtypes = self.get_buildtypes()
        matches = difflib.get_close_matches(name, buildtypes.keys(), 1, .3)
        if matches:
            return (matches[0], buildtypes[matches[0]])

    def request(self, url):
        return requests.get('http://{host}{url}'.format(host=HOST, url=url), headers=HEADERS, auth=AUTH)
