from html.parser import HTMLParser
import glob
from .config_io import read_config

class DocConverter:
    """
    Need to convert statically generated doc to use jinja template syntax, otherwise I can't serve it
    via the same VirtualHost ... due to lack of skill with Apache I guess.
    """

    def __init__(self, doc_dir: str):
        # for now, only for testing use only index.html ...
        self.files = glob.glob(doc_dir + "/index.html")
        self.template_dir = read_config()['path_to_templates']
        self.html_parser = _DocHTMLParser()

    def convert(self):        
        for f in self.files:
            self._convert_single(f)

    def _convert_single(self, html_file: str):
        html_content = open(html_file, 'r').read()
        self.html_parser.feed()


class _DocHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.converted_html = ''

    def handle_starttag(self, tag, attrs):
        print(attrs)
        

    
