import sys
import time
import socket
import requests

from urllib.parse import urlparse
from urllib.error import URLError

from crawler.HTML_parser import HTMLParser
from crawler.robotparser import RobotFileParser


TAG = '[SPIDER]'
ERROR = '[ERROR]'


class Spider:
    def __init__(self, id, frontier_manager, database):
        self.id = id
        self.frontier_manager = frontier_manager
        # self.working_domain_rules = RobotFileParser()
        self.working_domain_rules = None
        self.previous_ip = None
        self.html_parser = HTMLParser()
        self.database = database
        self.working_url = self.frontier_manager.get()

        self.set_working_domain_rules()

        # print(f'{TAG} Spider with Id: {id} init done.')

    def set_working_domain_rules(self):
        # Get current working URLs domain and parse its robots.txt file.
        if self.working_url is not None:

            domain = urlparse(self.working_url).netloc

            rules = self.frontier_manager.get_domain_rules(domain)

            if rules is not None:
                self.working_domain_rules = rules
            else:
                robots_url = f'https://{domain}/robots.txt'
                new_rules = RobotFileParser()
                new_rules.set_url(robots_url)

                try:
                    new_rules.read()
                except URLError as err:
                    print(f'{TAG} [ID {self.id}] URLError occurred: {err}')
                except TimeoutError as err:
                    print(f'{TAG} [ID {self.id}] TimeoutError occurred: {err}')

                self.frontier_manager.put_domain_rules(domain, new_rules)
                self.working_domain_rules = new_rules

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
                response = None

                try:
                    response = requests.get(self.working_url)
                except requests.HTTPError:
                    print(f'{TAG} [ID {self.id}] {ERROR} An HTTP error occurred.')
                except requests.ConnectionError:
                    print(f'{TAG} [ID {self.id}] {ERROR} A Connection error occurred.')
                except requests.URLRequired:
                    print(f'{TAG} [ID {self.id}] {ERROR} A valid URL is required to make a request.')
                except requests.TooManyRedirects:
                    print(f'{TAG} [ID {self.id}] {ERROR} Too many redirects.')
                except requests.ReadTimeout:
                    print(f'{TAG} [ID {self.id}] {ERROR} The server did not send any data in the allotted amount of time.')
                except requests.Timeout:
                    print(f'{TAG} [ID {self.id}] {ERROR} The request timed out.')
                except requests.RequestException as e:
                    print(e)
                except:
                    print(f'{TAG} [ID {self.id}] Unexpected error:{sys.exc_info()[0]}')

                if response is not None:
                    html = response.text
                else:
                    print(f'{TAG} [ID {self.id}] {ERROR} Response is None!')
                    continue

                # Set working html code.
                self.html_parser.set_working_html(html)

                # Get all links.
                for link in self.html_parser.get_links():
                    self.frontier_manager.put(self.working_url, link)
            else:
                print(f'{TAG} [ID {self.id}] Cant crawl on {self.working_url}, it is illegal!')

            # Terminate if frontier remains empty for 60 seconds. In the mean time check every 10 seconds if new
            # URLs were added. If yes continue working, if no terminate crawling.
            if self.frontier_manager.frontier.empty():
                if self.sleep_until(60):
                    print(f'{TAG} [ID {self.id}] Stopped crawling.')
                    return

            self.working_url = self.frontier_manager.get()
            self.set_working_domain_rules()
