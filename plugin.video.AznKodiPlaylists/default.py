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

import urllib, urllib2, re, os, sys, unicodedata
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.video.AznKodiPlaylists')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
playlistPath = xbmc.translatePath(os.path.join(home, 'resources', 'playlists'))

def removeAccents(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))

def menulist(homepath):
	try:
		mainmenu = open(homepath, 'r')  
		link = mainmenu.read()
		mainmenu.close()
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(link)
		return match
	except:
		pass	
 
def main():
	for foldername in os.listdir(playlistPath):
		add_dir(foldername, 'folderlist', 3, icon, fanart)
   
def category():
	for foldername in os.listdir(playlistPath + '/' + name):
		if 'Phim3s' in name:
			add_dir(foldername, 'folderlist', 4, logos + 'phim3s.png', fanart)
		elif 'Megabox' in name:
			add_dir(foldername, 'folderlist', 11, logos + 'megabox.png', fanart)
		elif 'Dangcaphd' in name:
			add_dir(foldername, 'folderlist', 21, logos + 'dangcaphd.png', fanart)
         
def phim3snet(name):
	if 'Phim3sLe' in name:
		add_dir('[COLOR lime]Tìm Phim3s Lẻ[/COLOR]', 'PhimLe', 1, logos + 'phim3s_search.png', fanart)
		for filename in os.listdir(playlistPath + '/Phim3s/' + name): 
			#add_dir(filename.replace('.xml', ''), filename, 5, logos + 'phim3s.png', fanart) 
			match = menulist(playlistPath + '/Phim3s/Phim3sLe/' + filename)    
			for name, url, thumbnail in match:	
				add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart) 
		
	elif 'Phim3sBo' in name:
		add_dir('[COLOR lime]Tìm Phim3s Bộ[/COLOR]', 'PhimBo', 2, logos + 'phim3s_search.png', fanart)
		for filename in os.listdir(playlistPath + '/Phim3s/' + name):
			if '3sPhimBoComplete' in filename:
				pass  
			else:    
				add_dir(filename.replace('.xml', ''), filename, 6, logos + 'phim3s.png', fanart)        
      
def phim3sle(name):
	match = menulist(playlistPath + '/Phim3s/Phim3sLe/' + name + '.xml')
	for name, url, thumbnail in match:	
		add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart)	

def phim3sbo(name):  
	match = menulist(playlistPath + '/Phim3s/Phim3sBo/' + name + '.xml')    
	for name, url, thumbnail in match:
		add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart)
		
def megaboxvn(name):
	if 'MegaboxLe' in name:
		add_dir('[COLOR lime]Tìm Megabox Phim Lẻ[/COLOR]', 'PhimLe', 1, logos + 'Megabox_search.png', fanart)
		for filename in os.listdir(playlistPath + '/Megabox/' + name): 
			match = menulist(playlistPath + '/Megabox/MegaboxLe/' + filename)  
			for name, url, thumbnail in match:	
				add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart)      
	elif 'MegaboxBo' in name:
		add_dir('[COLOR lime]Tìm Megabox Phim Bộ[/COLOR]', 'PhimBo', 2, logos + 'Megabox_search.png', fanart)
		for filename in os.listdir(playlistPath + '/Megabox/' + name):
			match = menulist(playlistPath + '/Megabox/MegaboxBo/' + filename)   
			for name, url, thumbnail in match:	
				add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart)
				        
def dangcaphd(name):
	if 'DangcaphdLe' in name:
		add_dir('[COLOR lime]Tìm Dangcaphd Phim Lẻ[/COLOR]', 'PhimLe', 1, logos + 'dangcaphd_search.png', fanart)
		for filename in os.listdir(playlistPath + '/Dangcaphd/' + name): 
			match = menulist(playlistPath + '/Dangcaphd/DangcaphdLe/' + filename)    
			for name, url, thumbnail in match:	
				add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart) 
		
	elif 'DangcaphdBo' in name:
		add_dir('[COLOR lime]Tìm Dangcaphd Phim Bộ[/COLOR]', 'PhimBo', 2, logos + 'dangcaphd_search.png', fanart)
		for filename in os.listdir(playlistPath + '/Dangcaphd/' + name):
			if 'DangcaphdBo' in filename:
				pass     
			else:
				add_dir(filename.replace('.xml', ''), filename, 22, logos + 'dangcaphd.png', fanart)

def dangcaphdbo(name): 
	match = menulist(playlistPath + '/Dangcaphd/DangcaphdBo/' + name + '.xml')  
	for name, url, thumbnail in match:	
		add_link('[COLOR yellow]' + name + '[/COLOR]', url, 99, thumbnail, fanart)
		        
def search_phimle(): 	
	try:
		keyb = xbmc.Keyboard('', '[COLOR lime]Enter search text[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')
		if 'Tìm Phim3s Lẻ' in name:
			match = menulist(playlistPath + '/Phim3s/Phim3sLe/Phim3sLeFull.xml')
			for title, url, thumbnail in match:     
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					add_link('[COLOR lime]' + title + '[/COLOR]', url, 99, thumbnail, fanart) 
		elif 'Tìm Megabox Phim Lẻ' in name:
			match = menulist(playlistPath + '/Megabox/MegaboxLe/MegaboxLe.xml')     
			for title, url, thumbnail in match:     
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					add_link('[COLOR lime]' + title + '[/COLOR]', url, 99, thumbnail, fanart) 
		elif 'Tìm Dangcaphd Phim Lẻ' in name:
			match = menulist(playlistPath + '/Dangcaphd/DangcaphdLe/DangcaphdLe.xml')    
			for title, url, thumbnail in match:     
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					add_link('[COLOR lime]' + title + '[/COLOR]', url, 99, thumbnail, fanart)
		
	except:
		pass

def search_phimbo(): 	
	try:
		keyb = xbmc.Keyboard('', '[COLOR lime]Enter search text[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText()).replace('+', ' ')
		if 'Tìm Phim3s Bộ' in name: 
			match = menulist(playlistPath + '/Phim3s/Phim3sBo/3sPhimBoComplete.xml')      
			for title, url, thumbnail in match:     
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					add_link('[COLOR yellow]' + title + '[/COLOR]', url, 99, thumbnail, fanart)  
		elif 'Tìm Megabox Phim Bộ' in name: 
			match = menulist(playlistPath + '/Megabox/MegaboxBo/MegaboxBo.xml')      
			for title, url, thumbnail in match:     
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					add_link('[COLOR yellow]' + title + '[/COLOR]', url, 99, thumbnail, fanart) 
		elif 'Tìm Dangcaphd Phim Bộ' in name: 
			match = menulist(playlistPath + '/Dangcaphd/DangcaphdBo/DangcaphdBo.xml')       
			for title, url, thumbnail in match:     
				if re.search(searchText, removeAccents(title.replace('Đ', 'D')), re.IGNORECASE):
					add_link('[COLOR yellow]' + title + '[/COLOR]', url, 99, thumbnail, fanart)
		
	except:
		pass
  
def resolve_url():
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

if mode == None or url == None or len(url) < 1:
	main()

elif mode == 1:
	search_phimle()

elif mode == 2:
	search_phimbo()
  
elif mode == 3:
	category()  

elif mode == 4:
	phim3snet(name)

elif mode == 5:
	phim3sle(name)

elif mode == 6:
	phim3sbo(name)

elif mode == 11:
	megaboxvn(name)

elif mode == 21:
	dangcaphd(name)

elif mode == 22:
	dangcaphdbo(name)
  
elif mode == 99:
	resolve_url()
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))