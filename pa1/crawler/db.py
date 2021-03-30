from sqlalchemy import create_engine, MetaData, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import exists

from pyvis.network import Network
import networkx as nx

"""
Class for working with database. 
Few rules: 
    - This class is meant for only working with database. What you are passing to it is up to you to parse.
    - When adding new entry you should pass data in dictionary in type of 
        {'name':'value'}. If you dont know the fields call Db.<table_name>_fields().  
    - Before creating new page you should create new site first, so that you get id of the site entry.
    - Before creating new image you should create new page first, so that you get id of page entry. 
    - Before creating new page data you should create new page first, so that you get id of page entry.
"""


def _name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    if constraint.name:
        return constraint.name.lower()
    return name_for_collection_relationship(base, local_cls, referred_cls, constraint)


class Db:
    def __init__(self, pool_size):
        self.engine = create_engine("postgresql://postgres:admin@localhost/crawldb", pool_size=pool_size)
        self.metadata = MetaData(schema="crawldb")
        self.Base = automap_base(bind=self.engine, metadata=self.metadata)
        self.Base.prepare(self.engine, reflect=True, name_for_collection_relationship=_name_for_collection_relationship)
        self.Page = self.Base.classes.page
        self.Site = self.Base.classes.site
        self.Image = self.Base.classes.image
        self.Page_type = self.Base.classes.page_type
        self.Page_data = self.Base.classes.page_data
        self.Data_type = self.Base.classes.data_type
        self.Hashes = self.Base.classes.hashes
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = scoped_session(self.session_factory)

    @staticmethod
    def page_fields():
        return ["site_id", "page_type_code", "url", "html_content", "http_status_code", "accessed_time"]

    @staticmethod
    def site_fields():
        return ["domain", "robots_content", "sitemap_content"]

    @staticmethod
    def image_fields():
        return ["page_id", "filename", "content_type", "data", "accessed_time"]

    @staticmethod
    def page_data_fields():
        return ["page_id", "data_type_code", "data"]

    def add_page(self, data):
        try:
            new_Page = self.Page(**data)
            self.session.add(new_Page)
            self.session.commit()
            return new_Page
        except IntegrityError:
            self.session.rollback()
            raise IntegrityError

    def add_site(self, data):
        new_Site = self.Site(**data)
        self.session.add(new_Site)
        self.session.commit()
        return new_Site

    def add_page_data(self, data):
        new_Page_data = self.Page_data(**data)
        self.session.add(new_Page_data)
        self.session.commit()
        return new_Page_data

    def add_image(self, data):
        new_Image = self.Image(**data)
        self.session.add(new_Image)
        self.session.commit()
        return new_Image

    def add_link(self, page1, page2):
        page1.fk_link_page.append(page2)
        self.session.add(page1)
        self.session.commit()
        return page1

    def add_hash(self, data):
        new_Hash = self.Hashes(**data)
        self.session.add(new_Hash)
        self.session.commit()
        return new_Hash

    def get_page_by_id(self, id):
        return self.session.query(self.Page).get(id)

    def get_page_by_url(self, url):
        return self.session.execute(self.session.query(self.Page).where(self.Page.url == url)).first()[0]

    def update_page_by_id(self, id, new_data):
        self.session.execute(update(self.Page).where(self.Page.id == id).values(**new_data))
        self.session.commit()
        page = self.session.query(self.Page).get(id)
        return page

    def check_if_page_exists(self, url):
        ex = self.session.query(exists().where(self.Page.url == url)).scalar()
        return ex

    def check_if_hash_of_page_exists(self, of_page):
        ex = self.session.query(exists().where(self.Hashes.of_page == of_page)).scalar()
        return ex

    def get_all_hashes(self):
        res = self.session.query(self.Hashes).all()
        h0 = []
        h1 = []
        h2 = []
        h3 = []
        ids = []
        for hashes in res:
            ids.append(hashes.of_page)
            h0.append(hashes.hash0)
            h1.append(hashes.hash1)
            h2.append(hashes.hash2)
            h3.append(hashes.hash3)

        return ids, h0, h1, h2, h3

    def delete_table(self, which):
        self.session.execute(text("delete from crawldb." + which))
        self.session.commit()

    def print_base(self):
        pages = self.session.query(self.Page).all()
        hashes = self.session.query(self.Hashes).all()
        print("PAGES:\n{id: <3} {html_content: <3500}".format(id="id", html_content="Html content"), )
        for page in pages:
            print("{id: <3} {html_content: <3500}".format(id=page.id, html_content=page.html_content))
        print("\nHASHES:\n{Page_id: <3} {Hash0: <8} {Hash1: <8} {Hash2: <8} {Hash3: <8}".format(Page_id="Page_id", Hash0="hash0",
                                                                                                Hash1="Hash1",
                                                                                                Hash2="Hash2",
                                                                                                Hash3="Hash3"))
        for hash in hashes:
            print("{Page_id: <3} {Hash0: <8} {Hash1: <8} {Hash2: <8} {Hash3: <8}".format(Page_id=hash.of_page, Hash0=hash.hash0, Hash1=hash.hash1, Hash2=hash.hash2, Hash3=hash.hash3))
        print("==========================================")

    def visualize(self):
        net = Network("1200px", "1200px")
        from_pages = self.session.execute(text("SELECT crawldb.link.from_page from crawldb.link"))
        from_pages = [(page, self.get_page_by_id(page).url) for page in set([rez[0] for rez in from_pages])]
        to_pages = self.session.execute(text("SELECT crawldb.link.to_page from crawldb.link"))
        to_pages = [(page, self.get_page_by_id(page).url) for page in set([rez[0] for rez in to_pages])]
        for node_id, url in from_pages+to_pages:
            net.add_node(node_id, label=url)
        edges = self.session.execute(text("SELECT crawldb.link.from_page,crawldb.link.to_page from crawldb.link"))
        for edge in edges:
            net.add_edge(edge[0], edge[1])
        net.show("links.html")


"""
db = Db(10)
db.visualize()
"""