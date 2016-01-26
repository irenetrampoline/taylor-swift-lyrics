import bs4
import urllib
from urlparse import urljoin
import gzip
import json
from os.path import join

import py.test

AZLYRICS_URL = 'http://www.azlyrics.com/t/taylorswift.html'
METROLYRICS_URL = 'http://www.metrolyrics.com/taylor-swift-lyrics.html'

EX_URL = 'http://www.azlyrics.com/lyrics/taylorswift/aplaceinthisworld.html'

# scrape lyrics
class LyricsWalker(object):
	"""
	Class for lyric gathering. Currently for AZ Lyrics, but can be adapted into
	base case.
	"""
	@classmethod
	def get_song_info(cls, url=EX_URL):
		"""
		Grabs lyrics from URL and return plain text lyrics.
		Lyrics are located at /html/body/div[3]/div/div[2]/div[6]
		"""
		soup = cls.get_soup_from_url(url)

		try:
			album_info = soup.find('div', {'class': 'album-panel'}).text.strip()
			album = album_info.split('"')[1]
			year = album_info.split('(')[1][:-1]
			title = soup.title.text.split(' - ')[-1]
			lyrics = soup.html.body.findAll('div')[10].div.findAll('div')[2].findAll('div')[7].text.strip()
		except:
			py.test.set_trace()

		entry_info = {
			'lyrics': lyrics,
			'title': album,
			'year': year,
			'title': title
		}

		print 'Parsed %s' % title
		return entry_info

	@classmethod
	def get_soup_from_url(cls, url):
		urlobject = urllib.urlopen(url)
		return bs4.BeautifulSoup(urlobject.read())

	@classmethod
	def walk_homepage(cls, home_url, output_dir=''):
		soup = cls.get_soup_from_url(home_url)
		py.test.set_trace()
		song_lst = soup.find(id='listAlbum').findAll(target='_blank')

		had_previous = False
		filename = join(output_dir, 'az_lyrics.json.gz')
		with open(filename, 'wb') as f:
			for song in song_lst:
				f.write(',' if had_previous else '[')
				song_url = urljoin(home_url, song.get('href'))
				json.dump(cls.get_song_info(song_url), f)
			f.write(']')

if __name__ == '__main__':
	py.test.set_trace()
	LyricsWalker.walk_homepage(AZLYRICS_URL, '')