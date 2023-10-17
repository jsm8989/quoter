import numpy as np
import re

from nltk.tokenize import TweetTokenizer # This will be our chosen tokenzier for cleaning text before hashing.
import re
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False) 


def fnv(data):
    return hval


def custom_tokenize(text, basic_tokenize = False):
        return split

def tweet_to_hash_array(text):
    """
    Takes a single string of text (e.g. a single tweet).
    Tokenizes the string, removing twitter handles, and reducing length, 
    (e.g. trueeeee becomes truee).
    Uses Fowler–Noll–Vo hash function on tokens to give digestable numbers.
    """
    if type(text) is not str: 
        return text
    try:
        return [fnv(str.encode(w)) for w in custom_tokenize(text)]
    
    except UnicodeEncodeError: # This is to deal with encoding unicode surrogates
        encoded = []
        for w in tknzr.tokenize(text):
            try:
                encoded.append(fnv(str.encode(w)))
            except UnicodeEncodeError:
                continue # They're simply ignored
        return encoded
