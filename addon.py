from xbmcswift2 import Plugin, xbmc

from speedrunslive import WebClient, JSONClient, TwitchVideoResolver, SpeedRunsLiveClient

TWITCH_API_ENDPOINTS = {
    'justin': 'http://www.justin.tv',
    'twitch': 'http://www.twitch.tv',
    'twitchApi': 'http://api.twitch.tv/api',
    'twitchUsher': 'http://usher.twitch.tv'
}

SRL_API_ENDPOINT = 'http://api.speedrunslive.com:81'

plugin = Plugin()
logger = plugin.log

webClient = WebClient(logger)
jsonClient = JSONClient(webClient, logger)

srlVideoResolver = TwitchVideoResolver(
    TWITCH_API_ENDPOINTS, webClient, jsonClient, logger)

srlClient = SpeedRunsLiveClient(SRL_API_ENDPOINT, jsonClient, logger)

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

def formattedItems(streams):
    for stream in streams:
        item = {
            'label': stream['display_name'],
            'path': plugin.url_for('get_stream', channel=stream['name'])
        }

        yield item

@plugin.route('/stream/<channel>')
def get_stream(channel):
    playlistFilename = (xbmc.translatePath('special://temp/') +
        'twitchplaylist.m3u8')

    srlVideoResolver.resolveChannelToPlaylist(channel, playlistFilename)
    xbmc.Player().play(playlistFilename)

    plugin.set_resolved_url(playlistFilename)

if __name__ == '__main__':
    plugin.run()
