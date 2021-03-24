import sys
import time
import socket
from urllib.error import URLError

from selenium.common.exceptions import WebDriverException

from crawler.HTML_parser import HTMLParser
from crawler.robotparser import RobotFileParser
from urllib.parse import urlparse


TAG = '[SPIDER]'


class Spider:
    def __init__(self, id, web_driver, frontier_manager, database):
        self.id = id
        self.frontier_manager = frontier_manager
        self.working_domain_rules = RobotFileParser()
        self.previous_ip = None
        self.web_driver = web_driver
        self.html_parser = HTMLParser()
        self.database = database
        self.working_url = self.frontier_manager.get()

        self.set_working_domain_rules()

        # print(f'{TAG} Spider with Id: {id} init done.')

    def set_working_domain_rules(self):
        # Get current working URLs domain and parse its robots.txt file.
        if self.working_url is not None:

            domain = urlparse(self.working_url).netloc

            self.working_domain_rules.set_url('https://' + domain + '/robots.txt')

            try:
                self.working_domain_rules.read()
            except URLError as err:
                print(f'{TAG} [ID {self.id}] URLError occurred: {err}')
            except TimeoutError as err:
                print(f'{TAG} [ID {self.id}] TimeoutError occurred: {err}')

    def sleep_until(self, timeout):

        print(f'{TAG} [ID {self.id}] Is in sleep mode.')

        mustend = time.time() + timeout

        while time.time() < mustend:
            if not self.frontier_manager.frontier.empty():
                print(f'{TAG} [ID {self.id}] Is waking up.')
                return False

            time.sleep(5)

        return True

    def crawl(self):

        while True:
            # If the current working URL is None it means the spider was launched with an empty frontier and needs to do
            # a short sleep. After the sleep the frontier should be nonempty.
            if self.working_url is None:
                if self.sleep_until(30):
                    print(f'{TAG} [ID {self.id}] Stopped crawling, URL is None!')
                    return

            print(f'{TAG} [ID {self.id}] Crawling on {self.working_url}')

            # Check if its legal to crawl on this site.
            if self.working_domain_rules.can_fetch("*", self.working_url):

                crawl_delay = self.working_domain_rules.crawl_delay("*")
                domain = urlparse(self.working_url).netloc
                ip = None

                try:
                    ip = socket.gethostbyname(domain)
                except socket.gaierror as err:
                    print(f'{TAG} [ID {self.id}] Socket error: {err}')
                except:
                    print(f'{TAG} [ID {self.id}] Unexpected error:{sys.exc_info()[0]}')

                # If we sent a request to the same ip address sleep for 5 seconds to preserve server stability.
                if crawl_delay is not None:
                    time.sleep(float(crawl_delay))
                elif self.previous_ip is not None and ip == self.previous_ip:
                    print(f'{TAG} [ID {self.id}] Is sleeping for 5 seconds!')
                    time.sleep(5)

                self.previous_ip = ip

                # Add site_maps URLs from robots.txt file to frontier if they exist.
                if self.working_domain_rules.site_maps() is not None:
                    for site_map_url in list(self.working_domain_rules.site_maps()):
                        # print(f'{TAG} [ID {self.id}] Site map url: {site_map_url}')
                        self.frontier_manager.put(self.working_url, site_map_url)

                # Get HTML code fom web page on working URL.
                try:
                    self.web_driver.get(self.working_url)
                except URLError as err:
                    print(f'{TAG} [ID {self.id}] URLError occurred: {err}')
                except TimeoutError as err:
                    print(f'{TAG} [ID {self.id}] TimeoutError occurred: {err}')
                except WebDriverException as err:
                    print(f'{TAG} [ID {self.id}] WebDriverException occurred: {err}')
                except:
                    print(f'{TAG} [ID {self.id}] Unexpected error:{sys.exc_info()[0]}')

                html = self.web_driver.page_source

                # Set working html code.
                self.html_parser.set_working_html(html)

                # Get all links.
                for link in self.html_parser.get_links():
                    self.frontier_manager.put(self.working_url, link)

                # Terminate if frontier remains empty for 60 seconds. In the mean time check every 10 seconds if new
                # URLs were added. If yes continue working, if no terminate crawling.
                if self.frontier_manager.frontier.empty():
                    if self.sleep_until(60):
                        print(f'{TAG} [ID {self.id}] Stopped crawling.')
                        return

            else:
                print(f'{TAG} [ID {self.id}] Cant crawl on {self.working_url}, it is illegal!')

            self.working_url = self.frontier_manager.get()
            self.set_working_domain_rules()
