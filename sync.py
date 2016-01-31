# -*- coding: utf-8 -*-
import os
import urllib2
import json
import codecs
import re
import HTMLParser
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
import urlgrabber

import vk_api
import config

from time import time

def runCommand(cmd):
	if not cmd==None:
		proc = subprocess.Popen(cmd.split(),
                            stdin = subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE
        	                )
		(out, err) = proc.communicate()
		return err, out

def get_token(credentials=[]):
	if not len(credentials):
		credentials = ('friends',)

	token, user_id = vk_api.auth(config.USERNAME,
								 config.PASSWORD,
								 config.CLIENT_ID,
								 ",".join(credentials))	
	return (token, user_id)


def get_audio(token, uid):
	res = vk_api.call_method('audio.getCount', {
		'oid': uid}, token)
	audio_cnt = res['response']

	res = vk_api.call_method('audio.get', {
		'count': audio_cnt}, token)

	return res
	

def clean_audio_tag(tag):
	h = HTMLParser.HTMLParser()
	tag = h.unescape(tag)
	tag = h.unescape(tag) # need to unescape unescaped entities

	tag = re.sub(r'http://.[^\s]+', '', tag) # remove any urls
	tag = tag.replace(' :)','') # remove smiles
	
	ctag = re.compile(u'[^a-zA-Zа-яА-ЯёЁ0-9\s_\.,&#!?\-\'"`\/\|\[\]\(\)]') 
	tag = ctag.sub('', tag).strip() # kill most unusual symbols
	tag = re.sub(r'\s+', ' ', tag) # remove long spaces

	return tag


def set_id3(filename, title, artist):
	try:
		mp3info = EasyID3(filename)
	except ID3NoHeaderError:
		mp3info = EasyID3()

	mp3info['title'] = title
	mp3info['artist'] = artist
	mp3info.save(filename) 

print "VKAudioSync script v0.04 by MelnikovSM"
if not os.path.exists(config.MUSIC_PATH):
	os.makedirs(config.MUSIC_PATH)
print "Loading songs list from VK.."
token, user_id = get_token(['audio'])
user_audio = get_audio(token, user_id)['response']
print "Downloading music to destination dir: %s" % (config.MUSIC_PATH)
i = 0
ei = 0
afi = 0
for track in user_audio:
	i+=1
	aid = str(track.get('aid'))
	artist = clean_audio_tag(track.get('artist'))
	title = clean_audio_tag(track.get('title'))
	url = track.get('url')
	filename = os.path.basename(url).split('?')[0]
	filepath = os.path.join(config.MUSIC_PATH, "%s.mp3" % (aid))
	print "Downloading song #%s with Audio ID: %s" % (i, aid)
	g = urlgrabber.grabber.URLGrabber(reget='simple')
	try:
		g.urlgrab(url, filename=filepath)
	except urlgrabber.grabber.URLGrabError, e:
		if e.exception[1] != 'The requested URL returned error: 416 Requested Range Not Satisfiable':
			print('Download error: '+e.exception[1])
			ei+=1
		else:
			print "This song is already downloaded, skipping.."
			afi+=1
print "Generating playlist.."
os.system('bash -c "cd '+config.MUSIC_PATH+"; find . -name '*.mp3'|sort -r|sed -r 's/.{2}//' > "+config.PLAYLIST+'"')
print """>>>>> Download complete! <<<<<
==========> Runtime statistics <=========="""
print "Total songs on account: %s" %(i)
if afi>0:
	print "Already downloaded songs found : %s" %(afi)
print "Total downloaded: %s" %(i-afi-ei)
if ei>0:
	print "Total download errors: %s" %(ei)