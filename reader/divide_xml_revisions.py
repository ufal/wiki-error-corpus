"""Divide the large XML revision dump file into per page revisions.

"""
import xml.sax

class WikiRevisionDumpHandler(xml.sax.ContentHandler):
  def __init__(self):
    self.current_tag = ''
   
    # Page and revision elements
    self.page_start = 0
    self.page_end = 0
    self.revision_start = 0
    self.revision_end = 0 

    # Elements under page
    self.page_title = 0
    self.page_id = 0
    self.page_ns = 0

    # Elements under revision
    self.rev_id = 0
    self.rev_timestamp = 0
    self.rev_contrib = 0
    self.rev_contrib_ip = 0
    self.rev_comment = 0 
    self.rev_model = 0
    self.rev_format = 0
    self.rev_text = 0 
    self.rev_sha1 = 0   

    self.content = ''

  def startElement(self, tag, attributes):
    self.current_tag = tag

    if self.current_tag == 'page': 
      self.page_start = 1
      self.page_end = 0

    if self.current_tag == 'revision':
      self.revision_start = 1
      self.revision_end = 1  
  
  def endElement(self, tag):
    self.current_tag = tag

  def characters(self, contents):
    self.content = contents      
    print contents
    print '\n'    


if __name__ == '__main__':
  import argparse
  arg_parser = argparse.ArgumentParser(description='Script for dividing the large XML revision dump into individual page revisions.')
  arg_parser.add_argument('input_file', help='XML revision dump file name')
  args = arg_parser.parse_args()
  
  # SAX XML reader
  xml_parser = xml.sax.make_parser()
  
  revision_dump_handler = WikiRevisionDumpHandler()
  xml_parser.setContentHandler(revision_dump_handler)
  xml_parser.parse(args.input_file)
