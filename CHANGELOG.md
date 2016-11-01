VK Audios Saver python script changelog:

1 Nov 2016:

* Fixed 'Too many requests per second' VK API error while processing album playlists
* Added deleted audios lyrics autodeletion


15 Sep 2016:

* Added by VK Audio Albums playlists generation option
* Added audios lyrics saving option
* Added excess files autodeletion option

1 Sep 2016:

+ Changed autogen playlists extension from "m3u" to "m3u8" for better readability by most players (8 digit at the end gives them to know about file encoded with utf-8)

24 Aug 2016:

+ Changed mp3 download lib from "urlgrabber" to "urllib"

23 Aug 2016:

+ Changed VK API interraction lib from "vk_api" to "vk"

20 Aug 2016:

+ Fixed excess audios search (since 04 Aug 2016 update if song already downloaded it wont be marked as existing in VK audios)
+ Added solution for "VK hides near half of audios from response"
	Problem details:
		For correct audios response you should use any offical apps APP ID, that allows to get token.
		In other case VK servers won't give all your audios in resoponse of this script request.
		Real experience at 20 Aug 2016: from my 822 audios BEFORE it returned for download 498-500 audios only, but AFTER it return 818 (where it lost last 4 I still cannot understand).
	Solution details:
		Default App ID at access_token request link changed to Windows App's App ID.
  Special thanks to Elisey Izumtsev for this solution.
+ Added download error handler: in case of VK server don't give download link (it could occur, for example, if song is seized by administration to comply with the DMCA)

07 Aug 2016:

+ Security improvement: Auth moved from username&password in config to access_token usage
+ Now script not turn page to online state when start (problem has existed since 04 Aug 2016 update)

04 Aug 2016:

+ Project renamed from "VKAudioSync" to "VK Audios Saver python script"
+ Repository renamed from "vkaudiosync" to "vk-audios-saver-cli"
+ Script absolutely rewritten from null, now using vk_api lib for interraction with VK.com

18 Mar 2016:

+ Modified output messages locale
+ Added excess files & audios search in music download folder to runtime stat output

01 Mar 2016:

+ Added showing download status (current download percentage, current song number, total songs number)
+ Rewritten download errors handlers for optimization purposes
+ Added download error hander: if save song with default file format impossible, save with template "<AudioID>.mp3"


28 Feb 2016:

+ Rewritten audios "Artist" and "Title" values reading
+ Added multi-spaces remove for "Artist" and "Title" values ("Stuff   a" with 2 or more spaces converts to "Stuff a" with one space)

22 Feb 2016:

+ Removed unix commands usage for cross-platfrom run ability.
+ Output locale changed from English to Russian.
+ Output filename format changed from <AudioID>.mp3 to "<Artist> - <Title>.mp3" where it possible
+ Implemented safe audios "Artist" and "Title" end values convertation (remove unsafe symbols for end file path).


31 Jan 2016:

+ Repository creation
+ Publication of my "VKAudioSaver" script sources in GitHub repo
