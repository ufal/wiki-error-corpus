# -*- coding: utf-8 -*-

"""Extracts spelling errors from revision history. 

"""

import utils

class ErrorSentence(object):
  """Class for representing an error sentence together with original sentence.

  """
  def __init__(self, orig_tokens, error_tokens):
    self.tokens = None
    self.set_error_sentence(orig_tokens, error_tokens)

  def set_error_sentence(self, orig_tokens, error_tokens):
    o_e_tokens = zip(orig_tokens, error_tokens)
    self.tokens = []
    for t in o_e_tokens:
      if t[0] != t[1]:
        self.tokens.append(t)
      else:
        self.tokens.append((t[0],))
      

class ErrorCorpus(object):
  """Class for representing the original text data with spelling errors.

  """
  max_dist = 3

  def __init__(self):
    self.corpus = None
    self.num_rev = 0
  
  def create_corpus_from_wiki(self, corpus_root, filename, output_dir):
    sentences = utils.get_sentences_for_text(corpus_root, filename)
    if sentences == None:
      return
    top_rev = []
    top_rev_with_err = []
    try:
      for s_list in sentences:
        s = ' '.join(s_list)
        if s.startswith('[Revision timestamp:'):
          self.num_rev += 1
        else:
          if self.num_rev == 1:
            if len(s_list) >= 1:
              top_rev.append(s_list)
          elif self.num_rev > 1:
            for r in top_rev:
              if len(s_list) == len(r):
                valid_errors = True
                errors = False
                old_curr_rev_sen = zip(r, s_list)
                for t in old_curr_rev_sen:
                  dist = utils.levenshtein_distance(t[0], t[1])
                  if dist > 0 and dist <= self.max_dist:
                    errors = True
                  elif dist > self.max_dist:
                    valid_errors = False
                    break
                if errors == True and valid_errors == True:
                  err_sen = ErrorSentence(r, s_list)
                  print ' '.join(r)
                  print ' '.join(s_list)
                  print '\n\n'
                  break
    except AssertionError:
      print 'Empty file'
        


if __name__ == '__main__':
  import os
  corpus_root = '/net/cluster/TMP/loganathan/wiki_dump/cs/processing/stage3'
  for root, dirnames, filenames in os.walk(corpus_root):
    for f in filenames:
      err_corpus = ErrorCorpus()
      print 'Extracting errors from: ', f
      err_corpus.create_corpus_from_wiki(corpus_root, f, '')

  #corpus_root = '/net/cluster/TMP/loganathan/wiki_dump/cs/processing/tmp_out'
  #file_name = 'hello.txt'
  #err_corpus = ErrorCorpus()
  #err_corpus.create_corpus_from_wiki(corpus_root, file_name, '')
