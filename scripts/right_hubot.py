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
#   right, hubot
#
# Author:
#   maxgoedjen

import os

from scripts.hubot_script import *

class RightHubot(HubotScript):
    
    @hear('test')
    def right(self, message, matches):
        return 'TESTTESTTEST.'
