"""Divide the large XML revision dump file into per page revisions.

"""
import codecs
import os
import xml.sax

class WikiRevisionDumpHandler(xml.sax.ContentHandler):
  input_file = 'wiki.xml'
  output_dir = '.'
 
  wiki_dump_tags = {'page': 'page', 'title': 'title', 'ns': 'ns', 
                    'id': 'id', 'parentid': 'parentid',  'rev': 'revision',
                    'tstamp': 'timestamp', 'contrib': 'contributor', 
                    'ip': 'ip', 'uname': 'username', 'comment': 'comment',
                    'model': 'model', 'format': 'format', 'text': 'text',
                    'sha1': 'sha1'}
 
  file_counter = 0
  file_handle = ''
  
 
  def __init__(self, input_file, output_dir):
    # Input/output locations
    self.input_file = input_file
    self.output_dir = output_dir

    # Recent tag visited by SAX parser
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

    if self.curr_tag == wiki_dump_tags['page']: 
      self.page_start = 1
      # close the unclosed handles first if any
      if self.file_handle:
        self.file_handle.close()
      fname = repr(self.file_counter).zfill(10) + '.xml'
      abspath = self.output_dir + '/' + fname
      self.file_handle = codecs.open(abspath, 'w', 'utf-8')
      self.file_handle.write(tag_start(wiki_dump_tags['page'])+'\n')

    if self.curr_tag == wiki_dump_tags['rev']: 
      self.revision_start = 1
      self.file_handle.write(tag_start(wiki_dump_tags['rev'])+'\n')

    if self.curr_tag == wiki_dump_tags['title']: self.page_title = 1

    if self.curr_tag == wiki_dump_tags['id']: 
      if self.page_start and not self.revision_start: 
        self.page_id = 1
      elif self.revision_start and not self.rev_contrib:
        self.rev_id = 1
      elif self.rev_contrib:
        self.rev_contrib_userid = 1

    if self.curr_tag == wiki_dump_tags['ns']: self.page_ns = 1
    if self.curr_tag == wiki_dump_tags['parentid']: self.rev_parent_id = 1
    if self.curr_tag == wiki_dump_tags['tstamp']: self.rev_timestamp = 1
    if self.curr_tag == wiki_dump_tags['contrib']: 
      self.rev_contrib = 1
      self.file_handle.write(tag_start(wiki_dump_tags['contrib']))
    if self.curr_tag == wiki_dump_tags['uname']: self.rev_contrib_username = 1
    if self.curr_tag == wiki_dump_tags['ip']: self.rev_contrib_ip = 1
    if self.curr_tag == wiki_dump_tags['comment']: self.rev_comment = 1
    if self.curr_tag == wiki_dump_tags['model']: self.rev_model = 1
    if self.curr_tag == wiki_dump_tags['format']: self.rev_format = 1
    if self.curr_tag == wiki_dump_tags['text']: self.rev_text = 1
    if self.curr_tag == wiki_dump_tags['sha1']: self.rev_sha1 = 1       
  
  def endElement(self, tag):
    self.current_tag = tag

    if self.curr_tag == wiki_dump_tags['page']: 
      self.page_start = 0
      self.file_handle.write(tag_end(wiki_dump_tags['page']+'\n')
      self.file_handle.close()
      self.file_counter += 1

    if self.curr_tag == wiki_dump_tags['rev']: 
      self.revision_start = 0
      self.file_handle.write(tag_end(wiki_dump_tags['rev']+'\n')

    if self.curr_tag == wiki_dump_tags['title']: self.page_title = 0
    if self.curr_tag == wiki_dump_tags['ns']: self.page_ns = 0
    if self.curr_tag == wiki_dump_tags['parentid']: self.rev_parent_id = 0
    if self.curr_tag == wiki_dump_tags['tstamp']: self.rev_timestamp = 0
    if self.curr_tag == wiki_dump_tags['contrib']: 
      self.rev_contrib = 0
      self.file_handle.write(tag_end(wiki_dump_tags['contrib']))
    if self.curr_tag == wiki_dump_tags['uname']: self.rev_contrib_username = 0
    if self.curr_tag == wiki_dump_tags['ip']: self.rev_contrib_ip = 0
    if self.curr_tag == wiki_dump_tags['comment']: self.rev_comment = 0
    if self.curr_tag == wiki_dump_tags['model']: self.rev_model = 0
    if self.curr_tag == wiki_dump_tags['format']: self.rev_format = 0
    if self.curr_tag == wiki_dump_tags['text']: self.rev_text = 0
    if self.curr_tag == wiki_dump_tags['sha1']: self.rev_sha1 = 0     

  def characters(self, contents):
    self.content = contents  
    
    if self.curr_tag == wiki_dump_tags['title']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['title'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['ns']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['ns'], 
                             self.content) + '\n')

    if self.curr_tag == wiki_dump_tags['id']:
      if self.rev_contrib_userid:
        self.rev_contrib_userid = 0
      if self.rev_id:
        self.rev_id = 0
      if self.page_id:
        self.page_id = 0
      self.file_handle.write(surround_with_tag(wiki_dump_tags['id'], 
                             self.content) + '\n')
    
    if self.curr_tag == wiki_dump_tags['parentid']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['parentid'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['tstamp']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['tstamp'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['uname']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['uname'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['comment']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['comment'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['model']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['model'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['format']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['format'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['text']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['text'], 
                             self.content) + '\n')
    if self.curr_tag == wiki_dump_tags['sha1']:
      self.file_handle.write(surround_with_tag(wiki_dump_tags['sha1'], 
                             self.content) + '\n')

  @staticmethod    
  def surround_with_tag(tag, cont): return '<'+tag+'>'+cont+'</'+tag+'>'

  @staticmethod
  def tag_start(tag): return '<'+tag+'>'
  
  @staticmethod
  def tag_end(tag): return '</'+tag+'>'
    

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
