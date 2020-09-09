from scrapers.nba import NbaScraper
from scrapers.mlb import MlbScraper


class ScraperFactory:
    def get_scraper(self, resource_type, args):
        sport = args['sport']
        if sport == "NBA":
            return NbaScraper(resource_type, args)
        elif sport == "MLB":
            return MlbScraper(resource_type, args)
