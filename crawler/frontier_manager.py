import re
import urlcanon
# TODO: Store only canon URLs!

from threading import Lock
from queue import Queue
from urllib.parse import urljoin

TAG = '[FRONTIER MANAGER]'
SEEDS = ['https://gov.si', 'https://evem.gov.si', 'https://e-uprava.gov.si', 'https://e-prostor.gov.si']


class FrontierManager:
    def __init__(self):
        self. lock = Lock()
        self.frontier = Queue()
        self.url_regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        self.gov_regex = re.compile('.*gov\.si.*', re.IGNORECASE)
        self.history = []
        self.domain_rules = {}

        for seed in SEEDS:
            self.frontier.put(seed)

    def put_domain_rules(self, domain, rules):
        with self.lock:
            self.domain_rules[domain] = rules

    def get_domain_rules(self, domain):
        with self.lock:
            # print(f'{TAG} Domains: {self.domain_rules.keys()}')
            if domain in self.domain_rules:
                return self.domain_rules[domain]

            return None

    def put(self, seed, url):
        if url is None:
            return

        # Is input valid URL
        if not re.match(self.url_regex, url):
            # print(f'{TAG} string: {url} is not a valid URL!')
            # print(seed, url, urljoin(seed, url).rstrip('/'))
            url = urljoin(seed, url).rstrip('/')

        # Is input valid gov.si URL
        if not re.match(self.gov_regex, url):
            # print(f'{TAG} string: {url} is not a valid gov URL!')
            return

        # Check for duplicates.
        with self.lock:
            if url not in self.history:
                self.history.append(url)
            else:
                # print(f'{TAG} string: {url} is a duplicate!')
                return

            self.frontier.put(url)

    def get(self):
        with self.lock:
            val = None
            if not self.frontier.empty():
                val = self.frontier.get()
                self.frontier.task_done()
        return val
