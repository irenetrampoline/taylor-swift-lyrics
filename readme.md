# Analyze Taylor Swift lyrics using Python
By Irene Chen, originally designed for a [WECode 2016](http://www.wecodeharvard.com/) workshop

# Intro
Taylor Swift is renowned for her narrative songs. Here we will analyze what makes a Taylor Swift song sound like her songwriting.

There are two parts designed for varying levels of familiarity with Python:

 * `analyze.py`: for newer students to find most common unigrams (words) and bigrams (2-word phrases) that Taylor Swift uses
 * `songbird.py`: for students more familiar with Python to generate a random song using a Markov Model. One sample output could be:

```
I'll drive on me is the news.
I'd tell the crowds.
Headlights pass by morning light on you to walk away
like they mean, I know you,
I paced back on me
From the water
That's when you
Remember when you were right to get out
```

# Data
Taylor Swift lyrics are scraped from [AZ Lyrics](http://www.azlyrics.com/) using `scrape.py`.

Full song data is contained in 'az_lyrics.json' and includes the following fields:
 * `title`: song title
 * `album`: album name
 * `year`: album year
 * `lyrics`: lyrics of song (no unicode)

To load song data in Python, use

```
import json

with open('az_lyrics.json', 'rb') as f:
	songs = json.load(f)
```

The other form of lyric data is in `all_tswift_lyrics.txt` and will be more relevant for the Markov Model. The file contains all of the song lyrics in one location without any separators or song titles.

To load song lyrics into Python, use
```
with open('all_tswift_lyrics.txt', 'rb') as f:
	lyrics = f.read()
```

# Unigrams and Bigrams
Execises can be found in `analyze.py` with exercises marked as `TODO`. As with all code, there are design considerations you must make: How much do you care about punctuation? Upper case letters? How do you feel about [stop words](https://en.wikipedia.org/wiki/Stop_words)?

Once you have completed the listed exercises, feel free to explore! Here are some ideas for further analysis:
 * Which words has she stopped using over time (from 2006 to 2014)?
 * Which words and phrases frequently appear together in the same song?

# Markov Model
As before, exercises can be found in `songbird.py` with exercises marked `TODO`. Here I would urge students to get a working product first and then tinker with things like punctuation and capitalization.

When completed, the code would run as follows

```
from songbird import Songbird
tswift_bird = Songbird('all_tswift_lyrics.txt')
print tswift_bird.generate(50)
```

# Contact me
If you have any questions, please reach out to me at irenetrampoline \[at\] gmail \[dot\] com
```