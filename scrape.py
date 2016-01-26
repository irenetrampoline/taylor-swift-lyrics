import bs4
import urllib
from urlparse import urljoin

AZLYRICS_URL = 'http://www.azlyrics.com/lyrics/taylorswift/timmcgraw.html'
METROLYRICS_URL = 'http://www.metrolyrics.com/taylor-swift-lyrics.html'

EX_URL = 'http://www.azlyrics.com/lyrics/taylorswift/aplaceinthisworld.html'

# scrape lyrics
class LyricsWalker(object):
	"""
	Class for lyric gathering. Currently for AZ Lyrics, but can be adapted into
	base case.
	"""
	def __init__(self, home_url):
		self.home_url = home_url

	@staticmethod
	def get_lyrics(url=EX_URL, album=False):
		"""
		Grabs lyrics from URL and return plain text lyrics.
		Lyrics are located at /html/body/div[3]/div/div[2]/div[6]
		"""
		soup = get_soup_from_url(url)

		lyrics = soup.html.body.findAll('div')[10].div.findAll('div')[2].findAll('div')[7].text.strip()
		print 'Parsed %s' % soup.title.text

		if album:
			return lyrics, None

		return lyrics


	@staticmethod
	def get_soup_from_url(url):
		urlobject = urllib.urlopen(url)
		return bs4.BeautifulSoup(urlobject.read())

	def walk_homepage(self):
		urlobject = get_soup_from_url(self.home_url)
		song_lst = soup.find(id='listAlbum').findAll(target='_blank')

		for song in song_lst:
			song_url = urljoin(self.homeurl, song.get('href'))
			get_lyrics(song_url)
if __name__ == '__main__':
	print parse_entry(EX_URL)