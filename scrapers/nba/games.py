import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows
from models.nba.game import NbaGame


NBA_MONTHS = (
    'october',
    'november',
    'december',
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
)
class NbaGamesScraper(AbstractScraper):
    def get_resource(self):
        games = []
        for month in NBA_MONTHS:
            season = self.key_store.args['season']
            endpoint = f'leagues/NBA_{season}_games-{month}.html'
            css_selectors = ('#schedule',)
            games_table = self.get_tables(endpoint, css_selectors)[0]
            css_config = {'rows': 'tr:not(.thead)', 'cells': 'th, td'}
            table_rows = get_table_rows(games_table, css_config)
            month_games = list(map(NbaGame, table_rows))
            games += month_games

        return {'games': games}