from xbmcswift2 import Plugin

from speedrunslive import JSONClient, SpeedRunsLiveClient, formattedItems

API_ENDPOINT = 'http://api.speedrunslive.com:81'

plugin = Plugin()
logger = plugin.log
jsonClient = JSONClient(API_ENDPOINT, logger)
srlClient = SpeedRunsLiveClient(jsonClient, logger)

@plugin.route('/')
def index():
    items = [
        {
            'label': 'Streams',
            'path': plugin.url_for('get_streams')
        }
    ]

    return items

@plugin.route('/streams')
def get_streams():
    streams = srlClient.getStreams()
    items = formattedItems(streams)

    return items

if __name__ == '__main__':
    plugin.run()
