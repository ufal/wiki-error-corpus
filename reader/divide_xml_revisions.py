"""Divide the large XML revision dump file into per page revisions.

"""
import codecs
import os
import xml.sax

class WikiRevisionDumpHandler(xml.sax.ContentHandler):
  input_file = 'wiki.xml'
  output_dir = '.'
  file_counter = 0
  file_handle = ''

  def __init__(self, input_file, output_dir):
    self.input_file = input_file
    self.output_dir = output_dir

    self.curr_tag = ''
  
    # Page and revision elements
    self.page_start = 0
    self.revision_start = 0

    # Elements under page
    self.page_title = 0
    self.page_id = 0
    self.page_ns = 0

    # Elements under revision
    self.rev_id = 0
    self.rev_parent_id = 0
    self.rev_timestamp = 0
    self.rev_contrib = 0
    self.rev_contrib_username = 0
    self.rev_contrib_userid = 0
    self.rev_contrib_ip = 0
    self.rev_comment = 0 
    self.rev_model = 0
    self.rev_format = 0
    self.rev_text = 0 
    self.rev_sha1 = 0   

    self.content = ''

  def startElement(self, tag, attributes):
    self.curr_tag = tag

    if self.curr_tag == 'page': 
      self.page_start = 1
      # close the unclosed handles first if any
      if self.file_handle:
        self.file_handle.close()
      fname = repr(self.file_counter).zfill(10) + '.xml'
      abspath = self.output_dir + '/' + fname
      self.file_handle = codecs.open(abspath, 'w', 'utf-8')
      self.file_handle.write('<page>')

    if self.curr_tag == 'revision': 
      self.revision_start = 1
      self.file_handle.write('<revision>')

    if self.curr_tag == 'title': self.page_title = 1

    if self.curr_tag == 'id': 
      if self.revision_start:
        self.rev_id = 1
      elif self.page_start: 
        self.page_id = 1
      elif self.rev_contrib:
        self.rev_contrib_userid = 1

    if self.curr_tag == 'ns': self.page_ns = 1
    if self.curr_tag == 'parentid': self.rev_parent_id = 1
    if self.curr_tag == 'timestamp': self.rev_timestamp = 1
    if self.curr_tag == 'contributor': self.rev_contrib = 1
    if self.curr_tag == 'username': self.rev_contrib_username = 1
    if self.curr_tag == 'comment': self.rev_comment = 1
    if self.curr_tag == 'model': self.rev_model = 1
    if self.curr_tag == 'format': self.rev_format = 1
    if self.curr_tag == 'text': self.rev_text = 1
    if self.curr_tag == 'sha1': self.rev_sha1 = 1       
  
  def endElement(self, tag):
    self.current_tag = tag

    if self.curr_tag == 'page': 
      self.page_start = 0
      self.file_handle.write('</page>')
      self.file_handle.close()
      self.file_counter += 1

    if self.curr_tag == 'revision': 
      self.revision_start = 0
      self.file_handle.write('</revision>')

    if self.curr_tag == 'title': self.page_title = 0
    if self.curr_tag == 'ns': self.page_ns = 0
    if self.curr_tag == 'parentid': self.rev_parent_id = 0
    if self.curr_tag == 'timestamp': self.rev_timestamp = 0
    if self.curr_tag == 'contributor': self.rev_contrib = 0
    if self.curr_tag == 'username': self.rev_contrib_username = 0
    if self.curr_tag == 'comment': self.rev_comment = 0
    if self.curr_tag == 'model': self.rev_model = 0
    if self.curr_tag == 'format': self.rev_format = 0
    if self.curr_tag == 'text': self.rev_text = 0
    if self.curr_tag == 'sha1': self.rev_sha1 = 0     

  def characters(self, contents):
    self.content = contents  
    
    if self.curr_tag == 'title':
      self.file_handle.write('<title>' + contents + '</title>' + '\n')
    if self.curr_tag == 'ns':
      self.file_handle.write('<ns>' + contents + '</ns>')


if __name__ == '__main__':
  import argparse
  arg_parser = argparse.ArgumentParser(description='Script for dividing the large XML revision dump into individual page revisions.')
  arg_parser.add_argument('input_file', help='XML revision dump file name')
  arg_parser.add_argument('output_dir', help='Output directory')
  args = arg_parser.parse_args()
  if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

  # SAX XML reader
  xml_parser = xml.sax.make_parser()
  
  revision_dump_handler = WikiRevisionDumpHandler(args.input_file, args.output_dir)
  xml_parser.setContentHandler(revision_dump_handler)
  xml_parser.parse(args.input_file)
