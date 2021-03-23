import sys  
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from frontier_manager import FrontierManager
from spider import Spider

SEEDS = ['https://gov.si', 'https://evem.gov.si', 'https://e-uprava.gov.si', 'https://e-prostor.gov.si']
PATH = 'C:\Program Files (x86)\chromedriver.exe'


class Crawler:
    def __init__(self, workers, seed=0):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.workers = workers
        self.seed_url = SEEDS[seed]
        self.frontier_manager = FrontierManager()
        self.web_driver = webdriver.Chrome(PATH, options=chrome_options)
        self.spiders = []

    def crawl(self):
        for i in range(self.workers):
            s = Spider(id=i, seed_url=self.seed_url, web_driver=self.web_driver, frontier_manager=self.frontier_manager)
            t = Thread(target=s.crawl, daemon=True)
            t.start()
            self.spiders.append(t)

        for spider in self.spiders:
            spider.join()

        self.frontier_manager.frontier.join()


def main(args):
    c = Crawler(workers=5, seed=0)
    c.crawl()


if __name__ == '__main__':
    main(sys.argv)
