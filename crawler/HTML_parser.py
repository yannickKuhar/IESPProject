from bs4 import BeautifulSoup
from datetime import datetime
import re

TAG = '[HTML PARSER]'

extensions = ["gif", "tif", "tiff", "bmp", "jpg", "jpeg", "png", "eps", "raw", "cr2", "nef", "orf", "sr2"]
page_extensions = ["PDF","DOC","DOCX","PPT","PPTX"]

def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


class HTMLParser:
    def __init__(self):
        self.soup = None

    def set_working_html(self, html):
        self.soup = BeautifulSoup(html, features='html.parser')
        # self.soup.prettify()

    def get_links(self):
        href_links = [i.get("href") for i in self.soup.find_all(href=True)]
        js_links = []
        rez = href_links
        for i in self.soup.find_all(onclick=True):
            parsed = Find(i.get("onclick"))
            if len(parsed) > 0:
                js_links.append(parsed)
        for l in js_links:
            rez += l
        links_to_crawl = [r for r in rez if r.split(".")[-1].upper() not in page_extensions]
        other_links = [r for r in rez if r.split(".")[-1].upper() in page_extensions]
        return rez

    def get_images(self):
        images = [(img.get("src"), img.get("src").split(".")[-1], datetime.now())
                  for img in self.soup.find_all('img') if img.get("src").split(".")[-1] in extensions]
        return images


temp = HTMLParser()
