from file_manager import FileManager
from validator import Validator
from scrapers import ScraperFactory

class Resources:
    def __init__(self, resource_type, args):
        self.validator = Validator(resource_type, args)
        self.file_manager = FileManager(resource_type, args)
        self.scraper = ScraperFactory().get_scraper(resource_type, args)

    def fetch(self):
        file_exists = self.file_manager.file_exists()
        if file_exists:
            return self.file_manager.read_json()
        else:
            resource_data = self.scraper.get_resource()
            self.file_manager.save_json(resource_data)
            return resource_data
    