import sys  
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawler.frontier_manager import FrontierManager
from crawler.spider import Spider

# from crawler.db import Db

PATH = 'C:\Program Files (x86)\chromedriver.exe'
TAG = '[CRAWLER]'


class Crawler:
    def __init__(self, workers):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # self.database = Db(workers)
        self.workers = workers
        self.frontier_manager = FrontierManager()
        self.web_driver = webdriver.Chrome(PATH, options=chrome_options)
        self.spiders = []

    def crawl(self):
        for i in range(self.workers):
            spider = Spider(id=i, web_driver=self.web_driver, frontier_manager=self.frontier_manager, database=None)
            thread = Thread(target=spider.crawl, daemon=True)
            thread.start()
            self.spiders.append(thread)

        for spider in self.spiders:
            spider.join()

        self.frontier_manager.frontier.join()


def main(args):
    workers = int(args[1])

    if workers <= 0:
        print(f'{TAG} [ERROR] Number of workers must be a positive integer!')
        return

    print(f'{TAG} Number of workers: {workers}')

    c = Crawler(workers=workers)
    c.crawl()


if __name__ == '__main__':
    main(sys.argv)
