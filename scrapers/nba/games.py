from constant import NBA_MONTHS
import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr
from operator import methodcaller


class NbaGamesScraper(AbstractScraper):
    def get_resource(self):
        games = []
        args = {}
        for month in NBA_MONTHS:
            args['month'] = month['text'].lower()
            games_table = self.get('games', args)
            css_config = {'rows': 'tr:not(.thead)', 'cells': 'th, td'}
            table_rows = get_table_rows(games_table, css_config)

            def get_game(row):
                date = row[0].text
                date_array = list(map(methodcaller('strip'), date.split(',')))
                game = {}
                game['year'] = int(date_array[-1])
                game['month'] = month['numeric']
                game['day'] = int(date_array[1].split()[-1])
                game['away_team'] = get_team_abbr(row[2])
                game['home_team'] = get_team_abbr(row[4])
                return game

            month_games = [get_game(row) for row in table_rows]
            games += month_games

        return {'games': games}