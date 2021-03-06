import re # regex for extracting the songtitle out of the html title
from bs4 import BeautifulSoup # scraper
import uuid # for generating unique filenames 

class SheetMusic:
	TABS_IDENTIFIER = {'class':'js-tab-content'}
	TITLE_REGEX = '(.+)\sby\s(.+)@.+'
	TEMPLATE_FILE = 'template.xhtml'
	def __init__(self,filepath):
		with open (filepath, 'r') as infile:
			self.parse_html(infile.read())
		self.tabs = SheetMusic.add_structure(self.tabs)
		self.add_h1title()

	def parse_html(self,content):
		soup = BeautifulSoup(content, 'html.parser')
		regex = re.search(self.TITLE_REGEX, soup.title.string)
		try:
			self.title = regex.groups()[0] # just the title
			self.author = regex.group()[1] # just the author
		except AttributeError: # does not match the regex
			self.title = soup.title.title()
			self.author = ''
		self.title = self.title.title() # capitalises the first letter of every word
		self.tabs = soup.find(attrs=self.TABS_IDENTIFIER).text

	@staticmethod
	def add_structure(strin):
		'''
		There is no further formatting inside the <pre>-element of the
		UG-HTML file. To make the sheet usable and nice looking on any
		device, we need to add a bit of HTML structure.
		'''
		strout = strin
		strout = strout.replace('\n\n','</p><p>')
		strout = strout.replace('\n','<br/>')
		strout = strout.replace('</p>','</p>\n')
		strout = strout.replace(' ','&nbsp;') #aligning chords & lyrics
		return strout

	def add_h1title(self):
		self.tabs='<h1>'+self.title+'</h1>'+self.tabs

	def create_xhtml(self,filename):
		'''
		We could create a XML file using designated and complex XML 
		creation tools, set up a XML trees, schemes, namespaces etc.
		Or we can just paste the extracted content into an existing
		XHTML template file and replace placeholdes where it's necessary.
		Unless it's necessary or gives more comfort we choose the 
		simple method.
		'''
		with open(self.TEMPLATE_FILE, 'r') as template:
			self.xhtml = template.read()
			self.xhtml = self.xhtml.replace('#SONGTITLE#',self.title)
			self.xhtml = self.xhtml.replace('#TABS#',self.tabs)
		with open(filename,'w') as outfile:
			outfile.write(self.xhtml)
		return filename
