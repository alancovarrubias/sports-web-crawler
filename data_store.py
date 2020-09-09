from file_manager import FileManager
from validator import Validator
from scrapers import ScraperFactory

class DataStore:
    def __init__(self, resource_type, args):
        self.file_manager = FileManager(resource_type, args)
        self.scraper = ScraperFactory().get_scraper(args)

    def get_resource(self):
        file_exists = self.file_manager.file_exists()
        if file_exists:
            return self.file_manager.read_json()
        else:
            table_data = self.scraper.get_table_data()
            self.file_manager.save_json(table_data)
    
