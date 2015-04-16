import urllib.request
import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    em_text = False
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []
    def handle_starttag(self,tag,attrs):
        if tag == 'em' and len(attrs)>0 and re.match('contact-mobile',attrs[0][1]):
            self.em_text = True
        
        
                    
    def handle_endtag(self,tag):  
        if tag == 'em':  
            self.em_text = False
            
    def handle_data(self,data):  
        if self.em_text:  
            print (data) 

hp = MyHTMLParser()

start = "http://sh.ganji.com/fang1/1495616018x.htm"
content = urllib.request.urlopen(start).read()
content = content.decode('utf-8')
hp.feed(content)
hp.close()
