# -*- coding: utf-8 -*-

# VK Audios Saver configuration file

# How to provide access to your audios to VK Audios Saver script:

# Go to this link then grant access:
# https://oauth.vk.com/authorize?client_id=3697615&scope=audio,offline&response_type=token
# Then copy access_token value from address link and put into token value below
# P.S. Read this instruction for more correct understanding: http://zenno.pro/kak-poluchit-access-token-prilozheniya-vk-com/

# Notice: You should use any offical apps APP ID, that allows to get token (Windows 8-10 PC/Mobile app ID is set by default, but servers don't allow to get token from Android APP ID, for example).
# In other case VK servers won't give all your audios in resoponse of this script request.
# Real experience at 20 Aug 2016: from my 822 audios BEFORE it returned for download 498-500 audios only, but AFTER it return 818 (where it lost last 4 I still cannot understand).
# This solution offered by Elisey Izumtsev. Huge human thanks to him.

# VK Access Information

# access_token value here
token='<insert your access_token value here>'


# Download config

# audios download destination dir
destdir='music'

# delete excess audios and files yes - True, no - False
deleteExcess=False

# playlist prefix
playlist_prefix='playlist'

# generate playlists from your VK Albums? yes - True, no - False
generateAlbumPlaylists=True


# write songs lyrics (if present) to specified dir with song name
writeSongsLyrics=True

# lyrics dir
lyricsDir='lyrics'
# Is lyrics dir location is absolute and should'nt be located inside download destination dir? yes - True, no - False
lyricsDirIsPathAbsolute=False