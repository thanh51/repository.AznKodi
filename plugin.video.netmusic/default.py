# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 4 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib, urllib2, re, os, sys
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.video.netmusic')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
homemenu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists', 'menulist.xml'))
dict = {'&amp;':'&', '&quot;':'"', '.':' ', '&#39':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...'}
karaoke = 'http://www.timkaraoke.com'
nctm = 'http://m.nhaccuatui.com/'
csn = 'http://chiasenhac.com/'
ThuyNga = 'http://ott.thuynga.com/'	

def replace_all(text, dict):
	try:
		for a, b in dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass	
 		
def menulist():
	try:
		mainmenu = open(homemenu, 'r')  
		mlink = mainmenu.read()
		mainmenu.close()
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(mlink)
		return match
	except:
		pass	

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req, timeout = 60)
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

def home():
	add_dir('[COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[COLOR yellow]  Home  [COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[/COLOR]', '', None, icon, fanart)
			
def main():
	add_dir('[COLOR lightgreen]Hát Karaoke Online[/COLOR]', 'KaraokeOnline', 6, logos + 'karaoke.png', fanart)
	#add_dir('[COLOR yellow]Thuý Nga - Paris by Night[/COLOR]', 'thuynga', 11, logos + 'thuynga.png', fanart)  	
	add_dir('[COLOR lime]Video Chia Sẻ Nhạc[/COLOR]', csn, 2, logos + 'csn.png', fanart)
	add_dir('[COLOR cyan]Video Nhạc Của Tui[/COLOR]', nctm + 'mv.html', 2, logos + 'nct.png', fanart)  
	add_link('[COLOR gold]Vmusic[/COLOR]', 'http://206.190.140.142:1935/liveStream/mtv_1/playlist.m3u8', 4, logos + 'vmusic.png', fanart)	
	add_link('[COLOR magenta]Viet MTV[/COLOR]', 'http://64.62.143.5:1935/live/donotstealmy-Stream1/playlist.m3u8?bitrate=800&q=high', 4, logos + 'vietmtv.png', fanart)		
	add_link('[COLOR violet]VPop TV[/COLOR]', 'http://206.190.136.254:1935/liveStream/vpoptv_1/playlist.m3u8', 4, logos + 'vpop.png', fanart)
	add_link('[COLOR chocolate]iTV[/COLOR]', 'rtmp://live.kenhitv.vn/liveweb/ playpath=itv_web_500k.stream swfUrl=http://zui.vn/templates/images/jwplayer.swf pageUrl=http://zui.vn/livetv/itv-10.html', 4, logos + 'itv.png', fanart)
	add_link('[COLOR orange]M[COLOR red]TV[/COLOR][/COLOR]', 'rtmp://85.132.78.6:1935/live/ playpath=muztv.stream swfUrl=http://zui.vn/templates/images/jwplayer.swf pageUrl=http://zui.vn/livetv/mtv-81.html', 4, logos + 'mtv.png', fanart)
	add_link('[COLOR yellow]VEVO HD 1[/COLOR]', 'http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch1/06/prog_index.m3u8', 4, logos + 'vevo.png', fanart)	
	add_link('[COLOR yellow]VEVO HD 2[/COLOR]', 'http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch2/06/prog_index.m3u8', 4, logos + 'vevo.png', fanart)	
	add_link('[COLOR yellow]VEVO HD 3[/COLOR]', 'http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch3/06/prog_index.m3u8', 4, logos + 'vevo.png', fanart)	

def get_karaoke():
	home()
	add_dir('[COLOR magenta]++++ [COLOR white][B]Youtube Search[/B] [COLOR magenta]++++[/COLOR]', 'youtube', 1, logos + 'YTSearch.png', fanart)	
	add_dir('[COLOR cyan]Vietnamese[COLOR magenta] - [COLOR lightgreen]timkaraoke.com[/COLOR]', karaoke, 2, logos + 'timkaraoke.png', fanart)	
	for title, url, thumb in menulist():
		if 'Karaoke - ' in title:
			add_dir(title.replace('Karaoke - ', ''), url, 3, logos + thumb, fanart) 
	
def thuy_nga():
	home()
	add_dir('PBN SHOWS | [COLOR yellow]VARIETY[/COLOR]', ThuyNga + 'en/genre/index/22/3/', 3, logos + 'thuynga.png', fanart)  
	add_dir('PBN SHOWS | [COLOR cyan]COMEDY[/COLOR]', ThuyNga + 'en/genre/index/26/3', 3, logos + 'thuynga.png', fanart)  
	add_dir('PBN SHOWS | [COLOR lime]BTS[/COLOR]', ThuyNga + 'en/genre/index/64/3', 3, logos + 'thuynga.png', fanart)    
  
def search(): 
	try:
		keyb = xbmc.Keyboard('', '[COLOR yellow]Enter search text[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText())
		if 'Chia Sẻ Nhạc' in name: 
			url = csn + 'search.php?s=' + searchText + '&cat=video'   
			search_result(url)
		elif 'Youtube Search' in name:  
			url = 'https://www.youtube.com/results?search_query=' + searchText
			search_result(url)			
		elif 'Nhạc Của Tui' in name:
			url = nctm + 'tim-kiem/mv?q=' + searchText     
			media_list(url)
		elif 'Tìm Karaoke' in name:
			url = karaoke + '/search/karaoke/' + searchText.replace('+', ' ')     
			media_list(url) 			
	except: 
		pass

def search_result(url):
	home()
	content = make_request(url)
	if 'youtube' in url:
		match = re.compile('href="/watch\?v=(.+?)" class=".+?" data-sessionlink=".+?" title="(.+?)".+?Duration: (.+?).</span>').findall(content)
		for url, name, duration in match:
			name = replace_all(name, dict)
			thumb = 'https://i.ytimg.com/vi/' + url + '/mqdefault.jpg'
			url = 'plugin://plugin.video.youtube/play/?video_id=' + url
			add_link(name + ' (' + duration + ')', url, 4, thumb, fanart)
		match = re.compile('href="/results\?search_query=(.+?)".+?aria-label="Go to (.+?)"').findall(content)
		for url, name in match:
			url = 'https://www.youtube.com/results?search_query=' + url
			add_dir(name, url, 5, icon, fanart)
	else:		
		match = re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
		for url, name, thumb in match:
			add_link('[COLOR yellow]' + name + '[/COLOR]', (csn + url), 4, thumb, fanart)
		match = re.compile("href=\"(.+?)\" class=\"npage\">(\d+)<").findall(content)
		for url, name in match:
			add_dir('[COLOR cyan]Trang ' + name + '[/COLOR]', url.replace('&amp;', '&'), 5, logos + 'csn.png', fanart)  
	
	
def category(url):
	home()
	content = make_request(url)	  
	if 'chiasenhac' in url:
		add_dir('[COLOR yellow]Chia Sẻ Nhạc[B]   [COLOR lime]>[COLOR magenta]>[COLOR cyan]>[COLOR orange]>   [/B][COLOR yellow]Tìm Nhạc[/COLOR]', csn, 1, logos + 'csn.png', fanart)		
		match = re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
		for url, name in match:
			add_dir('[COLOR lime]' + name + '[/COLOR]', csn + 'hd' + url, 3, logos + 'csn.png', fanart)
	elif 'nhaccuatui' in url:
		add_dir('[COLOR yellow]Nhạc Của Tui   [B][COLOR lime]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR yellow]Tìm Video[/COLOR]', nctm, 1, logos + 'nhaccuatui.png', fanart)
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		for url, name in match:		
			if 'Cách Mạng' in name or 'Phim' in name:
				pass
			else:	  
				add_dir('[COLOR lime]' + name + '[/COLOR]', nctm + 'mv/' + url, 3, logos + 'nct.png', fanart)
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		for url, name in match:
			if 'Phim' in name:
				add_dir('[COLOR orange]' + name + '[/COLOR]', nctm + 'mv/' + url, 3, logos + 'nhaccuatui.png', fanart)		
	elif 'timkaraoke' in url:
		add_dir('[COLOR cyan]Tìm Karaoke[B]   [COLOR cyan]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR cyan]Karaoke Search[/COLOR]', karaoke, 1, logos + 'timkaraoke.png', fanart) 
		match = re.compile('pagespeed_url_hash="1785647900".+?href="([^"]*)">([^>]+)<').findall(content)
		for url, name in match: 
			add_link('[COLOR yellow]' + name + '[/COLOR]', ('%s%s' % (karaoke, url)), 4, logos + 'timkaraoke.png', fanart)  
		match = re.compile('<\/i> <br\/>\s*<a href="([^"]*)">([^>]+)<').findall(content)
		for url, name in match: 
			add_link('[COLOR lime]' + name + '[/COLOR]', ('%s%s' % (karaoke, url)), 4, logos + 'timkaraoke.png', fanart)
  
def media_list(url):
	home()
	content = make_request(url)
	if 'chiasenhac' in url:		
		match = re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
		for url, name, thumb in match:
			add_link('[COLOR yellow]' + name + '[/COLOR]', (csn + url), 4, thumb, fanart)
		match = re.compile("<a href=\"(.+?)video\/\" class=\"npage\">1<\/a>").findall(content)[0:1]
		for url in match:
			add_dir('[COLOR cyan]Trang Đầu Tiên ([COLOR lime]Nhạc Video Mới Chia Sẻ[COLOR cyan] + [COLOR orange]Download Mới Nhất[COLOR cyan])[/COLOR]', csn + url + 'video/', 3, logos + 'csn.png', fanart)
		match = re.compile("<a href=\"hd\/video\/([a-z]-video\/new[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url, name in match:
			add_dir('[COLOR lime]Trang Mới Chia Sẻ ' + name + '[/COLOR]', csn + 'hd/video/' + url + '.html', 3, logos + 'csn.png', fanart)
		match = re.compile("<a href=\"hd\/video\/([a-z]-video\/down[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url, name in match:
			add_dir('[COLOR orange]Trang Download Mới Nhất ' + name + '[/COLOR]', csn + 'hd/video/' + url + '.html', 3, logos + 'csn.png', fanart)	    	  
	elif 'nhaccuatui' in url:
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/video\/([^\"]*)\" title=\"([^\"]+)\"><img alt=\".+?\" src=\"(.*?)\"").findall(content)		
		for url, name, thumb in match:
			add_link('[COLOR yellow]' + name + '[/COLOR]', nctm + 'video/' + url, 4, thumb, fanart)
		match = re.compile("href=\"([^\"]*)\" class=\"next\" titlle=\"([^\"]+)\"").findall(content)
		for url, name in match:	
			add_dir('[COLOR cyan]' + name + '[COLOR orange]  >>>>[/COLOR]', url, 3, logos + 'nct.png', fanart)
	elif 'timkaraoke' in url:
		match = re.compile('pagespeed_url_hash="1785647900".+?href="([^"]*)">([^>]+)<').findall(content)
		for url, name in match: 
			add_link('[COLOR cyan]' + name + '[/COLOR]', ('%s%s' % (karaoke, url)), 4, logos + 'timkaraoke.png', fanart) 			
	elif 'youtube' in url:	  
		add_link('', url, 4, '', fanart)
	elif 'thuynga' in url:
		match = re.compile("style=\"background-image: url\('(.+?)'\)\">\s*<span class.+?</span>\s.+\s.+\s.+\s*<a href=\"(.+?)\">(.+?)<").findall(content)
		for thumb, url, name in match:
			add_link(name, ThuyNga + url, 4, thumb + '?.jpg', fanart)
		match = re.compile('href="http://ott.thuynga.com/([^>]+)">(\d+)<').findall(content)	
		for url, name in match:
			add_dir('[COLOR magenta]Trang ' + name + '[/COLOR]', ThuyNga + url, 3, logos + 'thuynga.png', fanart)
	
					
def resolve_url(url):
	content = make_request(url)
	if 'chiasenhac' in url:		
		try:
			media_url = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A', ':').replace('%2F', '/').replace('%2520', '%20')
		except:
			media_url = re.compile("\"file\".*?\"([^\"]*)\"").findall(content)[-1].replace('%3A', ':').replace('%2F', '/').replace('%2520', '%20')
	elif 'nhaccuatui' in url:
		media_url = re.compile("title=\".+?\" href=\"([^\"]*)\"").findall(content)[0] 
	elif 'timkaraoke' in url:
		media_url = re.compile('source src="(.+?)"').findall(content)[0].replace(' ', '%20')  
	elif 'thuynga' in url:
		media_url = re.compile("var iosUrl = '(.+?)'").findall(content)[0]  
	else:
		media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok	
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true')  
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  

params = get_params()
url = None
name = None
mode = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
  
if mode == None or url == None or len(url)<1:
	main()

elif mode == 1:
	search()	
		
elif mode == 2:
	category(url)		
		
elif mode == 3:
	media_list(url)
		
elif mode == 4:
	resolve_url(url)		

elif mode == 5:	
	search_result(url)
		
elif mode == 6:
	get_karaoke() 

elif mode == 11:
	thuy_nga()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))