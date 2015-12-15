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

  with codecs.open(f1_name, 'w', encoding='utf-8') as f1_w, \
       codecs.open(f2_name, 'w', encoding='utf-8') as f2_w:
    for line in sys.stdin:
      line_uni = unicode(line, encoding='utf-8')
      line_clean = line_uni.strip()
      if '####' in line_clean:
        splitted_lines = re.split(r'####', line_clean)
        f1_w.write(splitted_lines[0]+u'\n')
        f2_w.write(splitted_lines[1]+u'\n')

if __name__ == '__main__':
  import argparse
  arg_parser = argparse.ArgumentParser(description='Clean the error data.')
  arg_parser.add_argument('output_dir', help='Where the cleaned error data should be written')
  args = arg_parser.parse_args()
  clean_error_data(args.output_dir)
