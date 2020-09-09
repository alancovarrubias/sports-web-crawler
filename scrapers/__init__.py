from constant import NBA, MLB
from scrapers.nba import NbaScraperFactory
from scrapers.mlb import MlbScraperFactory


class ScraperFactory:
    def get_scraper(self, resource_type, args):
        scraper_factory = self.get_sport_scraper_factory(resource_type, args)
        return scraper_factory.get_scraper(resource_type, args)
    def get_sport_scraper_factory(self, resource_type, args):
        sport = args['sport']
        if sport == NBA:
            return NbaScraperFactory(resource_type, args)
        elif sport == MLB:
            return MlbScraperFactory(resource_type, args)
