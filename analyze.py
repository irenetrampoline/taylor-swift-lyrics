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

from collections import Counter
from matplotlib import pyplot as plt

def create_word_occurence_dict(s):
    """
    TODO: Create a data structure to capture word occurrences and counts
    Input: string of lyrics text
    Output: Dictionary with key as word and value as occurrence count

    Note that you may decide to do some preprocessing on the text before counting,
    for example making everything lower case and removing puncuation.
    """
    raise NotImplementedError

def top_songs_with_word(word, lyrics_json, n=5):
    """
    TODO: Find top N songs with a certain word
    Input: word (str), lyrics_json (including word_counts dict), optional N
    Output: list of song titles and number of occurences
    """
    raise NotImplementedError

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

    print top_songs_with_word('love', songs)