import urllib.request
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):   
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.links = []   
    def handle_starttag(self, tag, attrs):   
        #print "Encountered the beginning of a %s tag" % tag   
        if tag == "a":   
            if len(attrs) == 0:   
                pass   
            else:   
                for (variable, value) in attrs:   
                    if variable == "href":   
                        self.links.append(value)
                        
       

hp = MyHTMLParser()

start = "http://sh.ganji.com/fang1/"
data = urllib.request.urlopen(start).read()
data = data.decode('utf-8')
hp.feed(data)
hp.close()
#print(hp.links)
