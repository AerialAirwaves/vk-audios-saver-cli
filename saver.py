# -*- coding: utf-8 -*-
print('VK Audios Saver Script by MelnikovSM')
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
sys.stdout.write('Loading libs.. ')
import vk_api
import re, os, codecs
import urlgrabber
g = urlgrabber.grabber.URLGrabber(reget='simple')
print('Done')

# Config file load
sys.stdout.write('Loading config file.. ')
try:
	import config
	print('Done')
except ImportError as error_msg:
	print('Error')
	raise ImportError, 'Please check config.py in current runtime dir!'

# Authorization & API capture
sys.stdout.write('Proceeding authorization at VK.. ')
vk_session = vk_api.VkApi(config.username, config.password)
try:
	vk_session.authorization()
	print('Done')
except vk_api.AuthorizationError as error_msg:
	print('Error')
	raise Exception, ('VK authorization error: '+str(error_msg))
vk = vk_session.get_api()

# Audios load
sys.stdout.write('Fetching audios list from VK.. ')
if config.pageid==0: config.pageid=vk.users.get()[0]['id']
totalAudiosCount=vk.audio.getCount(owner_id=config.pageid)

audios=[]

for caudio in vk.audio.get()['items']:
	audios.append({'aid': caudio['id'], 'title': caudio['title'], 'artist': caudio['artist'], 'url': caudio['url']})

print('Done')
if totalAudiosCount<>len(audios): print('Notice: VK servers provided information about '+str(len(audios))+' audios only of '+str(totalAudiosCount)+' total.')

if not os.path.exists(config.destdir):
	print('Notice: Download destination dir is not exists, attempting to create..')
	os.makedirs(config.destdir)

print('Starting '+str(len(audios))+' audios download..')

flist=[f for f in os.listdir(config.destdir) if os.path.isfile(os.path.join(config.destdir, f))]

def diff(a, b):
	b = set(b)
	return [aa for aa in a if aa not in b]

rlist=[]

fp=codecs.open(config.destdir+"/"+config.playlist, 'w', 'utf-8')
fp.write("#EXTM3U\n")

aeac=0
rtec=0
sadc=0

for audio in range(len(audios)):
	# converting artist & title to proper runtime
	artist = re.sub(' +', ' ', (str(audios[audio]['artist'].encode('utf8')).strip())).replace('&amp', '&').replace('&;', '&')
	title = re.sub(' +', ' ', (str(audios[audio]['title'].encode('utf8')).strip())).replace('&amp', '&').replace('&;', '&')
	if (artist=="" or artist.isspace()) and (title=="" or title.isspace()):
		fname=aid
	elif (artist=="" or artist.isspace()) and not (title=="" or title.isspace()):
		fname = re.sub(' +', ' ', ("Unknown - "+title).translate(None, ':*?!@%$<>|+\\\"').replace('/', '-'))
	else: fname = re.sub(' +', ' ', (artist+" - "+title).translate(None, ':*?!@%$<>|+\\\"').replace('/', '-'))

	sys.stdout.write("["+str(int((audio*1.0/len(audios)*1.0)*100))+"%] "+"Processing \"%s\" (#%s of %s).. " % (fname, audio, len(audios)))
	filepath = os.path.join(config.destdir, "%s.mp3" % (fname))
	fp.write("#EXTINF:,%s\n" % (artist+" - "+title))
	fp.write("%s.mp3\n" % (fname))
	if os.path.isfile(filepath)==False:
		try:
			g.urlgrab(str(audios[audio]['url']), filename=filepath)
			rlist.append("%s.mp3" % (fname))
			sadc+=1
			print('Complete')
		except urlgrabber.grabber.URLGrabError, e:
			if e.exception[1] != 'The requested URL returned error: 416 Requested Range Not Satisfiable':
				rtec+=1
				print('Error')
	else:
		aeac+=1
		print('Already exists.')
fp.close()
rlist.append(config.playlist)
rlist.append('playlist_deprecated.m3u')
print('Download complete!')

print('Displaying runtime stat..')
print('Total '+str(totalAudiosCount)+' audios detected at target ID')
if totalAudiosCount<>len(audios): print('But only '+str(len(audios))+' audios available for script.')
if sadc>0: print('Total successful downloads: '+str(sadc))
if aeac>0: print('Total already downloaded audios: '+str(aeac))
if rtec>0: print('Total terminated by error downloads: '+str(rtec))

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
		print "Notice: Script found %s (maybe) excess audio files:" %(len(diffm))
		fp=codecs.open(config.destdir+"/playlist_deprecated.m3u", 'w', 'utf-8')
		fp.write("#EXTM3U\n")
		for name in diffm:
			print name
			fp.write(name+"\n")
		fp.close()
		print "It may be deleted or seized by VK administration audios. Saved to playlist_deprecated"
	if len(difff)>0:
		print "Notice: Script found %s (maybe) excess files:" % len(difff)
		for name in difff: print name
