# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
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

mysettings = xbmcaddon.Addon(id = 'plugin.video.netmedia')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
home_menu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists', 'menulist.xml'))
prog_menu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists', 'ProgMenu.xml'))
dict = {'&amp;':'&', '&quot;':'"', '.':' ', '&#39':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...'}

def menu_list():
	try:
		mainmenu = open(home_menu, 'r')  
		link = mainmenu.read()
		mainmenu.close()
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(link)
		return match
	except:
		pass	
		
def replace_all(text, dict):
	try:
		for a, b in dict.iteritems():
			text = text.replace(a, b)
		return text
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
		elif hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
			
def home():
	add_dir('[COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[COLOR yellow]  Home  [COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[/COLOR]', '', None, icon, fanart)
		
def main():
	add_dir('[COLOR cyan]Youtube Search[/COLOR]', 'youtube', 90, logos + 'YTSearch.png', fanart)
	add_dir('[COLOR lime]Dailymotion Search[/COLOR]', 'dailymotion', 90, logos + 'DMSearch.png', fanart)	
	for title, url, thumb in menu_list():
		if 'Main Menu - ' in title:  
			add_dir(title.replace('Main Menu - ', ''), url, 2, logos + thumb, fanart)
		elif 'Main Menu Plus - ' in title:  
			add_dir(title.replace('Main Menu Plus - ', ''), url, 1, logos + thumb, fanart)	
		elif 'Main Menu learn_kodi - ' in title:  
			add_dir(title.replace('Main Menu learn_kodi - ', ''), url, 8, logos + thumb, fanart)			

def search():
	try:
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText())
		if 'Youtube Search' in name:  
			url = 'https://www.youtube.com/results?search_query=' + searchText
			search_result(url)
		elif 'Dailymotion Search' in name:  
			url = 'http://www.dailymotion.com/relevance/universal/search/'+ searchText +'/1'
			search_result(url)			
	except:
		pass

def search_result(url):
	home()
	if 'youtube' in url:
		content = make_request(url)
		match = re.compile('href="/watch\?v=(.+?)" class=".+?" data-sessionlink=".+?" title="(.+?)".+?Duration: (.+?).</span>').findall(content)
		for url, name, duration in match:
			name = replace_all(name, dict)
			thumb = 'https://i.ytimg.com/vi/' + url + '/mqdefault.jpg'
			url = 'plugin://plugin.video.youtube/play/?video_id=' + url
			add_link(name + ' (' + duration + ')', url, 4, thumb, fanart)
		match = re.compile('href="/results\?search_query=(.+?)".+?aria-label="Go to (.+?)"').findall(content)
		for url, name in match:
			url = 'https://www.youtube.com/results?search_query=' + url
			add_dir('[COLOR cyan]' + name + '[/COLOR]', url, 91, logos + 'YTSearch.png', fanart)
	elif 'dailymotion' in url:
		content = make_request(url)
		match = re.compile('data-xid="(.+?)">\s*\s*\s*<div class=".+?duration">\s*(.+?)\s*</div>\s*\s*\s*\s*\s*\s*\s*<img class.+?title="(.+?)".+?data-src="(.+?)"').findall(content)
		for url, duration, name, thumb in match:
			name = replace_all(name, dict)
			url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + url
			add_link(name + ' (' + duration + ')', url, 4, thumb, fanart)
		match = re.compile('href="(.+?)"\s*class=".+?"> (\d+)<').findall(content)
		for url, name in match:
			url = 'http://www.dailymotion.com' + url
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', url, 91, logos + 'DMSearch.png', fanart)			
		
def learn_kodi():
	home()
	myxml = open(prog_menu, 'r')  
	link = myxml.read()
	myxml.close()
	if '<channel>' in link:
		match = re.compile('<channel>\s*<name>(.+?)</name>').findall(link)
		for channel_name in match:
			add_dir(channel_name, 'progmenu', 9, iconimage, fanart)
	else:
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(link)
		for title, url, thumb in match:
			if len(thumb) > 0:
				add_link(title, url, 4, thumb, fanart) 
			else:	
				add_link(title, url, 4, iconimage, fanart)
		
def play_tutorial(name):
	home()
	myxml = open(prog_menu, 'r')  
	link = myxml.read()
	myxml.close()
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(link)	
	for vlink in match:
		final_link = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(vlink)
		for title, url, thumb in final_link:
			if len(thumb) <= 0:
				add_link(title, url, 4, iconimage, fanart)
			else:
				add_link(title, url, 4, thumb, fanart)
	
def directory():
	home()
	add_dir('Tin Tức & TV Hải Ngoại', url, 2, logos + 'haingoai.png', fanart)
	add_dir('Tin Tức & TV Trong Nước', url, 2, logos + 'vietnam.png', fanart)
		
def category(url):
	home()
	for title, url, thumb in menu_list():
		if 'Tôn Giáo' in name:   
			if 'Religion - ' in title:	
				add_dir(title.replace('Religion - ', ''), url, 3, thumb, fanart)      
		elif "thanh51's collection" in name:
			if 'thanh51 - ' in title:
				add_dir(title.replace('thanh51 - ', ''), url, 3, thumb, fanart)			
		elif 'Tin Tức & TV Hải Ngoại' in name:
			if 'OverseaNews - ' in title:	
				add_dir(title.replace('OverseaNews - ', ''), url, 3, thumb, fanart)
		elif 'Tin Tức & TV Trong Nước' in name:
			if 'NewsInVN - ' in title:	
				add_dir(title.replace('NewsInVN - ', ''), url, 3, thumb, fanart)  
		elif 'Thiếu Nhi' in name:
			if 'Children - ' in title:	
				add_dir(title.replace('Children - ', ''), url, 3, thumb, fanart)
		elif 'Ca Nhạc' in name:
			if 'Music - ' in title:	
				add_dir(title.replace('Music - ', ''), url, 3, thumb, fanart)
		elif 'Hát Karaoke' in name:
			if 'Karaoke - ' in title:	
				add_dir(title.replace('Karaoke - ', ''), url, 3, thumb, fanart)
		elif 'Cải Lương' in name:
			if 'CailuongTV - ' in title:
				add_link(title.replace('CailuongTV - ', ''), url, 4, thumb, fanart)
			elif 'Cailuong - ' in title:	
				add_dir(title.replace('Cailuong - ', ''), url, 3, thumb, fanart)        
		elif 'Hài Kịch' in name:
			if 'Sitcom - ' in title:	
				add_dir(title.replace('Sitcom - ', ''), url, 3, thumb, fanart)
		elif 'Talk Shows' in name:
			if 'TalkShows - ' in title:	
				add_dir(title.replace('TalkShows - ', ''), url, 3, thumb, fanart)    
		elif 'TV Shows' in name:
			if 'TiviShows - ' in title:	
				add_dir(title.replace('TiviShows - ', ''), url, 3, thumb, fanart)
		elif 'Thể Thao' in name:
			if 'Sports - ' in title:	
				add_dir(title.replace('Sports - ', ''), url, 3, thumb, fanart)
		elif 'Du Lịch' in name:
			if 'Travel - ' in title:	
				add_dir(title.replace('Travel - ', ''), url, 3, thumb, fanart)
		elif 'Y Khoa' in name:
			if 'Medical - ' in title:	
				add_dir(title.replace('Medical - ', ''), url, 3, thumb, fanart)       
			elif 'Y Tế Đồng Nai' in title:
				add_dir(title.replace('Y Tế Đồng Nai - ', ''), url, 5, logos + thumb, fanart)        
		elif 'Ẩm Thực Tình Yêu' in name:
			if 'Cooking - ' in title:	
				add_dir(title.replace('Cooking - ', ''), url, 3, thumb, fanart)     	
		elif 'Trang Điểm' in name:
			if 'MakeUp - ' in title:	
				add_dir(title.replace('MakeUp - ', ''), url, 3, thumb, fanart)	
		elif 'Đọc Truyện' in name:
			if 'AudioBook - ' in title:	
				add_dir(title.replace('AudioBook - ', ''), url, 3, thumb, fanart)
		elif 'Di trú và Nhập Tịch Hoa Kỳ' in name:
			if 'Immigration - ' in title:	
				add_dir(title.replace('Immigration - ', ''), url, 3, thumb, fanart)
		elif 'America\'s Funniest Videos' in name:
			if 'AFV - ' in title:	
				add_dir(title.replace('AFV - ', ''), url, 3, thumb, fanart)
		elif 'Dicovery Channels & Animal Planet' in name:
			if 'DCAP - ' in title:	
				add_dir(title.replace('DCAP - ', ''), url, 3, thumb, fanart)       
		elif 'Những Mục Khác' in name:
			if 'Other - ' in title:	
				add_dir(title.replace('Other - ', ''), url, 3, thumb, fanart)

def medical_site(url):
	home()
	if 'www.dnrtv.org.vn' in url:
		content = make_request(url)
		match = re.compile("img src=\"([^\"]+)\" \/><\/a>\s*<a href=\"([^\"]*)\" class=\"title\">(.+?)<").findall(content)
		for thumb, url, name in match:	
			add_link(name, url, 4, thumb, fanart)
		match = re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang đầu<').findall(content)
		for url in match:	
			add_dir('[COLOR violet]Trang đầu[/COLOR]', url, 5, logos + 'dongnai.png', fanart)    
		match = re.compile('class=\'paging_normal\' href=\'([^\']+)\'>(\d+)<').findall(content)
		for url, name in match:	
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', url, 5, logos + 'dongnai.png', fanart)	
		match = re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang cuối<').findall(content)
		for url in match:	
			add_dir('[COLOR red]Trang cuối[/COLOR]', url, 5, logos + 'dongnai.png', fanart)	
		
def media_list(url):
	home()
	if 'youtube' in url:
		add_link('', url, 4, '', fanart)
	elif 'dailymotion' in url:
		try:
			url1 = url.replace('/rss/', '/playlists/')
			content1 = make_request(url1)
			match1 = re.compile('href=".+?" class="link" title="(.+?)"').findall(content1)[0]
			for name in match1[0]:		
				if name > 0 and '/1' in url:
					add_dir('[COLOR magenta]+ + + +[COLOR lime]  Playlists  [COLOR magenta]+ + + +[/COLOR]', url1, 6, iconimage, fanart)	
		except:
			pass
		content = make_request(url)		
		match = re.compile('<title>(.+?)<\/title>\s*<link>(.+?)_.+?<\/link>\s*<description>.+?src="(.+?)"').findall(content)
		for name, url, thumb in match:
			name = replace_all(name, dict)    
			url = url.replace('http://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=')	  
			add_link(name, url, 4, thumb, fanart)
		match = re.compile('<dm:link rel="next" href="(.+?)"').findall(content)
		for url in match:  
			add_dir('[COLOR lime]Trang kế  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]', url, 3, icon, fanart)	
		
def DailyMotion_playlist(url):
	home()
	content = make_request(url)
	match = re.compile('href="(.+?)" class="link" title="(.+?)"').findall(content)
	for url, name in match:
		name = replace_all(name, dict)
		add_dir(name, 'http://www.dailymotion.com/rss' + url, 7, iconimage, fanart)
	match = re.compile('href="(.+?)"\s*class=".+?"> (\d+)<').findall(content)	
	for url, name in match:  
		add_dir("[COLOR lime]Playlists  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>  [COLOR lime]Page " + name + "[/COLOR]" , "http://www.dailymotion.com" + url, 6, icon, fanart)

def DailyMotion_playlist_medialist(url):
	home()
	content = make_request(url)
	match = re.compile('<title>(.+?)<\/title>\s*<link>(.+?)_.+?<\/link>\s*<description>.+?src="(.+?)"').findall(content)
	for name, url, thumb in match:
		name = replace_all(name, dict)    
		url = url.replace('http://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=')	  
		add_link(name, url, 4, thumb, fanart)
	match = re.compile('<dm:link rel="next" href="(.+?)"').findall(content)
	for url in match:  
		add_dir('[COLOR lime]Playlists  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>  [COLOR lime]Next page[/COLOR]', url, 7, icon, fanart)	
				
def resolve_url(url):
	if 'www.dnrtv.org.vn' in url:
		content = make_request(url)
		media_url = re.compile("url: '(.+?)mp4'").findall(content)[0] + 'mp4'       
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
iconimage = None

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
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url) < 1:
	main()
  
elif mode == 1: 
	directory()  
  
elif mode == 2:
	category(url)  

elif mode == 3:
	media_list(url)
   
elif mode == 4:
	resolve_url(url)

elif mode == 5:
	medical_site(url)  

elif mode == 6:	
	DailyMotion_playlist(url)
	
elif mode == 7:
	DailyMotion_playlist_medialist(url)
	
elif mode == 8:	
	learn_kodi()

elif mode == 9:	
	play_tutorial(name)

elif mode == 90:	
	search()

elif mode == 91:	
	search_result(url)	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))