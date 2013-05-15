import json
import re
import sys
import time

_hear_regexes = {}
_resp_regexes = {}

class HubotScript:

    def __init__(self):
        pass
        
# Decorators

def hear(regex):  
    def decorator(handler):
        _hear_regexes[regex] = handler
    return decorator  

def respond(regex):  
    def decorator(handler):
        _resp_regexes['^%s$' % regex] = handler
    return decorator
