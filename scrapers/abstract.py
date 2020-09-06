from abc import ABC, abstractmethod
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os


class AbstractScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        options = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(options, options=chrome_options)
        super().__init__()

    def get(self, endpoint):
        url = os.path.join(self.base_url, endpoint)
        print(url)
        self.driver.get(url)

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
