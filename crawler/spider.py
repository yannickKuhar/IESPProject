import time
from bs4 import BeautifulSoup


TAG = '[SPIDER]'


class Spider:
    def __init__(self, id, seed_url, web_driver, frontier_manager):
        self.id = id
        self.seed_url = seed_url
        self.web_driver = web_driver
        self.frontier_manager = frontier_manager

    def crawl(self):

        url = self.seed_url
        self.frontier_manager.add_to_history(url)

        while len(url) > 0:

            print(f'{TAG} [ID {self.id}] Crawling on {url}')

            self.web_driver.get(url)
            html = self.web_driver.page_source
            soup = BeautifulSoup(html, features='html.parser')

            # Get all links
            for link in soup.find_all('a'):
                self.frontier_manager.put(url, link.get('href', None))

            # Parse html and save to DB
            # for tag in soup.find_all('title'):
            #     print(f'{TAG} [ID {self.id}] Title: {tag}')

            if self.frontier_manager.frontier.empty():
                print(f'{TAG} [ID {self.id}] Stopped crawling. ')
                return

            url = self.frontier_manager.get()
