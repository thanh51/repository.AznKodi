import CommonFunctions as common
import urllib
import urllib2
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import urlfetch
import re
import json
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.hdplay')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
thumbnails = xbmc.translatePath( os.path.join( home, 'thumbnails\\' ) )

def _makeCookieHeader(cookie):
	cookieHeader = ""
	for value in cookie.values():
			cookieHeader += "%s=%s; " % (value.key, value.value)
	return cookieHeader

def make_request(url, headers=None):
	if headers is None:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
								 'Referer' : 'http://www.google.com'}
	try:
			req = urllib2.Request(url,headers=headers)
			f = urllib2.urlopen(req)
			body=f.read()
			return body
	except urllib2.URLError, e:
			print 'We failed to open "%s".' % url
			if hasattr(e, 'reason'):
					print 'We failed to reach a server.'
					print 'Reason: ', e.reason
			if hasattr(e, 'code'):
					print 'We failed with error code - %s.' % e.code
def get_fpt():	

        def home():

		req = urllib2.Request(fptplay)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.4) Gecko/2008092417 Firefox/4.0.4')
		response = urllib2.urlopen(req, timeout=90)
		link=response.read()
		response.close()
		match=re.compile("<li ><a href=\"(.+?)\" class=\".+?\">(.+?)<\/a><\/li>").findall(link)
		for url,name in match:
				if 'livetv' in url:
						addDir('[COLOR yellow]' + name + '[/COLOR]',fptplay + url,3,logos + 'fptplay.png')
				else:
						addDir('[COLOR lime]' + name + '[/COLOR]',fptplay + url,1,icon)	


	    
	content = make_request('http://play.fpt.vn/livetv/')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', {'class' : 'channel_link'})
	for item in items:
		img = item.find('img')
		if img is not None:
			try:
				add_link('', item['channel'], 0, 'http://play.fpt.vn' + item['href'], img['src'], '')
			except:
				pass

#add_dir(name,url,mode,iconimage,query='',type='f',page=0):
def get_vtc_movies(url, query='25', type='', page=0):
	if url == '':
		content = make_request('http://117.103.206.21:88/Movie/GetMovieGenres?device=4')
		result = json.loads(content)
		for item in result:
			add_dir(item["Name"], 'http://117.103.206.21:88/Movie/GetMoviesByGenre?device=4&genreid=' + str(item["ID"]) + '&start=0&length=25', 11, '', '25', str(item["ID"]), 0)
	if 'GetMoviesByGenre' in url:
		content = make_request(url)
		result = json.loads(content)
		for item in result:
			add_link('', item["Title"], 0, 'http://117.103.206.21:88/Movie/GetMovieStream?device=4&path=' + item["MovieUrls"][0]["Path"].replace('SD', 'HD'), item["Thumbnail3"], item["SummaryShort"])
		add_dir('Next', 'http://117.103.206.21:88/Movie/GetMoviesByGenre?device=4&genreid=' + type + '&start=' + str(int(query)+page) + '&length=' + str(query), 11, '', str(int(query)+page), type, page)
	
def get_vtc(url = None):
	content = make_request(url)
	
	result = json.loads(content)
	for item in result:
		path = item["ChannelUrls"][0]["Path"]
		if 'http' in path:
			add_link('', item["Name"], 0, item["ChannelUrls"][0]["Path"], item["Thumbnail2"], '')
		else:
			add_link('', item["Name"], 0, "http://117.103.206.21:88/channel/GetChannelStream?device=4&path=" + item["ChannelUrls"][0]["Path"], item["Thumbnail2"], '')

def get_hdonline(url = None):
	if url == '':
		content = make_request('http://old.hdonline.vn/')
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.find('div',{'id' : 'full-mn-phim-le'}).findAll('a')
		for item in items:
			href = item.get('href')
			if href is not None:
				try:
					add_dir(item.text, href, 13, thumbnails + 'HDOnline.png', query, type, 0)
				except:
					pass
		return
	if 'xem-phim' in url:	
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.findAll('ul', {'class' : 'clearfix listmovie'})[1].findAll('li')
		for item in items:
			a = item.find('a')
			img = item.find('img')
			span = item.find('span',{'class' : 'type'})
			href = a.get('href')
			if href is not None:
				try:
					if span is not None:
						add_dir(a.get('title') + ' (' + span.text + ')', href, 9, a.img['src'], '', '', 0)
					else:	
						add_link('', a.get('title'), 0, href, img['src'], '')
				except:
					pass
		items = soup.find('div',{'class' : 'pagination pagination-right'})
		if items is not None:
			for item in items.findAll('a'):
				a = item
				href = a.get('href')
				if href is not None:
					try:
						add_dir(a.get('title'), href, 9, thumbnails + 'zui.png', '', '', 0)
					except:
						pass
		
def get_zui(url = None):
	if url == '':
		content = make_request('http://zui.vn')
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.find('div',{'class' : 'span8 visible-desktop visible-tablet'}).findAll('a')
		for item in items:
			href = item.get('href')
			if href is not None:
				try:
					add_dir(item.text, href, 9, thumbnails + 'zui.png', query, type, 0)
				except:
					pass
		return
	if 'the-loai' in url or 'phim-' in url:	
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		groups = soup.find('ul', {'class' : 'group'})
		if groups is not None:
			for item in groups.findAll('a'):
				matchObj = re.match( r'change_group_chapter\((\d+),(\d+),(\d+)\)', item['onclick'], re.M|re.I)
				response = urlfetch.fetch(
			url = 'http://zui.vn/?site=movie&view=show_group_chapter',
			method ='POST',
			data = {
				"pos": matchObj.group(1),
				"movie_id": matchObj.group(2),
				"type": matchObj.group(3)
			}
		)
				soup = BeautifulSoup(str(response.content), convertEntities=BeautifulSoup.HTML_ENTITIES)
				for item in soup.findAll('a'):
					add_link('', u'T?p ' + item.text, 0, 'http://zui.vn/' + item['href'], thumbnails + 'zui.png', '')
		else:
			items = soup.find('ul',{'class' : 'movie_chapter'})
			if items is not None:
				for item in items.findAll('a'):
					a = item
					href = a.get('href')
					if href is not None:
						try:
							add_link('', u'T?p ' + a.text, 0, 'http://zui.vn/' + href, thumbnails + 'zui.png', '')
							#add_dir(u'T?p ' + a.text, 'http://zui.vn/' + href, 9, thumbnails + 'zui.png', '', '', 0)
						except:
							pass
			else:
				items = soup.findAll('div',{'class' : 'poster'})
				for item in items:
					a = item.find('a')
					span = item.find('span',{'class' : 'type'})
					href = a.get('href')
					if href is not None:
						try:
							if span is not None:
								add_dir(a.get('title') + ' (' + span.text + ')', href, 9, a.img['src'], '', '', 0)
							else:	
								add_link('', a.get('title'), 0, href, a.img['src'], '')
						except:
							pass
				items = soup.find('div',{'class' : 'pagination pagination-right'})
				if items is not None:
					for item in items.findAll('a'):
						a = item
						href = a.get('href')
						if href is not None:
							try:
								add_dir(a.get('title'), href, 9, thumbnails + 'zui.png', '', '', 0)
							except:
								pass
	else:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		groups = soup.find('ul', {'class' : 'group'})
		if groups is not None:
			for item in groups.findAll('a'):
				matchObj = re.match( r'change_group_chapter\((\d+),(\d+),(\d+)\)', item['onclick'], re.M|re.I)
				response = urlfetch.fetch(
			url = 'http://zui.vn/?site=movie&view=show_group_chapter',
			method ='POST',
			data = {
				"pos": matchObj.group(1),
				"movie_id": matchObj.group(2),
				"type": matchObj.group(3)
			}
		)
				soup = BeautifulSoup(str(response.content), convertEntities=BeautifulSoup.HTML_ENTITIES)
				for item in soup.findAll('a'):
					add_link('', u'T?p ' + item.text, 0, 'http://zui.vn/' + item['href'], thumbnails + 'zui.png', '')
			return
	
		items = soup.find('ul',{'class' : 'movie_chapter'})
		if items is not None:
			for item in items.findAll('a'):
				a = item
				href = a.get('href')
				if href is not None:
					try:
						add_link('', u'T?p ' + a.text, 0, 'http://zui.vn/' + href, thumbnails + 'zui.png', '')
						#add_dir(u'T?p ' + a.text, 'http://zui.vn/' + href, 9, thumbnails + 'zui.png', '', '', 0)
					except:
						pass
	
def get_fpt_other(url):
	content = make_request(url)
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a')
	for item in items:
		href = item.get('href')
		if href is not None and 'the-loai-more' in href and 'Xem' not in item.text:
			try:
				add_dir(item.text, 'http://play.fpt.vn' + href, 8, thumbnails + 'fptplay.jpg', query, type, 0)
			except:
				pass

def get_fpt_tvshow_cat(url):
	content = make_request(url)
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	if url is not None and '/Video/' not in url:
		items = soup.findAll('div', {'class' : 'col'})
		for item in items:
			img = item.a.img['src']
			href = item.a['href']
			text = item.a.img['alt']	
			try:
				add_dir(text, 'http://play.fpt.vn' + href, 8, img, '', '', 0)
			except:
				pass

	items = soup.find('ul', {'class' : 'pagination pagination-sm'}).findAll('a')
	for item in items:
		href = ''
		href = item.get('href')
		if href is not None and 'the-loai-more' in href and 'Xem' not in item.text:
			try:
				add_dir('Trang ' + item.text, 'http://play.fpt.vn' + href, 8, thumbnails + 'fptplay.jpg', query, type, 0)
			except:
				pass
		if href is not None and '/Video/' in href:
			try:
				add_link('', u'T?p ' + item.text, 0, 'http://play.fpt.vn' + href, thumbnails + 'fptplay.jpg', '')
			except:
				pass
		
def get_htv():
	content = make_request('http://www.htvonline.com.vn/livetv')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', {'class' : 'mh-grids5-img'})
	for item in items:
		img = item.find('img')
		if img is not None:
			try:
				add_link('', item['title'], 0, item['href'], img['src'], '')
			except:
				pass

		
def get_categories():

	add_link('', '[COLOR cyan]*****************TH Dành cho người Việt ở nước ngoài****************[/COLOR]', 0, '', thumbnails + '', '')
	
	add_link('', '[COLOR lime]*******ZTV *******[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VTV3 HD ', 0, 'http://123.30.184.172:1935/livez3/smil:vtv3hd.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VTV6 HD ', 0, 'http://123.30.184.172:1935/livez3/smil:vtv6hd.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VTC1 HD ', 0, 'http://123.30.184.172:1935/livez3/smil:vtchd1.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VTC HD3', 0, 'http://123.30.184.172:1935/livez3/smil:vtchd3.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VTC3 HD', 0, 'http://123.30.184.172:1935/livez3/smil:vtc3hd.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'HBO HD ', 0, 'http://123.30.184.172:1935/livez3/smil:hbo.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'DISCOVERY WORLD HD ', 0, 'http://123.30.184.172:1935/livez3/smil:discovery.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'FASHIONTV HD', 0, 'http://123.30.184.172:1935/livez3/smil:fashion.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'DISNEY HD', 0, 'http://123.30.184.172:1935/livez3/smil:disneyhd.smil/playlist.m3u8', thumbnails + '', '')
	add_link('', 'FOX SPORT HD', 0, 'http://123.30.184.172:1935/livez3/smil:foxplus.smil/playlist.m3u8', thumbnails + '', '')
	
	add_link('', '[COLOR lime]*******VP9 ******[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VTV1', 0, 'http://2co1.vp9.tv/chn/vtv1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV2', 0, 'http://2co1.vp9.tv/chn/vtv2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV3 HD', 0, 'http://2co1.vp9.tv/chn/vtv3/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV4', 0, 'http://2co1.vp9.tv/chn/vtv4/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTV6 HD', 0, 'http://2co1.vp9.tv/chn/vtv6/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'ANTV', 0, 'http://2co1.vp9.tv/chn/antv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'QPVN', 0, 'http://2co1.vp9.tv/chn/qpvn/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VOVTV', 0, 'http://2co1.vp9.tv/chn/vovtv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'TTXVN', 0, 'http://2co1.vp9.tv/chn/ttxvn/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB2', 0, 'http://2co1.vp9.tv/chn/phimv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB5', 0, 'http://2co1.vp9.tv/chn/echannel/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB7', 0, 'http://2co1.vp9.tv/chn/ddra/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB8', 0, 'http://2co1.vp9.tv/chn/bibi/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB10', 0, 'http://2co1.vp9.tv/chn/o2tv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HN1', 0, 'http://2co1.vp9.tv/chn/hn1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HN2', 0, 'http://2co1.vp9.tv/chn/hn2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HTV7', 0, 'http://2co1.vp9.tv/chn/htv7/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'HTV9', 0, 'http://2co1.vp9.tv/chn/htv9/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC1', 0, 'http://2co1.vp9.tv/chn/vtc1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC2', 0, 'http://2co1.vp9.tv/chn/vtc2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC3', 0, 'http://2co1.vp9.tv/chn/vtc3/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC6', 0, 'http://2co1.vp9.tv/chn/sgc6/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC7', 0, 'http://2co1.vp9.tv/chn/tdayt/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC9', 0, 'http://2co1.vp9.tv/chn/letsv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC11', 0, 'http://2co1.vp9.tv/chn/kids/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC13 ITV', 0, 'http://2co1.vp9.tv/chn/itvvn/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC16', 0, 'http://2co1.vp9.tv/chn/3ntv/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'DRT1', 0, 'http://2co1.vp9.tv/chn/drt1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'BTV1', 0, 'http://2co1.vp9.tv/chn/btv1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'THVL1', 0, 'http://2co1.vp9.tv/chn/vl1/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	add_link('', 'THVL2', 0, 'http://2co1.vp9.tv/chn/vl2/v.m3u8|User-Agent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/39.0.2171.65%20Safari/537.36', thumbnails + '', '')
	
	add_link('', '[COLOR lime]******VTV PLay *******[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VTV1', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:vtv1sd_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + 'VTV1.jpg', '')
	add_link('', 'VTV3', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:vtv3sd_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + 'VTV3 HD.jpg', '')
	add_link('', 'VTV6', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:vtv6sd_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + 'VTV6 HD.jpg', '')
	add_link('', 'VTVCAB1', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:giaitritv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB2', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:phimviet_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
        add_link('', 'VTVCAB3 THETHAOTV', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:thethaotvsd_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
        add_link('', 'VTVCAB4', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:kenh17_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB5', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:echanel_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB6', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:haytv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB7', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:ddramas_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB8', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:bibi_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB9', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:infotv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB10', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:o2tv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB12', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:styletv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB15', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:investtv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB16 BONGDATV', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:bongdatvsd_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTVCAB17', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:yeah1tv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
        add_link('', 'HANOI 1', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:hanoi1_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
        add_link('', 'HTV9', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:htv9_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'HTVC PHU NU', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:htvcphunu_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC7', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:todaytv_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'VTC9', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:letsviet_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'SCTVHD HAI(720P)', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:sctvhaihd_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'ARIANG', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:arirang_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'KBS', 0, 'http://vtv.live.cdn.fptplay.net/vtvlive/smil:kbs_hls.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')

	add_link('', '[COLOR lime]***********LIFETV ********[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'LIFETV ', 0, 'rtmp://27.118.16.16/live/live_lifetv', thumbnails + '', '')
	add_link('', 'KÊNH 9 MUSIC ', 0, 'rtmp://27.118.16.16/live//9_music', thumbnails + '', '')
	add_link('', 'FITNESS 360 ', 0, 'rtmp://27.118.16.16/live//fitness_360', thumbnails + '', '')
	add_link('', 'MODEL CHANNEL ', 0, 'rtmp://27.118.16.16/live//model_channel', thumbnails + '', '')
	add_link('', 'DI SẢN VIỆT ', 0, 'rtmp://27.118.16.16/live//disanviet', thumbnails + '', '')
	add_link('', '4 MEN ', 0, 'rtmp://27.118.16.16/live//4Men', thumbnails + '', '')
	add_link('', '2CHANNEL VN ', 0, 'rtmp://27.118.16.16/live//2channel', thumbnails + '', '')
	add_link('', 'SOTV ', 0, 'rtmp://27.118.16.16/live//sotv', thumbnails + '', '')
	add_link('', 'TECH CHANNEL ', 0, 'rtmp://27.118.16.16/live//tech', thumbnails + '', '')
	add_link('', 'KÊNH 911 ', 0, 'rtmp://27.118.16.16/live//911', thumbnails + '', '')
	add_link('', 'TRUYỀN THÔNG VIỆT ', 0, 'rtmp://27.118.16.16/live//ttv', thumbnails + '', '')
	add_link('', 'NLĐ ', 0, 'http://222.255.27.218:8081/nld.m3u8', thumbnails + '', '')

	add_link('', '[COLOR lime]*********ACCESSASIA********[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VTV4 ', 0, 'http://tvod.accessasia.tv:8080/live/vtv4.480p/index.m3u8', thumbnails + '', '')
	add_link('', 'VTVcab1 ', 0, 'http://tvod.accessasia.tv:8080/live/vctv1.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'VTVcab2 ', 0, 'http://tvod.accessasia.tv:8080/live/vctv2.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'VTVcab4 ', 0, 'http://tvod.accessasia.tv:8080/live/vctv4.480p/index.m3u8', thumbnails + '', '')
	add_link('', 'VTVcab8 ', 0, 'http://tvod.accessasia.tv:8080/live/vctv8.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'VTVcab10 ', 0, 'http://tvod.accessasia.tv:8080/live/vctv10.480p/index.m3u8', thumbnails + '', '')
	add_link('', 'VTVcab17 ', 0, 'http://tvod.accessasia.tv:8080/live/vctv17.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'HTVC DU LICH ', 0, 'http://tvod.accessasia.tv:8080/live/dulichcuocsong.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'HTVC THUAN VIET ', 0, 'http://tvod.accessasia.tv:8080/live/thuanviet.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'HTVC FBNC ', 0, 'http://tvod.accessasia.tv:8080/live/htvcfbnc.480p/htvcfbnc/index.m3u8', thumbnails + '', '')
        add_link('', 'SCTVHD-HAI ', 0, 'http://tvod.accessasia.tv:8080/live/sctvhaihd.480p/index.m3u8', thumbnails + '', '')
        add_link('', 'SCTV14 ', 0, 'http://tvod.accessasia.tv:8080/live/sctv14.480p/index.m3u8', thumbnails + '', '')

	add_link('', '[COLOR lime]******** HẢI NGOẠI ********[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'KVLA', 0, 'http://206.190.140.142/liveStream/kvla_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VZN TV Houston TX', 0, 'http://206.190.136.254/liveStream/vantv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VietV LA', 0, 'http://206.190.140.142/liveStream/vietvla_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VietV Houston TX', 0, 'http://hls12.las.v247tv.com:8081/live/vietv-oc1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VPop TV', 0, 'http://206.190.136.254/liveStream/vpoptv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VNA TV', 0, 'http://206.190.140.142/liveStream/vnatv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VietFace TV', 0, 'http://206.190.140.142/liveStream/vface_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VietFace TV Houston TX', 0, 'http://hls12.las.v247tv.com:8081/live/vietv-hou1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'SET 57.4', 0, 'http://206.190.140.142:1935/liveStream/set_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Little Saigon TV 57.7', 0, 'http://206.190.140.142/liveStream/lstv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'IBC TV', 0, 'http://206.190.140.142:1935/liveStream/ibctv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'MTV Viet TV', 0, 'http://206.190.140.142/liveStream/mtv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Viet Media TV', 0, 'http://206.190.140.142/liveStream/viettv24_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'CaiLuong TV', 0, 'http://206.190.136.254/liveStream/cailuong_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Hai TV', 0, 'http://206.190.140.142/liveStream/hai_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Tuoi Than Tien TV', 0, 'http://206.190.140.142/liveStream/ttt_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VietSun TV', 0, 'http://206.190.136.254/liveStream/vietsuntv_1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Pho Viet TV', 0, 'http://69.178.181.93:1935/phoviettv/myStream/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VBS 57.6', 0, 'http://uni6rtmp.tulix.tv:1935/vbstv/vbsabr.smil/chunklist.m3u8', thumbnails + '', '')
	add_link('', 'VSTAR Television', 0, 'http://origin.onworldtv.com:1935/liveorigin/vstartv/chunklist_w228688581_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2MjQ1JndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDA4NDUmd29ybGR0b2tlbmhhc2g9LXlBOUoxb29IZ2pMTlBWbEZjcVFtUXRSVEpNeWNyWU1oQ0lWUG9BNVl0az0=.m3u8', thumbnails + '', '')
	add_link('', 'vietnamese american network', 0, 'http://origin.onworldtv.com:1935/liveorigin/van/chunklist_w1237319353_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2NTM5JndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDExMzkmd29ybGR0b2tlbmhhc2g9c1FRbUE3VU5laXoyMDJ6SHpTZ2otbl9iR2QtLTBGQ1pERDF2UEZlVHFWMD0=.m3u8', thumbnails + '', '')
	add_link('', 'Viet USA Television', 0, 'http://origin.onworldtv.com:1935/liveorigin/vus/chunklist_w957481003_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2NDU3JndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDEwNTcmd29ybGR0b2tlbmhhc2g9cTZGeV9UdnBjQUR4cDhlX0lnRTQyNmlXUTRlX19nQmtRd2h5ZEl1a1hRdz0=.m3u8', thumbnails + '', '')
	add_link('', 'Film 24 Gio Television', 0, 'http://origin.onworldtv.com:1935/liveorigin/film24/chunklist_w1980697456_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2MzgzJndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDA5ODMmd29ybGR0b2tlbmhhc2g9cmNTTTNQeXdOdkNZUFRrU1R1WjZHMkFYVS1BY3plNFgwekxLeGRkUERaWT0=.m3u8', thumbnails + '', '')
	add_link('', 'Cuoi 24 Gio Television', 0, 'http://origin.onworldtv.com:1935/liveorigin/laugh24/chunklist_w1030335260_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2MzQ3JndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDA5NDcmd29ybGR0b2tlbmhhc2g9Y1JTdnBHWEpoYVZNRHppLXQwN21SWnNkdklyR0xncGs2OVBZd1BiX0ppQT0=.m3u8', thumbnails + '', '')
	add_link('', 'Little Saigon', 0, 'http://origin.onworldtv.com:1935/liveorigin/lstv/chunklist_w2039022998_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2NjA3JndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDEyMDcmd29ybGR0b2tlbmhhc2g9Ni0xWG5zTlAzcnZkQlRzeXYwR3RUai1ZdWwyeW5GSUMxWkw2MHlEVXhqMD0=.m3u8', thumbnails + '', '')
	add_link('', 'Sai Gon Network', 0, 'http://origin.onworldtv.com:1935/liveorigin/sgn/chunklist_w942043689_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2NjUxJndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDEyNTEmd29ybGR0b2tlbmhhc2g9dzNCdXB1NVpacjJDYVg1LUxhOGlCOTdlNDFkNG5PbWlpeE90bGEwbXRkQT0=.m3u8', thumbnails + '', '')
	
	add_link('', '[COLOR lime]*******THÚY NGA PARIS BY NIGHT *********[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 100 GHI NHỚ MỘT CHẶNG ĐƯỜNG P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Thuy.Nga.100.Ghi.Nho.Mot.Chang.Duong..Disk01.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 100 GHI NHỚ MỘT CHẶNG ĐƯỜNG P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Thuy.Nga.100.Ghi.Nho.Mot.Chang.Duong..Disk02.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 101 HẠNH PHUC ĐẦU NĂM', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Thuy.Nga.101_HanhPhucDauNam.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 102 TÌNH CA LAM PHƯƠNG', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Thuy.Nga.102_Nhacyeucau-tinhcalamphuong.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 103 TÌNH SỬ TRONG ÂM NHẠC', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Thuy.Nga.103_TinhsutrongamnhacViet.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 104 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.104_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 104 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.104_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 104 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.104_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 105 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.105_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 105 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.105_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 105 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.105_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 106 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.106_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 106 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.106_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 106 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.106_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 107 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.107_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 107 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.107_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 107 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.107_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 108 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.108_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 108 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.108_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 108 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.108_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 109 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.109_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 109 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.109_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 109 P3', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.109_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 110 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.110_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 110 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.110_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 110 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.110_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 111 P1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.111_001.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 111 P2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.111_002.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 111 P3 END', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.111_003.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 112 CHỦ ĐỀ "ĐÔNG" DISC 1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.112.Dong-fix.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 112 CHỦ ĐỀ "ĐÔNG" DISC 2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.112.Dong_2.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 112 CHỦ ĐỀ "ĐÔNG" DISC 3', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/ThuyNga/Paris.By.Night.112.Dong_3.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 113 MỪNG TUỔI MẸ DISK 1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/phim2015/200315/PBN.113.Disk1.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 113 MỪNG TUỔI MẸ DISK 2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/phim2015/200315/PBN.113.Disk2.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 114 - Tôi Là Người Việt Nam - Disc 1', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/phim2015/200515/Paris.By.Night.114.Toi.La.Nguoi.Viet.Nam.D1.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 114 - Tôi Là Người Việt Nam - Disc 2', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/phim2015/200515/Paris.By.Night.114.Toi.La.Nguoi.Viet.Nam.D2.mp4', thumbnails + '', '')
	add_link('', 'PARIS BY NIGHT 114 - Tôi Là Người Việt Nam - Disc 3', 0, 'http://server3.dangcaphd.com/p4R4cDQnzcUagcNa/phim2015/200515/Paris.By.Night.114.Toi.La.Nguoi.Viet.Nam.D3.mp4', thumbnails + '', '')

	add_link('', '[COLOR lime]*******Phim Veetle.com(máy chủ USA) *********[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'Columbo', 0, 'http://veetle.com/index.php/hls/streamMbrfast/51d8cf3f02188_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'All kinds of MOVIES', 0, 'http://veetle.com/index.php/hls/streamMbrfast/54f028dede2b7_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'SCI-FI  ACTION', 0, 'http://veetle.com/index.php/hls/streamMbrfast/559230410dbe0_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Teeburds Movies', 0, 'http://veetle.com/index.php/hls/streamMbrfast/555fdbe860d6e_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'HQ Bollywood', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4e0e6f4dcc2d3_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Action Movies', 0, 'http://veetle.com/index.php/hls/streamMbrfast/558ed413da95d_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'UFO Channel', 0, 'http://veetle.com/index.php/hls/streamMbrfast/5570083766031_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'The X-Files', 0, 'http://veetle.com/index.php/hls/streamMbrfast/521135971d84a_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Movies', 0, 'http://veetle.com/index.php/hls/streamMbrfast/516291ebc884b_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'HQ Bollywood', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4e2c5fd04592d_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Stinky Sci-Fi Cheese Theater', 0, 'http://veetle.com/index.php/hls/streamMbrfast/5367a2e15a717_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'The Filmmakers Channel', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4bef8c6938e15_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'AlsterLandTV-At The Drive-In', 0, 'http://veetle.com/index.php/hls/streamMbrfast/5408d7749bc24_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'War Movie', 0, 'http://veetle.com/index.php/hls/streamMbrfast/559c86246bc4e_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'filmnoirclassicchannel', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4d7fbae3b4c52_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Jefimija Televizija Krusevac', 0, 'http://veetle.com/index.php/hls/streamMbrfast/532c1eb424c27_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Sex and Sexuality', 0, 'http://veetle.com/index.php/hls/streamMbrfast/55086a95c9cf7_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'SCI-FI ORIGINAL CHANNEL', 0, 'http://veetle.com/index.php/hls/streamMbrfast/516291ebc884b_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Movie World', 0, 'http://veetle.com/index.php/hls/streamMbrfast/555f79c52d90b_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'FIREBALL CINEMA', 0, 'http://veetle.com/index.php/hls/streamMbrfast/559518fba9dc9_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'watchable Movies', 0, 'http://veetle.com/index.php/hls/streamMbrfast/52a8bf512eb59_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'filmnoirclassicchannel', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4d7fbae3b4c52_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Box_tv live', 0, 'http://veetle.com/index.php/hls/streamMbrfast/558b2427769ea_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Classic War Movies', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4e7bd4cbe3e54_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'german', 0, 'http://veetle.com/index.php/hls/streamMbrfast/53419fff5d146_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Hottronics- knowledge is key', 0, 'http://veetle.com/index.php/hls/streamMbrfast/5164884b71202_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Películas en Esp', 0, 'http://veetle.com/index.php/hls/streamMbrfast/558541e58f32a_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Star Trek TOS remastered', 0, 'http://veetle.com/index.php/hls/streamMbrfast/51e482fa02883_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'TNG', 0, 'http://veetle.com/index.php/hls/streamMbrfast/53f4d37c4b958_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Babylon 5', 0, 'http://veetle.com/index.php/hls/streamMbrfast/54f361339738a_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'THE BIBLE', 0, 'http://veetle.com/index.php/hls/streamMbrfast/555657e5b863d_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Wake Up America and World', 0, 'http://veetle.com/index.php/hls/streamMbrfast/4bd6f1473bf81_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'PopWindowTV Live Stream', 0, 'http://veetle.com/index.php/hls/streamMbrfast/517aa55bd94a7_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'automaticintl', 0, 'http://veetle.com/index.php/hls/streamMbrfast/517be3ea98d07_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Anime Livestrea 24.7', 0, 'http://veetle.com/index.php/hls/streamMbrfast/52a0adb7b6024_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	add_link('', 'Cartoon Remix', 0, 'http://veetle.com/index.php/hls/streamMbrfast/53b1f49df2730_/stream.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36', thumbnails + '', '')
	
	add_link('', '[COLOR lime]*******RADIO *********[/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VOV1', 0, 'http://210.245.60.242:1935/vov1/vov1/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VOV2', 0, 'http://210.245.60.242:1935/vov2/vov2/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VOV3', 0, 'http://210.245.60.242:1935/vov3/vov3/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Kênh XONE FM', 0, 'http://scache.fptplay.net.vn/liveshow/xonefmlive/playlist.m3u8?token=c335VydmVyX3RpbWU9MTQwMjYxNzIyNCZoYXNoX3ZhbHVl&did=NzIyNCZoYXNoX3ZhbHVl', thumbnails + '', '')
	add_link('', 'Kênh FM90Mhz - HANOITV.VN', 0, 'rtmp://vovandroid.radiovietnam.vn:1935/live/hanoi swfUrl=http://hanoi.radiovietnam.vn/media/radioplayer.swf live=1 pageUrl=http://hanoitv.vn/Media/157/Radio.htv', thumbnails + '', '')
	add_link('', 'Kênh JOYFM - HANOITV.VN', 0, 'rtmp://radio.joyfm.vn:1935/live playpath=RadioOnline swfUrl=http://hanoitv.vn/JScripts/player.swf live=1 pageUrl=http://hanoitv.vn/Media/157/Radio.htv', thumbnails + '', '')
	add_link('', 'VOH - FM 95.6 Mhz', 0, 'rtmp://221.132.38.110/live//channel1 swfUrl=http://www.voh.com.vn/jwplayer/jwplayer.flash.swf pageUrl=http://www.voh.com.vn/radio/fm-95-6-mhz-3.html#', thumbnails + '', '')
	add_link('', 'VOH - AM 610Kz', 0, 'rtmp://221.132.38.110/live//channel2 swfUrl=http://www.voh.com.vn/jwplayer/jwplayer.flash.swf pageUrl=http://www.voh.com.vn/radio/am-610khz-1.html#', thumbnails + '', '')
	add_link('', 'VOH - FM 99.9 Mhz', 0, 'rtmp://221.132.38.110:1935/live/ playpath=channel3 swfUrl=http://www.voh.com.vn/jwplayer/jwplayer.flash.swf pageUrl=http://www.voh.com.vn/radio/fm-99-9-mhz-2.html#', thumbnails + '', '')
	add_link('', 'VOV GT HN', 0, 'http://210.245.60.242:1935/vovgt/vovgt/playlist.m3u8', thumbnails + '', '')
	add_link('', 'VOV GT TP.HCM', 0, 'http://210.245.60.242:1935/vovgtsg/vovgtsg/playlist.m3u8', thumbnails + '', '')
	add_link('', 'Nationwide Viet Radio (NVR)', 0, 'http://vndcradio2.serverroom.us:4480/', thumbnails + '', '')
	add_link('', 'Sai Gon Network Radio', 0, 'http://origin.onworldtv.com:1935/liveorigin/sgn_aud/chunklist_w1625237777_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU3MDUwJndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDE2NTAmd29ybGR0b2tlbmhhc2g9Nk1id0ViZEplQjI5dU5GT2xXaG1lSVltSWprOXJZbk5aYkdNVndQTEpxZz0=.m3u8', thumbnails + '', '')
	add_link('', 'Little Saigon Radio', 0, 'http://origin.onworldtv.com:1935/liveorigin/lstv_aud/chunklist_w1228284842_tkd29ybGR0b2tlbnN0YXJ0dGltZT0xNDM0MzU2Nzk0JndvcmxkdG9rZW5lbmR0aW1lPTE0MzQ0NDEzOTQmd29ybGR0b2tlbmhhc2g9X3dCeXhGU09TLWtGd2RISEREd2JLNDBiWkhfSy1CdG41UVZ1c3RVYUNydz0=.m3u8', thumbnails + '', '')
	add_link('', 'Cherry radio - Tin tức.giải trí', 0, 'http://50.7.96.210:8618/;stream.mp3', thumbnails + '', '')
	add_link('', 'Cherry radio - Nhạc trẻ', 0, 'http://199.189.111.28:8226/;stream.mp3', thumbnails + '', '')
	add_link('', 'Cherry radio - Nhạc trữ tình', 0, 'http://174.37.252.208:8500/;stream.mp3', thumbnails + '', '')
	add_link('', 'VOA NEWS', 0, 'mms://a823.l211056822.c2110.g.lm.akamaistream.net/D/823/2110/v0001/reflector:56822', thumbnails + '', '')
	add_link('', 'NHK VN', 0, 'mms://wm.nhk.or.jp/rj/on_demand/wma/vietnamese.wma', thumbnails + '', '')
	add_link('', 'RFI VN', 0, 'http://95.81.155.3/2584/rfi_en_vietnamien/rfivietnamien.mp3', thumbnails + '', '')
	#add_dir('[COLOR lime]HTVOnline LIVETV[/COLOR]', url, 5, thumbnails + 'htv.jpg', query, type, 0)
	#add_dir('VTCPlay - TV', 'http://117.103.206.21:88/Channel/GetChannels?device=4', 10, thumbnails + 'vtcplay.jpg', query, type, 0)
	#add_dir('VTCPlay - Movies', '', 11, thumbnails + 'vtcplay.jpg', query, type, 0)
	#add_dir('FPTPlay - TV', url, 6, thumbnails + 'fptplay_logo.jpg', query, type, 0)
	#add_dir('FPTPlay - TVShow', url, 7, thumbnails + 'fptplay_logo.jpg', query, type, 0)
	#add_dir('ZUI.VN', url, 9, thumbnails + 'zui.png', query, type, 0)
	#add_dir('HDOnline.vn', url, 13, thumbnails + 'HDOnline.png', query, type, 0)

def searchMenu(url, query = '', type='f', page=0):
	add_dir('New Search', url, 2, icon, query, type, 0)
	add_dir('Clear Search', url, 3, icon, query, type, 0)

	searchList=cache.get('searchList').split("\n")
	for item in searchList:
		add_dir(item, url, 2, icon, item, type, 0)

def resolve_url(url):
	make_request("http://feed.hdrepo.com/hitcount.php?url=" + url);
	if 'zui.vn' in url:
		headers2 = {'User-agent' : 'iOS / Chrome 32: Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/32.0.1700.20 Mobile/11B554a Safari/9537.53',
											 'Referer' : 'http://www.google.com'}
		content = make_request(url, headers2)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('movie_play_chapter'):
				#movie_play_chapter('mediaplayer', '1', 'rtmp://103.28.37.89:1935/vod3/mp4:/phimle/Vikingdom.2013.720p.WEB-DL.H264-PHD.mp4', '/uploads/movie_view/5c65563b1ce8d106c013.jpg', 'http://zui.vn/subtitle/Vikingdom.2013.720p.WEB-DL.H264-PHD.srt');
				matchObj = re.match( r'[^\']*\'([^\']*)\', \'([^\']*)\', \'([^\']*)\', \'([^\']*)\', \'([^\']*)\'', s, re.M|re.I)
				url = matchObj.group(3)
				url = url.replace(' ','%20')
				xbmc.Player().play(url)
				xbmc.Player().setSubtitles(matchObj.group(5))
				return
				break

	if 'play.fpt.vn/Video' in url:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('"<source src='):
				start = s.index('\'')+1
				end = s.index('\'', start+1)
				url = s[start:end]
				break

	if 'play.fpt.vn' in url:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		item = soup.find('div', {'id' : 'bitrate-tag'})
		url = item['highbitrate-link']
		content = make_request(url)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('<id>'):
				start = s.index('<id>')+4
				end = s.index('<', start+1)
				url = url.replace('manifest.f4m',s[start:end])
				url = 'http://scache.fptplay.net.vn/live/' + s[start:end] + '/playlist.m3u8'
				break
			       
	if 'htvonline' in url:
		content = make_request(url)
		for line in content.splitlines():
			if line.strip().startswith('file: '):
				url = line.strip().replace('file: ', '').replace('"', '').replace(',', '')
				break

			
	if 'GetChannelStream' in url or 'GetMovieStream' in url or 'vtvplay' in url:
		content = make_request(url)
		url = content.replace("\"", "")
		url = url[:-5]
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def add_link(date, name, duration, href, thumb, desc):
	description = date+'\n\n'+desc
	u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&mode=4"
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration})
	if 'zui' in href:
		liz.setProperty('IsPlayable', 'false')
	else:
		liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)



def add_dir(name,url,mode,iconimage,query='',type='f',page=0):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)#+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]

	return param

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=''
name=None
mode=None
query=None
type='f'
page=0

try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
try:
	page=int(urllib.unquote_plus(params["page"]))
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "type: "+str(type)
print "page: "+str(page)
print "query: "+str(query)

if mode==None:
	get_categories()
#		fslink_get_video_categories(FSLINK+'/phim-anh.html')

elif mode==1:
	searchMenu(url, '', type, page)

elif mode==2:
	search(url, query, type, page)

elif mode==3:
	clearSearch()

elif mode==4:
	resolve_url(url)
elif mode==5:
	get_htv()
elif mode==6:
	get_fpt()
elif mode==7:
	get_fpt_other('http://play.fpt.vn/the-loai/tvshow')
	#get_fpt_other('http://play.fpt.vn/the-loai/sport')
	#get_fpt_other('http://play.fpt.vn/the-loai/music')
	#get_fpt_other('http://play.fpt.vn/the-loai/general')
elif mode==8:
	get_fpt_tvshow_cat(url)
elif mode==9:
	get_zui(url)
elif mode==10:
	get_vtc(url)
elif mode==11:
	get_vtc_movies(url, query, type, page)
elif mode==13:
	get_hdonline(url)
	 
xbmcplugin.endOfDirectory(int(sys.argv[1]))





	
	




























