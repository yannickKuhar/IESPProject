from bs4 import BeautifulSoup


TAG = '[HTML PARSER]'


class HTMLParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, features='html.parser')
        self.soup.prettify()

    def get_links(self):
        return [link.get('href', None) for link in self.soup.find_all('a')]

    def get_images(self):
        pass


