import urllib2
import os

PLAYLIST_URL = "http://tv.sychrovnet.cz/channels.m3u"

CACHE_FILE = '/tmp/channels.m3u'


def get_or_create_channels():
    if not os.path.exists(CACHE_FILE):
        o = urllib2.urlopen(PLAYLIST_URL)
        f = open(CACHE_FILE, 'w')
        f.write(o.read())

    f = open(CACHE_FILE)

    return f.readlines()


def parse_channels(lines):
    res = []
    for line in lines:
        if line.startswith('#EXTINF:'):
            res.append(line.replace('\r\n', ''))
        if line.startswith('http://sledovanitv.cz/'):
            res.append(line.replace('\r\n', ''))

    return res


def separate_list(channels_list):
    r = []
    for i in range(0, len(channels_list)):
        if i % 2 == 0:
            r.append((channels_list[i],))
        else:
            r[-1] = (r[-1][0], channels_list[i])

    radios = {}
    tvs = {}

    for channel in r:
        channel_name = channel[0].split('#EXTINF:,')[1]
        channel_url = channel[1]

        if "/channel/radio_" in channel_url:
            radios[channel_name] = channel_url
        else:
            tvs[channel_name] = channel_url

    return radios, tvs


def create_m3u(fname, context):
    f = open(fname, 'w')
    f.write('#EXTM3U\n')

    for k, v in context.iteritems():
        f.write("#EXTINF:0,%s,,0\n" % k)
        f.write(v + "\n")


def main():
    content = get_or_create_channels()

    data = parse_channels(content)

    radios, tvs = separate_list(data)

    tv_file = '/home/paiti/.config/smplayer/tv.m3u8'
    radio_file = '/home/paiti/.config/smplayer/radio.m3u8'

    create_m3u(tv_file, tvs)
    create_m3u(radio_file, radios)


if __name__ == "__main__":
    main()