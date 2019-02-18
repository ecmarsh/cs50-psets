from nltk.tokenize import sent_tokenize, word_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # Split each string into lines
    t_type = 'line'
    tokenized_a = tokenize(a, t_type)
    tokenized_b = tokenize(b, t_type)

    # Return a list of matches
    return matches(tokenized_a, tokenized_b)


def sentences(a, b):
    """Return sentences in both a and b"""

    # Split each string into sentences
    t_type = 'sent'
    tokenized_a = tokenize(a, t_type)
    tokenized_b = tokenize(b, t_type)

    # Return the matching sentences
    return matches(tokenized_a, tokenized_b)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # Split each file into list of words
    t_type = 'word'
    tokenized_a = tokenize(a, t_type)
    tokenized_b = tokenize(a, t_type)

    # Split each list of words into substrings
    subStr_a = []
    subStr_b = []
    for s in split_strings(a, n):
        subStr_a.append(s)
    for s in split_strings(b, n):
        subStr_b.append(s)

    # Return the matching substrings
    return matches(subStr_a, subStr_b)


def tokenize(text, tokenize_type):
    """Splits file text by t, either word or sentence and returns list"""
    tokenized = []

    # Tokenize by sentence
    if tokenize_type == 'sent':
        tokenized = sent_tokenize(text)
    # Tokenize by word
    elif tokenize_type == 'word':
        tokenized = word_tokenize(text)
    # Default split by line
    else:
        tokenized = text.split('\n')

    # Return list w/ duplicates removed
    tokenized_set = set(tokenized)
    return list(tokenized_set)


def matches(a, b):
    """Returns set of matches from two lists"""
    return [s for s in set(a) if s in set(b)]


def split_strings(s, n):
    """Extract all substrings of length n from single string s"""

    subs = set()

    # Split a and b into substrings of length n
    # "Hello", n = 3 --> ["Hel", "ell", "llo"]
    l = len(s)
    for i in range(l):
        j = i + n
        if len(s[i:j]) == n:
            subs.add(s[i:j])

    # Return new list with substrings
    return list(subs)