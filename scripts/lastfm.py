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
#   stuff
#
# Author:
#   maxgoedjen

import os

from scripts.hubot_script import *

import lastfmapi

class LastFM(HubotScript):
    
    def __init__(self):
        self.api = lastfmapi.LastFmApi(os.environ.get('HUBOT_LASTFM_API_KEY'))
        HubotScript.__init__(self)

    def recent_tracks(self):
        recent = self.api.user_getRecentTracks(user=os.environ.get('HUBOT_LASTFM_USERNAME'))
        if 'track' in recent['recenttracks']:
            tracks = [Track(x) for x in recent['recenttracks']['track']]
            return tracks
        return []

    @hear('(?:last )?([0-9]* )?(?:song(?:s)? )played')
    def recently_played(self, message, matches):
        last_x = ''
        played = [track for track in self.recent_tracks() if not track.playing]
        lim = 1
        if matches[0]:
            lim = min(int(matches[0]), len(played))
        else:
            lim = min(1, len(played))
            
        for i in range(0, lim):
            last_x += '%s\n' % played[i]
        return last_x

    @hear('(currently playing|playing( right)? now|now playing|song\?)')
    def current(self, message, matches):
        current_track = None
        for track in self.recent_tracks():
            if track.playing:
                return '%s' % track
        return 'No track currently playing'
        
class Track:
    def __init__(self, props):
        self.name = props['name']
        self.artist = props['artist']['#text']
        self.playing = props.get('@attr', {'nowplaying':'false'})['nowplaying'] == 'true'

    def __str__(self):
        return '%s by %s' % (self.name, self.artist)
