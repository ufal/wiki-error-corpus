# *-* coding: utf-8 *-*

"""Utility functions.

"""
import nltk.data
from nltk.tokenize.regexp import WhitespaceTokenizer
from nltk.corpus import PlaintextCorpusReader
import numpy as np
import sys


def to_unicode_or_bust(s, encoding='utf-8'):
  """Converts the bytestring in utf-8 to Unicode.

  Credit: Method from 'Unicode in Python, Completely Demystified'.
  
  Args:
    s: Bytestring
    encoding: Encoding

  Returns:
    Return the Unicode version of the given bytestring

  """
  if isinstance(s, basestring):
    if not isinstance(s, unicode):
      s = unicode(s, encoding)
  return s   


def get_sentences_for_text(corpus_root, filename, lang='english'):
  """Segments the given text into sentences.

  Args:
    corpus_root: Directory in which the text file is residing.
    filename: Name of the text file.
    lang: Tokenizer language. For possible values, look at:
    ${NLTK_DATA}/tokenizers/punkt

  Returns:
    Sentences in the given text. 

  """
  tokenizer_path = 'tokenizers/punkt/' + lang + '.pickle'
  text = PlaintextCorpusReader(corpus_root, [filename], word_tokenizer=WhitespaceTokenizer(), 
                               sent_tokenizer=nltk.data.LazyLoader(tokenizer_path))
  return text.sents()

def levenshtein_distance(s, t):
  """Minimum edit distance between two strings.

  Args:
    s: Source string
    t: Target string

  Returns:
    int: Minimum edit distance between the two input strings.

  """
  m = len(s)
  n = len(t)
  if m == 0:
    return n
  if n == 0:
    return m
  d = np.zeros((m+1, n+1))
  d[:, 0] = np.arange(m+1)
  d[0, :] = np.arange(n+1)
  for j in range(1, n+1):
    for i in range(1, m+1):
      if s[i-1] == t[j-1]:
        d[i][j] = d[i-1][j-1]
      else:
        d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+1)
  return int(d[m][n])


if __name__ == '__main__':
  corpus_root = '/net/cluster/TMP/loganathan/wiki_dump/cs/processing/stage3'
  file_name = '0000000007.xml'
  sentences = get_sentences_for_text(corpus_root, file_name)
  try:
    for s in sentences:
      print s
      print '\n----END----'
  except AssertionError:
    print 'Empty file'
  
