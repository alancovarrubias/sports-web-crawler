from abc import ABC, abstractmethod
from web_driver import WebDriver


class AbstractScraper(ABC):
    def __init__(self):
        self.web_driver = WebDriver()

    def get(self, resource, args):
        return self.web_driver.get(resource, args)

    @abstractmethod
    def get_table_data(self):
        pass

    @abstractmethod
    def get_teams(self, args):
        pass

    @abstractmethod
    def get_players(self, args):
        pass

    @abstractmethod
    def get_games(self, args):
        pass

    @abstractmethod
    def get_stats(self, args):
        pass
