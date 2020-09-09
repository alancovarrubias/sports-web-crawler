from constants.sports import NBA, MLB
from scrapers.nba import NbaScraperFactory
from scrapers.mlb import MlbScraperFactory


class ScraperFactory:
    def get_scraper(self, resource_type, args):
        sport = args['sport']
        if sport == NBA:
            return NbaScraperFactory().get_scraper(resource_type, args)
        elif sport == MLB:
            return MlbScraperFactory().get_scraper(resource_type, args)
    
