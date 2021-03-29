import sys
import time
import socket
from datetime import datetime

import requests

from urllib.parse import urlparse
from urllib.error import URLError
import urlcanon
from sqlalchemy.exc import IntegrityError

from crawler.HTML_parser import HTMLParser
from crawler.robotparser import RobotFileParser
from crawler.doc_sim import doc_similarity

TAG = '[SPIDER]'
ERROR = '[ERROR]'

types = {
    "msword": "DOC",
    "vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",
    "pdf": "PDF",
    "vnd.ms-powerpoint": "PPT",
    "vnd.openxmlformats-officedocument.presentationml.presentation": "PPTX"
}


class Spider:
    def __init__(self, id, frontier_manager, database):
        self.id = id
        self.frontier_manager = frontier_manager
        self.working_domain_rules = RobotFileParser()
        self.previous_ip = None
        self.html_parser = HTMLParser()
        self.database = database
        self.working_url = self.frontier_manager.get()
        self.domain = None
        self.previous_domain = None
        self.set_working_domain_rules()
        self.current_site = None
        self.doc_sim = doc_similarity(self.database)
        # print(f'{TAG} Spider with Id: {id} init done.')

    def set_working_domain_rules(self):
        # Get current working URLs domain and parse its robots.txt file.
        if self.working_url is not None:
            current_domain = urlparse(self.working_url).netloc
            if self.domain != current_domain:
                self.domain = current_domain
                self.working_domain_rules.set_url('https://' + self.domain + '/robots.txt')
                try:
                    self.working_domain_rules.read()
                    if self.working_domain_rules is not None:
                        self.current_site = self.database.add_site({
                            "domain": self.domain,
                            "robots_content": self.working_domain_rules.raw,
                            "sitemap_content": "" if self.working_domain_rules.site_maps() is None else self.working_domain_rules.site_maps()
                        })
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
                response = None

                try:
                    response = requests.get(self.working_url, headers={'Content-type': 'content_type_value'})
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
                type = response.headers["Content-Type"].split(" ")[0].split("/")[1] if ";" not in response.headers["Content-Type"] else response.headers["Content-Type"].split(" ")[0][:-1].split("/")[
                    1]
                if type == "html":
                    self.html_parser.set_working_html(html)
                    similarity = self.doc_sim.similarity(html)

                    cannonized_url = urlcanon.parse_url(self.working_url)
                    urlcanon.whatwg(cannonized_url)

                    if similarity[0]:
                        try:
                            page = self.database.add_page({
                                "site_id": self.current_site.id,
                                "page_type_code": "HTML",
                                "url": str(cannonized_url),
                                "html_content": html,
                                "http_status_code": response.status_code,
                                "accessed_time": datetime.now()
                            })
                        except IntegrityError:
                            page = self.database.update_page_by_id(self.database.get_page_by_url(cannonized_url).id, {
                                "page_type_code": "HTML",
                                "html_content": html,
                                "response": response.status_code,
                                "accessed_time": datetime.now()
                            })
                    else:
                        similar_page = self.database.get_page_by_id(similarity[-1])
                        page = self.database.add_page({
                            "site_id": self.current_site.id,
                            "page_type_code": "DUPLICATE",
                            "url": str(cannonized_url),
                            "html_content": None,
                            "http_status_code": response.status_code,
                            "accessed_time": datetime.now()
                        })
                        page.add_link(similar_page)

                    _ = self.database.add_hash({
                        "of_page": page.id,
                        "hash0": similarity[1],
                        "hash1": similarity[2],
                        "hash2": similarity[3],
                        "hash3": similarity[4]
                    })

                    # Get all links.
                    for link in self.html_parser.get_links():
                        self.frontier_manager.put(self.working_url, link)
                        temp_ulr = urlcanon.parse_url(link)
                        urlcanon.whatwg(temp_ulr)
                        temp_page = self.database.add_page({
                            "url": temp_ulr,
                            "page_type_code": "FRONTIER",
                            "site_id": self.current_site.id
                        })
                        self.database.add_link(page, temp_page)

                    # Get all images
                    for filename, extension, accessed_time in self.html_parser.get_images():
                        self.database.add_image({
                            "page_id": page.id,
                            "filename": filename,
                            "content_type": extension,
                            "accessed_time": accessed_time,
                            "data": None
                        })
                elif type in types:
                    cannonized_url = urlcanon.parse_url(self.working_url)
                    urlcanon.whatwg(cannonized_url)
                    page = self.database.add_page({
                        "site_id": self.current_site.id,
                        "html_content": None,
                        "url": str(cannonized_url),
                        "accessed_time": datetime.now(),
                        "page_type_code": "BINARY"
                    })
                    self.database.add_page_data({
                        "page_id": page.id,
                        "data_type_code": types[type],
                        "data": None
                    })
                else:
                    print(f'{TAG} [ID {self.id}] Cant crawl on {self.working_url}, wrong data type!')
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
