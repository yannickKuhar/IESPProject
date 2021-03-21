from bs4 import BeautifulSoup


TAG = '[HTML PARSER]'


class HTMLParser:
    def __init__(self):
        self.soup = None

    def set_working_html(self, html):
        self.soup = BeautifulSoup(html, features='html.parser')
        self.soup.prettify()

    def get_links(self):
        return [link.get('href', None) for link in self.soup.find_all('a')]

    def get_images(self):
        images = self.soup.find_all('img')
        # TODO: parse <img><\img> to get src links (download and encode images?).
        return images

    def get_content(self):
        # TODO: get text from html, remove stop words and stem them. Also content type if != html don't parse text
        #  just remember content type (pdf, docx, ppt, ...).
        pass


