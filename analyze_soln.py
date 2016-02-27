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
    return counter

def top_songs_with_word(word, lyrics_json, n=5):
    """
    TODO: Find top N songs with a certain word
    Input: word (str), lyrics_json (including word_counts dict), optional N
    Output: list of song titles and number of occurences
    """
    top_songs_word_lst = list()
    top_songs = [(i['title'], i['word_counts'].get(word, 0)) for i in songs]
    for i,j in sorted(top_songs, reverse=True, key=operator.itemgetter(1))[:n]:
        top_songs_word_lst.append((i, j))
    return top_songs_word_lst

def ascii_encoder(data):
    ascii_encode = lambda x: x.encode('ascii') if x is not None else None
    return dict(map(ascii_encode, pair) for pair in data.items())

def get_lyrics_json():
    with open('az_lyrics.json', 'rb') as f:
        return json.load(f, object_hook=ascii_encoder)

def get_stopwords():
    with open('stopwords.txt', 'rb') as f:
        words = f.read().splitlines()
    return set(words)

def make_txt_alllyrics():
    songs = get_lyrics_json()

    with open('all_tswift_lyrics.txt', 'wb') as f:
        for song in songs:
            f.write(song['lyrics'])

def plot_bar_chart(values, labels):
    fig, ax = plt.subplots(figsize=(8,6))
    N = len(values)
    ind = np.arange(N)
    width = 0.75

    ax.bar(ind, values, width, color='#FFB7AA', edgecolor='none')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(labels)

    # make plot prettier
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

    plt.xticks(rotation=35, ha='right')
    plt.title('The 20 Most Common Taylor Swift Words')
    plt.xlabel('Word (excl stop words)')
    plt.ylabel('Uses per song')
    plt.savefig('top_words.png', bbox_inches='tight')

if __name__ == '__main__':
    songs = get_lyrics_json()
    stopwords = get_stopwords()

    for song in songs:
        song['word_counts'] = create_word_occurence_dict(song['lyrics'])

    # Which song has "love" in it the most?
    print 'Top 5 songs with "love" in them'
    for i,j in top_songs_with_word('love', songs):
        print i, j
    print

    # What are the top 20 words used by TSwift?
    vocab = Counter()
    for song in songs:
        vocab += song['word_counts']

    for i in vocab.keys():
        if i in stopwords:
            del vocab[i]

    # Graph top 20 words used by TSwift
    words, counts = zip(*vocab.most_common(20))
    plot_bar_chart(map(lambda x: float(x) / len(songs), counts), words)
    print 'Top 20 words graph in top_words.png'
    print

    # Which words has she started/stopped using between 2006 and 2014?
    # take top thousand, group by album year (total and num songs), divide and find change
    top_thousand, _ = zip(*vocab.most_common(1000))
    album_info = dict()

    for song in songs:
        year = song['year']
        album = song['album']
        # example data: {'num_songs': 10, 'vocab': {'i': 1000, 'penny': 2}}
        if year is not None and album is not None:
            album_year_info = album_info.get(year, dict())

            num_songs = album_year_info.get('num_songs', 0)
            album_year_info['num_songs'] = num_songs + 1

            for word in top_thousand:
                year_vocab = album_year_info.get('vocab', dict())
                song_word_occurence = song['word_counts'].get(word, 0)

                year_word_occurence = year_vocab.get(word, 0)
                year_vocab[word] = year_word_occurence + song_word_occurence
                album_year_info['vocab'] = year_vocab

            album_info[year] = album_year_info
    # now divide to get averages
    for year in album_info.keys():
        num_songs = album_info[year]['num_songs']
        for word in album_info[year]['vocab'].keys():
            album_info[year]['vocab'][word] /= float(num_songs)

    vocab2006 = album_info['2006']['vocab']
    vocab2014 = album_info['2014']['vocab']

    diff = {key: vocab2014[key] - vocab2006.get(key, 0) for key in vocab2014.keys()}
    print 'Top 5 words grown in use from 2006 to 2014'
    for i,j in sorted(diff.items(), reverse=True, key=operator.itemgetter(1))[:5]:
        print i, j
    print
    print 'Top 5 words decrease in use from 2006 to 2014'
    for i,j in sorted(diff.items(), reverse=True, key=operator.itemgetter(1))[-5:]:
        print i,j
    # differences
    # py.test.set_trace()