import numpy as np
import json
import string
import py.test
import operator

from collections import Counter
from matplotlib import pyplot as plt

def create_word_occurence_dict(s):
    """
    TODO: Create a data structure to capture word occurrences and counts
    Input: string of lyrics text
    Output: Dictionary with key as word and value as occurrence count

    Note that you may decide to do some preprocessing on the text before counting,
    for example making everything lower case and removing puncuation. You may also
    want to consider removing stop words.
    """
    s = s.translate(string.maketrans("",""), string.punctuation)
    s = s.lower()
    s = s.split()
    return Counter(s)

def top_songs_with_word(word, lyrics_json, n=5):
    """
    TODO: Find top N songs with a certain word
    Input: word (str), lyrics_json (including word_counts dict), optional N
    Output: list of song titles and number of occurences
    """
    top_songs = [(i['title'], i['word_counts'].get(word, 0)) for i in songs]
    for i,j in sorted(top_songs, reverse=True, key=operator.itemgetter(1))[:n]:
        print i, j

def ascii_encode_dict(data):
    """
    Quick and dirty ascii encoder for ensuring that lyrics don't come in unicode
    """
    ascii_encode = lambda x: x.encode('ascii') if x is not None else None
    return dict(map(ascii_encode, pair) for pair in data.items())

def get_lyrics_json():
    with open('az_lyrics.json', 'rb') as f:
        return json.load(f, object_hook=ascii_encode_dict)

def get_stopwords():
    with open('stopwords.txt') as f:
        return f.readlines()

if __name__ == '__main__':
    songs = get_lyrics_json()
    stopwords = get_stopwords()

    for song in songs:
        song['word_counts'] = create_word_occurence_dict(song['lyrics'])

    # which song has "love" in it the most?
    top_songs_with_word('hate', songs)
    # py.test.set_trace()