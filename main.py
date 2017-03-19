#!/usr/bin/python3
from SheetMusic import SheetMusic # converting UG HTML --> XHTML
from ebooklib import epub # compiling list of XHTML --> epub 
import os # for navigating through file system
import uuid # creating unique ids and filenames

sheets = list()
for infile in os.listdir('.'):
	if infile.endswith('.htm'):
		SM = SheetMusic(infile)
		random_filename = str(uuid.uuid4())
		sheet = {'tabs':SM.tabs,\
		'title':SM.title,\
		'file':random_filename}
		sheets.append(sheet)
sheets.sort(key=lambda x: x['title'])

book = epub.EpubBook()
book.set_identifier(str(uuid.uuid4()))
book.set_title('My Favourite Sheets')
book.set_language('en')
book.add_author('Your Name Here')

for s in sheets:
	c = epub.EpubHtml(title=s['title'], file_name=s['file'], lang='en')
	c.content = s['tabs']
	book.add_item(c)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ['nav', c]

# write to the file
epub.write_epub('test.epub', book, {})
