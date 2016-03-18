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

print "Типо самопальная качалка музончега с ВКонтактика by MelnikovSM"
if not os.path.exists(config.MUSIC_PATH):
	os.makedirs(config.MUSIC_PATH)
print "Гружу список аудиозаписей со страницы.."
token, user_id = get_token(['audio'])
user_audio = get_audio(token, user_id)['response']
print "Качаю аудиозаписи в заданный в конфиге каталог: %s" % (config.MUSIC_PATH)
i = 0
ei = 0
afi = 0

flist=[f for f in os.listdir(config.MUSIC_PATH) if os.path.isfile(os.path.join(config.MUSIC_PATH, f))]

def diff(a, b):
	b = set(b)
	return [aa for aa in a if aa not in b]

rlist=[]

fp=codecs.open(config.MUSIC_PATH+"/"+config.PLAYLIST, 'w', 'utf-8')
fp.write("#EXTM3U\n")
for track in user_audio:
	i+=1
	aid = str(track.get('aid'))
	artist = re.sub(' +', ' ', (str(track.get('artist').encode('utf8')).strip())).replace('&amp', '&').replace('&;', '&')
	title = re.sub(' +', ' ', (str(track.get('title').encode('utf8')).strip())).replace('&amp', '&').replace('&;', '&')

	if (artist=="" or artist.isspace()) and (title=="" or title.isspace()):
		fname=aid
	elif (artist=="" or artist.isspace()) and not (title=="" or title.isspace()):
		fname = re.sub(' +', ' ', ("Unknown - "+title).translate(None, ':*?!@%$<>|+\\\"').replace('/', '-'))
	else: fname = re.sub(' +', ' ', (artist+" - "+title).translate(None, ':*?!@%$<>|+\\\"').replace('/', '-'))
	
	url = track.get('url')
	filename = os.path.basename(url).split('?')[0]
	filepath = os.path.join(config.MUSIC_PATH, "%s.mp3" % (fname))
	print "["+str(int((i*1.0/len(user_audio)*1.0)*100))+"%] "+"Качаю песню \"%s\".. (#%s из %s)" % (fname, i, len(user_audio))
	g = urlgrabber.grabber.URLGrabber(reget='simple')
	nic=1
	if os.path.isfile(filepath)==False:
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
				print "Какая-то хрень с именем файла. Пофиг, сохраню как "+aid+".mp3"
				filepath = os.path.join(config.MUSIC_PATH, "%s.mp3" % (aid))
				g = urlgrabber.grabber.URLGrabber(reget='simple')
				if os.path.isfile(filepath)==False:
					try:
						g.urlgrab(url, filename=filepath)
					except urlgrabber.grabber.URLGrabError, e:
						if e.exception[1] != 'The requested URL returned error: 416 Requested Range Not Satisfiable':
							print('Ошибка закачки: '+e.exception[1])
							ei+=1
						else:
							print "Данная песня уже закачана, ничо не делаю.."
							afi+=1
					else:
						print "Данная песня уже закачана, ничо не делаю.."
						afi+=1
			pass
	else:
		print "Данная песня уже закачана, ничо не делаю.."
		afi+=1
	if nic==1:
		fp.write("#EXTINF:,%s\n" % (artist+" - "+title))
		fp.write("%s.mp3\n" % (fname))
		rlist.append("%s.mp3" % (fname))
	elif nic==2: 
		fp.write("#EXTINF:,%s\n" % (artist+" - "+title))
		fp.write("%s.mp3\n" % (aid))
		rlist.append("%s.mp3" % (aid))
fp.close()
rlist.append(config.PLAYLIST)
print """>>>>> Закачка завершена! <<<<<
==========> Статистика работы <=========="""
print "Всего аудиозаписей на странице: %s" %(i)
if afi>0:
	print "Ранее скачаных аудиозаписей в каталоге: %s" %(afi)
print "Всего скачано/докачано: %s" %(i-afi-ei)
if ei>0:
	print "Ошибок закачки: %s" %(ei)

diffr=diff(flist, rlist)
if len(diffr)>0:
	diffm=[]
	difff=[]
	for name in diffr:
		if ".mp3" in name:
			diffm.append(name)
		else:
			difff.append(name)
	if len(diffm)>0:
		print "Найдено %s (возможно) лишних аудиозаписей:" %(len(diffm))
		for name in diffm: print name
		print "Возможно они были удалены одминами ВКонтакта по требованию копирастов, или вы просто удалили эти аудиозаписи со страницы. Что с ними делать, решать вам."
	if len(difff)>0:
		print "Найдено %s (возможно) лишних файлов:" % len(difff)
		for name in difff: print name
