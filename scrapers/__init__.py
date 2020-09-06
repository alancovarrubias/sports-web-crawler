from .nba import NbaScraper
from .mlb import MlbScraper


class ScraperFactory:
    def get_scraper(self, sport):
        if sport == "NBA":
            return NbaScraper()
        elif sport == "MLB":
            return MlbScraper()
