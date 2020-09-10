import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr


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

            def get_game(row):
                game = {}
                game['date'] = row[0].get_attribute('csk')[:-4]
                game['away_team'] = get_team_abbr(row[2])
                game['home_team'] = get_team_abbr(row[4])
                return game

            month_games = [get_game(row) for row in table_rows]
            games += month_games

        return {'games': games}