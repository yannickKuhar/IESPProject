from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base, name_for_collection_relationship
from sqlalchemy.orm import Session
from datetime import datetime

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


class Db:

    @staticmethod
    def _name_for_collection_relationship(base, local_cls, referred_cls, constraint):
        if constraint.name:
            return constraint.name.lower()
        return name_for_collection_relationship(base, local_cls, referred_cls, constraint)

    def __init__(self):
        self.engine = create_engine("postgresql://postgres:admin@localhost/crawldb")
        self.session = Session(bind=self.engine)
        self.metadata = MetaData(schema="crawldb")
        Base = automap_base(bind=self.engine, metadata=self.metadata)
        Base.prepare(self.engine, reflect=True, name_for_collection_relationship=self._name_for_collection_relationship)
        self.Page = Base.classes.page
        self.Site = Base.classes.site
        self.Image = Base.classes.image
        self.Page_type = Base.classes.page_type
        self.Page_data = Base.classes.page_data
        self.Data_type = Base.classes.data_type

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


database = Db()
"""
site = database.add_site(
    {
        "domain": "gov2.si",
        "robots_content": "temp",
        "sitemap_content": "temp"
    }
)
database.add_page(
    {
        "site_id": site.id,
        "page_type_code": "HTML",
        "url": "gov2.si",
        "html_content": "<html></html>",
        "http_status_code": 200,
        "accessed_time": datetime.now()
    }
)
"""