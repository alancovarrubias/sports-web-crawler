from constant import TEAM, PLAYER, GAME, STAT
from .teams import MlbTeamsScraper
from .players import MlbPlayersScraper
from .games import MlbGamesScraper
from .stats import MlbStatsScraper


class MlbScraperFactory:
    def get_scraper(self, resource_type, args):
        if resource_type == TEAM:
            return MlbTeamsScraper(resource_type, args)
        if resource_type == PLAYER:
            return MlbPlayersScraper(resource_type, args)
        if resource_type == GAME:
            return MlbGamesScraper(resource_type, args)
        if resource_type == STAT:
            return MlbStatsScraper(resource_type, args)
