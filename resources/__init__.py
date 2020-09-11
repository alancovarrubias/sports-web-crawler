from resources.db_manager import DbManager
from crawlers import ScraperFactory

class Resources:
    def __init__(self, key_store):
        self.db_manager = DbManager(key_store)
        self.scraper = ScraperFactory().get_scraper(key_store)

    def fetch(self):
        file_exists = self.db_manager.resource_exists()
        if file_exists:
            return self.db_manager.fetch_resource()
        else:
            resource_data = self.scraper.get_resource()
            self.db_manager.save_resource(resource_data)
            return resource_data
    