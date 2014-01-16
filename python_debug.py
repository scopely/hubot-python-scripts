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
            line = raw_input('>')
            if line:
                self.receive(line)
            else:
                return

    def receive(self, line):
        self.dispatch(line)

    def send(self, message):
        if message:
            print message

    def dispatch(self, msg):
        if msg.startswith('hubot '):
            trimmed = msg[len('hubot '):]
            self.dispatch_generic(trimmed, self.resp_regexes)
        else:
            self.dispatch_generic(msg, self.hear_regexes)

    def dispatch_generic(self, message, regexes):
        for regex in regexes:
            search = re.search(regex, message, re.IGNORECASE)
            if search:
                handler = regexes[regex]
                response = message
                instance = self.instance_map[handler]
                try:
                    response_text = handler(instance, message, search.groups())
                    if response_text:
                        self.send(response_text)
                except Exception as e:
                    self.send('Python exception: {0}'.format(str(e)))
                    self.send(response)

    def no_handler(self, message):
        pass

    def load_scripts(self):
        prefix = '{root}{sep}'.format(
            root=os.path.dirname(os.path.realpath(__file__)), sep=os.sep)
        sys.path.append('{0}scripts'.format(prefix))
        package = json.load(open('{0}package.json'.format(prefix)))
        self.scripts = []
        for filename in package['enabled_scripts']:
            modname = filename.replace('.py', '')
            modf = imp.find_module(modname)
            hubot_script._hear_regexes.clear()
            hubot_script._resp_regexes.clear()
            try:
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
            except Exception as e:
                pass

if __name__ == '__main__':
    dispatch = HubotDispatch()
