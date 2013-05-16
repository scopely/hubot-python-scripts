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
    
    @hear('right(,)? hubot')
    def right(self, message, matches):
        return 'Yep.'
