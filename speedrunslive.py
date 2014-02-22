import sys
import urllib2

try:
  import json
except:
  import simplejson as json

class JSONClient(object):
    def __init__(self, endpoint, logger):
        object.__init__(self)

        self.endpoint = endpoint
        self.logger = logger

    def _get(self, path, headers=None):
        request = urllib2.Request(self.endpoint + '/' + path)

        response = urllib2.urlopen(request)
        data = response.read()
        response.close()

        return data

    def get(self, path, headers=None):
        try:
            response = self._get(path, headers)
        except:
            raise Exception('HTTP error')

        try:
            obj = json.loads(response)
            return obj

        except:
            raise Exception('JSON parsing error')

class SpeedRunsLiveClient(object):
    def __init__(self, jsonClient, logger):
        self.jsonClient = jsonClient
        self.logger = logger

    def getStreams(self):
        obj = self.jsonClient.get('test/teams')
        streams = obj['channels']

        return self.formattedStreams(self.filteredStreams(streams))

    def filteredStreams(self, streams):
        for stream in streams:
            yield stream

    def formattedStreams(self, streams):
        for stream in streams:
            yield stream['channel']

def formattedItems(streams):
    for stream in streams:
        item = {
            'label': stream['display_name']
        }

        yield item
