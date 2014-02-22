import sys
import urllib2

try:
  import json
except:
  import simplejson as json

class WebClient(object):
    def __init__(self, logger):
        object.__init__(self)

        self.logger = logger

    def get(self, url, headers=None):
        request = urllib2.Request(url)

        response = urllib2.urlopen(request)
        data = response.read()
        response.close()

        return data

class JSONClient(object):
    def __init__(self, webClient, logger):
        object.__init__(self)

        self.webClient = webClient
        self.logger = logger

    def get(self, url, headers=None):
        try:
            response = self.webClient.get(url, headers)
        except:
            raise Exception('HTTP error')

        try:
            obj = json.loads(response)
            return obj

        except:
            raise Exception('JSON parsing error')

class TwitchVideoResolver(object):
    _USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'

    def __init__(self, apiEndpoints, webClient, jsonClient, logger):
        self.apiEndpoints = apiEndpoints

        self.webClient = webClient
        self.jsonClient = jsonClient
        self.logger = logger

    def _resolveSWFURL(self, channel):
        swfURL = (self.apiEndpoints['justin'] +
            '/widgets/live_embed_player.swf?channel=' + channel)

        twitchURL = self.apiEndpoints['twitch'] + '/' + channel

        headers = {
            'User-Agent': _USER_AGENT,
            'Referer': twitchURL
        }

        request = urllib2.Request(swfURL, None, headers)
        response = urllib2.urlopen(request)

        return response.geturl()

    def _getToken(self, channel):
        url = (self.apiEndpoints['twitchApi'] + '/channels/' +
            channel + '/access_token')

        obj = self.jsonClient.get(url)
        return obj['token'], obj['sig']

    def _parseUnrestrictedPlayListItems(self, data):
        if 'No Results' not in data:
            items = data.split('\n')
            i = 0
            while i < len(items):
                item = items[i]
                if ('EXT-X-TWITCH-RESTRICTED' not in item):
                    yield item

                i += 1

        else:
            raise Exception('Stream offline')

    def _getPlaylistItems(self, channel, token, signature):
        template = (self.apiEndpoints['twitchUsher'] +
            '/select/{0}.m3u8?nauthsig={1}&nauth={2}&allow_source=true')

        url = template.format(channel, signature, token)
        data = self.webClient.get(url)

        return self._parseUnrestrictedPlayListItems(data)

    def resolveChannelToPlaylist(self, channel, playlistFilename):
      token, signature = self._getToken(channel)
      items = self._getPlaylistItems(channel, token, signature)

      playlistFile = open(playlistFilename, 'w')
      for item in items:
        playlistFile.write(item + '\n')

      playlistFile.close()

class SpeedRunsLiveClient(object):
    def __init__(self, apiEndpoint, jsonClient, logger):
        self.apiEndpoint = apiEndpoint
        self.jsonClient = jsonClient
        self.logger = logger

    def _getJSON(self, path):
        return self.jsonClient.get(self.apiEndpoint + '/' + path)

    def getStreams(self):
        obj = self._getJSON('test/teams')
        streams = obj['channels']

        return self.formattedStreams(self.filteredStreams(streams))

    def filteredStreams(self, streams):
        for stream in streams:
            yield stream

    def formattedStreams(self, streams):
        for stream in streams:
            yield stream['channel']
