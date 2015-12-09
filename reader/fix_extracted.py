# -*- coding: utf-8 -*-

"""Fixes output of WikiExtractor.py

"""

import argparse
import codecs
import re


def fix_extraction(input_dir, input_file, output_dir):
  with codecs.open(input_dir + '/' + input_file, 'r', encoding='utf-8') as f, codecs.open(output_dir + '/' + input_file, 'w', encoding='utf-8') as fw:
      contents = f.read()
      contents = re.sub(r'<br>', '', contents)
      contents = re.sub(r'<\/text>\s*<sha1>', '##LOSPR##', contents)
      contents = re.sub(r'<sha1>', '</text>\n\t<sha1>', contents)
      contents = re.sub(r'##LOSPR##', '</text>\n\t<sha1>', contents)
      fw.write(contents)
      

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser(description='Script for fixing WikiExtractor.py outputs')
  arg_parser.add_argument('input_dir', help='Input dir')
  arg_parser.add_argument('input_file', help='Input file')
  arg_parser.add_argument('output_dir', help='Output directory')
  args = arg_parser.parse_args()
  fix_extraction(args.input_dir, args.input_file, args.output_dir)
