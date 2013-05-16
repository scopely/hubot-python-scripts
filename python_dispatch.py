import imp
import os
import sys
import inspect
import json
import re

from scripts import hubot_script

class HubotDispatch(object):

    def __init__(self):
        self.hear_regexes = {}
        self.resp_regexes = {}
        self.instance_map = {}
        self.load_scripts()
        self.start_listening()

    def start_listening(self):
        while True:
            line = sys.stdin.readline()
            if line:
                self.receive(line)
            else:
                return

    def receive(self, json_str):
        try:
            json_dict = json.loads(json_str)
            self.dispatch(json_dict)
        except Exception as e:
            pass

    def send(self, message):
        if message:
            sys.stdout.write(json.dumps(message) + '\n')
            sys.stdout.flush()

    def dispatch(self, json_dict):
        msg_type = json_dict['type']
        if msg_type == 'hear':
            json_dict['message'] = json_dict['message']
            self.dispatch_generic(json_dict, self.hear_regexes)
        elif msg_type == 'respond':
            self.dispatch_generic(json_dict, self.resp_regexes)

    def dispatch_generic(self, message, regexes):
        for regex in regexes:
            search = re.search(regex, message['message'])
            if search:
                handler = regexes[regex]
                response = message
                instance = self.instance_map[handler]
                response_text = handler(instance, message, search.groups())
                if response_text:
                    response['message'] = response_text
                    self.send(response)

    def no_handler(self, message):
        pass

    def load_scripts(self):
        prefix = '{root}{sep}'.format(root=os.getcwd(), sep=os.sep)
        sys.path.append('{0}scripts'.format(prefix))
        package = json.load(open('{0}package.json'.format(prefix)))
        self.scripts = []
        for filename in package['enabled_scripts']:
            modname = filename.replace('.py', '')
            modf = imp.find_module(modname)
            hubot_script._hear_regexes.clear()
            hubot_script._resp_regexes.clear()
            mod = imp.load_module(modname, *modf)
            regexes = {}
            regexes.update(hubot_script._hear_regexes)
            regexes.update(hubot_script._resp_regexes)
            self.hear_regexes.update(hubot_script._hear_regexes)
            self.resp_regexes.update(hubot_script._resp_regexes)

            for name, member in inspect.getmembers(mod):
                if inspect.isclass(member):
                    if issubclass(member, hubot_script.HubotScript) and member != hubot_script.HubotScript:
                        instance = member()
                        for key in regexes:
                            self.instance_map[regexes[key]] = instance
                        self.scripts += [instance]

if __name__ == '__main__':
    dispatch = HubotDispatch()
