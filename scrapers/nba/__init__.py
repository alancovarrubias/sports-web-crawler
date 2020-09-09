from constant import TEAM, PLAYER, GAME, STAT
from .teams import NbaTeamsScraper
from .players import NbaPlayersScraper
from .games import NbaGamesScraper
from .stats import NbaStatsScraper


class NbaScraperFactory:
    def get_scraper(self, resource_type, args):
        if resource_type == TEAM:
            return NbaTeamsScraper(resource_type, args)
        if resource_type == PLAYER:
            return NbaPlayersScraper(resource_type, args)
        if resource_type == GAME:
            return NbaGamesScraper(resource_type, args)
        if resource_type == STAT:
            return NbaStatsScraper(resource_type, args)
