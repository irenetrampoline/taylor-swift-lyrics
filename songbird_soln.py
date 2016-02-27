"""
Songbird: A Markov Model text generator (solutions)
Irene Chen (github/irenetrampoline)
Feb 27, 2016
"""

import re
from random import choice
import py.test

class Songbird:
    """
    Given a single source document, generate similar sounding strings/songs
    based on a Markov Model.
    """
    def __init__(self, source_path):
        self.corpus = open(source_path, 'rb').read()
        self.tokens = self.get_tokens()
        self.bigrams = self.get_bigrams()

    def get_tokens(self):
        """
        Read corpus file and create a list of all tokens (words). Note that we
        are not removing duplicates, only turning a text file into a list.

        Removing punctuation is optional but will make everything much easier.
        """
        tokens = re.findall(r"[\w']+|[.,!?;]", self.corpus)
        return tokens

    def get_bigrams(self):
        """
        TODO: From the list of tokens, create a dict that has:
         - key: word
         - value: list of words that appear after it

        Bigrams are sequences of two words that are adjacent to each other.
        Example: If tokens = ['I', 'am', 'happy.', 'I', 'saw', 'a', 'happy', 'cat.'],
        then our dictionary would look like:
        {
            'I': ['am', 'saw'],
            'am': ['happy'],
            'happy.': ['I'],
            'saw': ['a'],
            'a': ['happy'],
            'happy': ['cat.'']
        }
        """
        bigrams = {}
        for i in xrange(len(self.tokens) - 1):
            try:
                prefix = self.tokens[i]
                suffix = self.tokens[i + 1]
                if prefix not in bigrams:
                    bigrams[prefix] = []
                bigrams[prefix].append(suffix)
            except:
                py.test.set_trace()
        self.stop = suffix
        return bigrams

    def generate(self, size=100):
        """
        TODO: Generate a new string given a desired length.

        This is the meat of the project. Using the bigrams create above, use
        randomness to generate an original Taylor-Swift-inspired song! You have a
        LOT of freedom here.

        1) Choose how to start the song. Do you pick a random word? An upper case word?
        A word that's started other songs?
        2) Given one word, pick the next word! The bigrams dictionary that we made
        above might be helpful.
        3) [optional] Before you publish your song, do you want to clean it up?
        Captialize letters, add line breaks, up to you!
        """
        text = []
        startwords = [x for x in self.bigrams.keys() if x[0].isupper()]
        if startwords:
            prefix = choice(startwords) #random start choice
        else:
            prefix = choice(self.bigrams.keys())
        text.append(prefix)

        for i in xrange(size - 1):
            if prefix == self.stop:
                #last word has no suffix!
                if startwords:
                    prefix = choice(startwords)
                else:
                    prefix = choice(self.bigrams.keys())

            suffix = choice(self.bigrams[prefix])
            # random choice. theoretically if we hash duplicates
            # then more common words show up more.
            text.append(suffix)
            prefix = suffix

        string = self.format_string(text)
        return string

    @staticmethod
    def format_string(text):
        """
        TODO [optional]: Format string into readable format (if desired).
        Reformat the text to a nice readable string.
        Capitalize sentence beginnings.
        Remove space before punctuation.
        """
        string = " ".join(text)
        punct = ["?", "!", ".", ",", ";"] #newlines

        for p in punct:
            string = string.replace(" " + p, p)

        return string

if __name__ == '__main__':
    tswift_bird = Songbird('all_tswift_lyrics.txt')
    print tswift_bird.generate(50)
