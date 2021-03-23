# import time
from HTML_parser import HTMLParser


TAG = '[SPIDER]'


# TODO: Read robot.txt
class Spider:
    def __init__(self, id, seed_url, web_driver, frontier_manager, database):
        self.id = id
        self.working_url = seed_url
        self.web_driver = web_driver
        self.frontier_manager = frontier_manager
        self.html_parser = HTMLParser()
        self.database = database

    def crawl(self):

        while len(self.working_url) > 0:

            # TODO: Get URL domain and its robot.txt.

            print(f'{TAG} [ID {self.id}] Crawling on {self.working_url}')

            # Get HTML code fom web page on working URL.
            self.web_driver.get(self.working_url)
            html = self.web_driver.page_source

            # Set working html code.
            self.html_parser.set_working_html(html)

            # Get all links (also do document.location)
            for link in self.html_parser.get_links():
                self.frontier_manager.put(self.working_url, link)

            # TODO: Other termination condition, this is suboptimal.
            if self.frontier_manager.frontier.empty():
                print(f'{TAG} [ID {self.id}] Stopped crawling. ')
                return

            self.working_url = self.frontier_manager.get()
