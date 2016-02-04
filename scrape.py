import bs4
import urllib
from urlparse import urljoin
import gzip
import json
from os.path import join
import time

import py.test

AZLYRICS_URL = 'http://www.azlyrics.com/t/taylorswift.html'
METROLYRICS_URL = 'http://www.metrolyrics.com/taylor-swift-lyrics.html'

EX_URL = 'http://www.azlyrics.com/lyrics/taylorswift/aplaceinthisworld.html'

class LyricsWalker(object):
	"""
	Class for lyric gathering. Currently for AZ Lyrics, but can be adapted into
	base case with varying scraping functions.
	"""
	@classmethod
	def get_song_info(cls, url=EX_URL):
		"""
		Grabs lyrics from URL and return plain text lyrics.
		Lyrics are located at /html/body/div[3]/div/div[2]/div[6]
		"""
		soup, html = cls.get_soup_from_url(url, html=True)

		try:
			album_info = soup.find('div', {'class': 'album-panel'})
			if album_info:
				album_text = album_info.text.strip()
				album = album_text.split('"')[1]
				year = album_text.split('(')[1][:-1]
			else:
				album, year = None, None
			title = soup.title.text.split(' - ')[-1]
			lyrics = soup.html.body.findAll('div')[10].div.findAll('div')[2].findAll('div')[7].text.strip()
		except:
			py.test.set_trace()

		entry_info = {
			'lyrics': lyrics,
			'album': album,
			'year': year,
			'title': title
		}

		title_str = title.replace(' ', '_')
		f = open('data/%s.txt' % title_str, 'wb')
		f.write(html)
		f.close()

		print 'Parsed %s' % title
		return entry_info

	@classmethod
	def get_soup_from_url(cls, url, html=False):
		urlobject = urllib.urlopen(url)
		time.sleep(5)
		print 'Just read %s' % url
		full_html = urlobject.read()

		if html:
			return bs4.BeautifulSoup(full_html), full_html
		return bs4.BeautifulSoup(full_html)

	@classmethod
	def walk_homepage(cls, home_url, output_dir=''):
		soup = cls.get_soup_from_url(home_url)
		# py.test.set_trace()
		song_lst = soup.find(id='listAlbum').findAll(target='_blank')

		had_previous = False
		filename = join(output_dir, 'az_lyrics.json')
		with open(filename, 'wb') as f:
			for song in song_lst:
				f.write(',' if had_previous else '[')
				song_url = urljoin(home_url, song.get('href'))
				json.dump(cls.get_song_info(song_url), f)
			f.write(']')
		print "Wrote all songs to json!"

if __name__ == '__main__':
	LyricsWalker.walk_homepage(AZLYRICS_URL)