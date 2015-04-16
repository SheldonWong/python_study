import urllib.request
import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    
    name = False
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []
        
    def handle_starttag(self,tag,attrs):
        if tag == 'i' :
            print(attrs)
  
            

hp = MyHTMLParser()

start = "http://sh.ganji.com/fang1/1495616018x.htm"
content = urllib.request.urlopen(start).read()
content = content.decode('utf-8')
hp.feed(content)
hp.close()
