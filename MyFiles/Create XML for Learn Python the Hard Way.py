# -*- coding: utf-8 -*-

'''
Create XML on Windows PC's Desktop from YouTube website's playlist.
'''

import urllib2, urllib, re, os

# This script creates XML playlist on PC's Desktop for "Learn Python the Hard Way by Barton Poulson" from YouTube.
# Change url, foldername, and thumb accordingly for other youTube's playlist.
url='https://www.youtube.com/playlist?list=PLCHnubFzFwjJVEvQk-FuEynAuwGV_4BNS'  # playlist's url on YouTube mainsite.
foldername = 'Learn Python the Hard Way by Barton Poulson'  # This name will be used for folder, file, and channel name
thumb = 'https://yt3.ggpht.com/-SeiGqP6PKvI/AAAAAAAAAAI/AAAAAAAAAAA/3NKqqfiwqCw/s100-c-k-no/photo.jpg' # location to thumbnail on xml playlist.


xml_file = os.path.expanduser('~/Desktop/' + foldername + '.xml')		# xml file is on Desktop

'''
Desktop_folderpath = os.path.expanduser('~/Desktop/' + foldername)
if not os.path.exists(Desktop_folderpath):
    os.makedirs(Desktop_folderpath)
else: pass
xml_file = Desktop_folderpath + '\\' + foldername + '.xml'
'''

req = urllib2.Request(url)
req.add_header('User-agent' , 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0')
response = urllib2.urlopen(req)
link=response.read()
response.close()

f = open(xml_file, 'a+')
f.write('<channel>\n<name>' + foldername + '</name>\n<thumbnail>' + thumb + '</thumbnail>\n<items>\n')

match = re.compile('<a class=".+?" dir="ltr" href="/watch\?v=(.+?)\&.+?" data-sessionlink=".+?">\s*(.+?)\s*</a>\s*.+\s*.+\s*.+\s*.+\s*.+<div class="timestamp"><span title=".+?">(.+?)<').findall(link)
for url, name, duration in match:
	name = name.replace('Learn Python the Hard Way - ', '') + ' - Learn Python the Hard Way'
	url = 'plugin://plugin.video.youtube/play/?video_id=' + url
	f.write('<item>\n<title>' + name + ' (' + duration + ')' + '</title>\n<link>' + url + '</link>\n<thumbnail>' + thumb + '</thumbnail>\n</item>\n')
f.write('</items>\n</channel>\n')
f.close()