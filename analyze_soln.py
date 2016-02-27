"""
Analyzing Taylor Swift Lyrics: Unigrams and Bigrams (solutions)
Irene Chen (github/irenetrampoline)
Feb 27, 2016
"""
import json
import numpy as np
import operator
import pandas as pd
import string
import py.test

from collections import Counter
from matplotlib import pyplot as plt

VOCAB = Counter(['test'])

def create_word_occurence_dict(s):
    """
    TODO: Create a data structure to capture word occurrences and counts
    Input: string of lyrics text
    Output: Dictionary with key as word and value as occurrence count

    Note that you may decide to do some preprocessing on the text before counting,
    for example making everything lower case and removing puncuation.
    """
    s = s.translate(string.maketrans("",""), string.punctuation)
    s = s.lower()
    s = s.split()
    counter = Counter(s)
    global VOCAB
    VOCAB = counter + VOCAB
    return counter

def top_songs_with_word(word, lyrics_json, n=5):
    """
    TODO: Find top N songs with a certain word
    Input: word (str), lyrics_json (including word_counts dict), optional N
    Output: list of song titles and number of occurences
    """
    top_songs = [(i['title'], i['word_counts'].get(word, 0)) for i in songs]
    for i,j in sorted(top_songs, reverse=True, key=operator.itemgetter(1))[:n]:
        print i, j

def get_lyrics_json():
    with open('az_lyrics.json', 'rb') as f:
        return json.load(f)

def get_stopwords():
    with open('stopwords.txt', 'rb') as f:
        words = f.read().splitlines()
    return set(words)

def make_txt_alllyrics():
    songs = get_lyrics_json()

    with open('all_tswift_lyrics.txt', 'wb') as f:
        for song in songs:
            f.write(song['lyrics'])

if __name__ == '__main__':
    songs = get_lyrics_json()
    stopwords = get_stopwords()

    for song in songs:
        song['word_counts'] = create_word_occurence_dict(song['lyrics'])

    # vocab =
    # which song has "love" in it the most?
    # top_songs_with_word('hate', songs)

    for i in VOCAB.keys():
        if i in stopwords:
            del VOCAB[i]

    # take top thousand, group by album year (total and num songs), divide and find change

    top_thousand, _ = zip(*VOCAB.most_common(1000))
    album_info = dict()

    for song in songs:
        year = song['year']
        album = song['album']
        # {'num_songs': 10, 'vocab': {'i': 1000, 'penny': 2}}
        if year is not None and album is not None:
            album_year_info = album_info.get(year, dict())

            num_songs = album_year_info.get('num_songs', 0)
            album_year_info['num_songs'] = num_songs + 1

            # # albums = album_year_info.get('albums', dict())

            # try:
            #     album_year_info['albums'] = albums.append(album)
            # except:
            #     py.test.set_trace()

            for word in top_thousand:
                year_vocab = album_year_info.get('vocab', dict())
                song_word_occurence = song['word_counts'].get(word, 0)

                year_word_occurence = year_vocab.get(word, 0)
                year_vocab[word] = year_word_occurence + song_word_occurence
                album_year_info['vocab'] = year_vocab

            album_info[year] = album_year_info

    # py.test.set_trace()
    # now divide to get averages
    for year in album_info.keys():
        num_songs = album_info[year]['num_songs']
        for word in album_info[year]['vocab'].keys():
            album_info[year]['vocab'][word] /= float(num_songs)

    vocab2006 = album_info['2006']['vocab']
    vocab2014 = album_info['2014']['vocab']

    diff = {key: vocab2014[key] - vocab2006.get(key, 0) for key in vocab2014.keys()}
    print sorted(diff.items(), reverse=True, key=operator.itemgetter(1))[:5]
    print sorted(diff.items(), reverse=True, key=operator.itemgetter(1))[-5:]
    # differences
    # py.test.set_trace()