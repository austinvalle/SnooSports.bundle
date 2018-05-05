NAME = 'SnooSports'
ART = 'art-default.jpg'
ICON = 'icon-default.jpg'
PREFIX = '/video/snoosports'

def Start():
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)

@handler(PREFIX, NAME, art=ART, thumb=ICON)
def MainMenu():
	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(ShowNBAStreams, title="NBA"), title="NBA"))
	oc.add(DirectoryObject(key=Callback(ShowMLBStreams, title="MLB"), title="MLB"))
	oc.add(DirectoryObject(key=Callback(ShowSoccerStreams, title="Soccer"), title="Soccer"))

	return oc

@route(PREFIX + '/nba')
def ShowNBAStreams(title):
	oc = ObjectContainer(title2=title)
	oc.add(
        CreateVideoClipObject(
            url = 'http://d1dzfjk2pzv6t2.cloudfront.net/live/p1401/playlist.m3u8',
            title = 'Test NBA Stream',
            thumb = 'icon-default.png',
            art = 'art-default.jpg',
            summary = 'No description available',
            c_audio_codec = AudioCodec.AAC,
            c_video_codec = VideoCodec.H264,
            c_container = 'mpegts',
            c_protocol = 'hls',
            c_user_agent = None,
			optimized_for_streaming = True,
            include_container = False
        )
    )
	oc.add(
        CreateVideoClipObject(
            url = 'https://hlslive-l3c-ewr1.media.mlb.com/ls01/mlb/2018/05/05/Home_VIDEO_eng_Toronto_Blue_Jays_Tampa_B_20180505_1525551048404/master_wired60_complete.m3u8',
            title = 'Test MLB Stream',
            thumb = 'icon-default.png',
            art = 'art-default.jpg',
            summary = 'No description available',
            c_audio_codec = AudioCodec.AAC,
            c_video_codec = VideoCodec.H264,
            c_container = 'mpegts',
            c_protocol = 'hls',
            c_user_agent = None,
			optimized_for_streaming = True,
            include_container = False
        )
    )
	return oc

@route(PREFIX + '/mlb')
def ShowMLBStreams(title):
	oc = ObjectContainer(title2=title)
	return oc

@route(PREFIX + '/soccer')
def ShowSoccerStreams(title):
	oc = ObjectContainer(title2=title)
	return oc

@route(PREFIX + '/createvideoclipobject', include_container = bool)
def CreateVideoClipObject(url, title, thumb, art, summary,
                          c_audio_codec = None, c_video_codec = None,
                          c_container = None, c_protocol = None,
                          c_user_agent = None, optimized_for_streaming = True,
                          include_container = False, *args, **kwargs):

    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject,
                       url = url, title = title, thumb = thumb, art = art, summary = summary,
                       c_audio_codec = c_audio_codec, c_video_codec = c_video_codec,
                       c_container = c_container, c_protocol = c_protocol,
                       c_user_agent = c_user_agent, optimized_for_streaming = optimized_for_streaming,
                       include_container = True),
        rating_key = url,
        title = title,
        thumb = thumb,
        art = art,
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(Callback(PlayVideo, url = url, c_user_agent = c_user_agent))
                    )
                ],
                audio_codec = c_audio_codec if c_audio_codec else None,
                video_codec = c_video_codec if c_video_codec else None,
                container = c_container if c_container else None,
                protocol = c_protocol if c_protocol else None,
                optimized_for_streaming = optimized_for_streaming
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects = [vco], user_agent = c_user_agent if c_user_agent else None)
    else:
        return vco

@indirect
@route(PREFIX + '/playvideo.m3u8')
def PlayVideo(url, c_user_agent = None):
    if c_user_agent:
        HTTP.Headers['User-Agent'] = c_user_agent

    return IndirectResponse(VideoClipObject, key = url)