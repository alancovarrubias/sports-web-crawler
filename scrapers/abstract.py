from abc import ABC, abstractmethod
from web_driver import WebDriver


class AbstractScraper(ABC):
    def __init__(self, resource_type, args):
        self.web_driver = WebDriver(resource_type, args)

    def get(self, resource, args):
        return self.web_driver.get()

    @abstractmethod
    def get_resource(self):
        pass
