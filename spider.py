import urllib.request
import re
import csv
import http.cookiejar
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
                    if variable == "href" and re.search('^/fang1/\w*x.htm',value) :   
                        self.links.append(value)



class SetContent(HTMLParser):
    phone = False
    name = False
    
    def __init__(self):   
        HTMLParser.__init__(self)   
        self.content = {}
        
    def handle_starttag(self,tag,attrs):
        if tag == 'i' and len(attrs)>0 and re.match('fc-gray9',attrs[0][1]):
            self.name = True
        if tag == 'em' and len(attrs)>0 and re.match('contact-mobile',attrs[0][1]):
            self.phone = True

                    
    def handle_endtag(self,tag):
        if tag == 'i':
            self.name = False
        if tag == 'em':  
            self.phone = False
        
          
    def handle_data(self,data):  
        if self.phone:
            self.content["phone"] = data
        if self.name :
            self.content["name"] = data

        FIELDS = ['name', 'phone']   
        csv_file = open("d:/kehu.csv","r+",newline='')
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        #writer.writerow(dict(zip(FIELDS, FIELDS)))
        writer.writerow(self.content)
        csv_file.close()
        print("suceess")
        
        
                        
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
                  




start = "http://sh.ganji.com/fang1"
oper = makeMyOpener()
data = oper.open(start, timeout = 1000).read()
data = data.decode('utf-8')

hp = MyHTMLParser()
hp.feed(data)
hp.close()
hp.links = hp.links[::2]

s = SetContent()
for item in hp.links[::5] :
    if(len(item) != 0):
        item = "http://sh.ganji.com" + item
        print("url:",item)
        data = oper.open(item).read().decode('utf-8')
        s.feed(data)
s.close()
