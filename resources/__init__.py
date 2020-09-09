from file_manager import FileManager
from validator import Validator
from scrapers import ScraperFactory
from key_store import KeyStore

class Resources:
    def __init__(self, resource_type, args):
        key_store = KeyStore(resource_type, args)
        validator = Validator(key_store)
        self.file_manager = FileManager(key_store)
        self.scraper = ScraperFactory().get_scraper(key_store)
        self.valid = validator.validate_args()

    def fetch(self):
        file_exists = self.file_manager.file_exists()
        if file_exists:
            return self.file_manager.read_json()
        else:
            resource_data = self.scraper.get_resource()
            self.file_manager.save_json(resource_data)
            return resource_data
    