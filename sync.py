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
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import vk_api
import config

from time import time

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
	
	ctag = re.compile(u'[^a-z^A-Z^а-я^А-ЯёЁ0-9\s_\.,&#!?\-\'"`\[\]\(\)]') 
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

print "Типо самопальная качалка музончега с ВКонтактика by MelnikovSM"
if not os.path.exists(config.MUSIC_PATH):
	os.makedirs(config.MUSIC_PATH)
print "Гружу список музона со страницы.."
token, user_id = get_token(['audio'])
user_audio = get_audio(token, user_id)['response']
print "Качаю музон в заданный в конфиге каталог: %s" % (config.MUSIC_PATH)
i = 0
ei = 0
afi = 0
fp=codecs.open(config.MUSIC_PATH+"/"+config.PLAYLIST, 'w', 'utf-8')
fp.write("#EXTM3U\n")
for track in user_audio:
	i+=1
	aid = str(track.get('aid'))
	artist = str(track.get('artist').encode('utf8'))
	title = str(track.get('title').encode('utf8'))

	if (artist=="" or artist.isspace()) and (title=="" or title.isspace()):
		fname=aid
	elif (artist=="" or artist.isspace()) and not (title=="" or title.isspace()):
		fname = ("Unknown - "+title).translate(None, ':*?!@%$<>|+\\').replace('/', '-')
	else: fname = (artist+" - "+title).translate(None, ':*?!@%$<>|+\\').replace('/', '-')
	
	url = track.get('url')
	filename = os.path.basename(url).split('?')[0]
	filepath = os.path.join(config.MUSIC_PATH, "%s.mp3" % (fname))
	print "Качаю песню #%s.. (%s)" % (i, fname)
	g = urlgrabber.grabber.URLGrabber(reget='simple')
	nic=1
	try:
		g.urlgrab(url, filename=filepath)
	except urlgrabber.grabber.URLGrabError, e:
		try:
			if e.exception[1] != 'The requested URL returned error: 416 Requested Range Not Satisfiable':
				print('Ошибка закачки: '+e.exception[1])
				nic=0
				ei+=1
			else:
				print "Данная песня уже закачана, ничо не делаю.."
				afi+=1
		except AttributeError:
			nic=2
			print "Какая-то хрень с именем файла, пофиг, сохраню как "+aid+".mp3"
			filepath = os.path.join(config.MUSIC_PATH, "%s.mp3" % (aid))
			g = urlgrabber.grabber.URLGrabber(reget='simple')
			try:
				g.urlgrab(url, filename=filepath)
			except urlgrabber.grabber.URLGrabError, e:
				if e.exception[1] != 'The requested URL returned error: 416 Requested Range Not Satisfiable':
					print('Ошибка закачки: '+e.exception[1])
					ei+=1
				else:
					print "Данная песня уже закачана, ничо не делаю.."
					afi+=1
		pass
	if nic==1:
		fp.write("#EXTINF:,%s\n" % (artist+" - "+title))
		fp.write("%s.mp3\n" % (fname))
	elif nic==2: 
		fp.write("#EXTINF:,%s\n" % (artist+" - "+title))
		fp.write("%s.mp3\n" % (aid))
fp.close()
print """>>>>> Закачка завершена! <<<<<
==========> Статистика работы <=========="""
print "Всего музла на странице: %s" %(i)
if afi>0:
	print "Ранее скачаного музла в каталоге: %s" %(afi)
print "Всего скачано/докачано: %s" %(i-afi-ei)
if ei>0:
	print "Ошибок закачки: %s" %(ei)
