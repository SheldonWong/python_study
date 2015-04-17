import urllib.request
import re
from html.parser import HTMLParser

class GetLinks(HTMLParser):
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        if tag == "a":   
            if len(attrs) == 0:   
                pass   
            else:   
                for (variable, value) in attrs:   
                    if variable == "href" and re.search('^/fang1/\w*x.htm',value):   
                        self.links.append(value)
       
        
hp = GetLinks()

start = "http://sh.ganji.com/fang1/o1"
data = urllib.request.urlopen(start).read()
data = data.decode('utf-8')
hp.feed(data)
hp.close()
print(hp.links)



