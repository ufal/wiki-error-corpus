# -*- coding: utf-8 -*-

"""Fixes output of WikiExtractor.py

"""

import argparse
import codecs
import re


def fix_extraction(input_dir, input_file, output_dir):
  with codecs.open(input_dir + '/' + input_file, 'r', encoding='utf-8') as f, codecs.open(output_dir + '/' + input_file, 'w', encoding='utf-8') as fw:
      contents = f.read()
      contents = re.sub(r'<\/text>\s*<sha1>', '##LOSPR##', contents)
      contents = re.sub(r'<sha1>', '</text>\n\t<sha1>', contents)
      contents = re.sub(r'##LOSPR##', '</text>\n\t<sha1>', contents)
      
      # HTML entities
      contents = re.sub(r'&', '&amp;', contents)

      # Remove HTML tags if not removed already
      tag_pat1 = (r'<\/?(textarea|select|strong|center|option|'
                  r'input|param|small|style|table|tbody|thead|tfoot|'
                  r'body|head|html|span|font|form|'
                  r'div|img|var|pre|sub|sup|var|'
                  r'br|dl|dt|dd|em|h[1-6]|hr|li|ol|td|tr|th|ul|a|b|p|q|u)>'
                  )
      contents = re.sub(tag_pat1, '', contents)
      
      fw.write(contents)
      

if __name__ == '__main__':
  arg_parser = argparse.ArgumentParser(description='Script for fixing WikiExtractor.py outputs')
  arg_parser.add_argument('input_dir', help='Input dir')
  arg_parser.add_argument('input_file', help='Input file')
  arg_parser.add_argument('output_dir', help='Output directory')
  args = arg_parser.parse_args()
  fix_extraction(args.input_dir, args.input_file, args.output_dir)
