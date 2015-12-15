# -*- coding: utf-8 -*

"""Cleans the error corpus. 

"""

import codecs
import re
import sys

def clean_error_data(output_dir):
  """Cleans and writes error data in two files.

  Args:
    output_dir: Where the output files should be written

  """
  f1_name = output_dir + '/' + 'orig_sen.txt'
  f2_name = output_dir + '/' + 'error_sen.txt'
  f3_name = output_dir + '/' + 'orig_error_words.txt'

  with codecs.open(f1_name, 'w', encoding='utf-8') as f1_w, \
       codecs.open(f2_name, 'w', encoding='utf-8') as f2_w, \
       codecs.open(f3_name, 'w', encoding='utf-8') as f3_w:

    for line in sys.stdin:
      line_uni = unicode(line, encoding='utf-8')
      line_clean = line_uni.strip()
      if '####' in line_clean:
        splitted_lines = re.split(r'####', line_clean)
        s1 = splitted_lines[0]
        s2 = splitted_lines[1]
        s1_toks = re.split(r'\s+', s1)
        s2_toks = re.split(r'\s+', s2)
        if len(s1_toks) > 0 and len(s1_toks) == len(s2_toks):
          s1_s2_toks_zipped = zip(s1_toks, s2_toks)
          o_e_list = []
          digit_error = False
          for o_e in s1_s2_toks_zipped:
            if o_e[0].lower() != o_e[1].lower():
              orig_match = re.match(r'\d', o_e[0])
              if not orig_match:
                o_e_list.append(o_e)
              else:
                digit_error = True
          if not digit_error:
            f1_w.write(s1+u'\n')
            f2_w.write(s2+u'\n')
            for o_e in o_e_list:
              f3_w.write(o_e[0]+'\t:\t'+o_e[1]+u'\n')

if __name__ == '__main__':
  import argparse
  arg_parser = argparse.ArgumentParser(description='Clean the error data.')
  arg_parser.add_argument('output_dir', help='Where the cleaned error data should be written')
  args = arg_parser.parse_args()
  clean_error_data(args.output_dir)
