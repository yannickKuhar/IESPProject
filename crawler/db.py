from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import Session

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
        self.session = Session(bind=self.engine)

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