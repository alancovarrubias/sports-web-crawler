import re
from constants.nba import MONTHS
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr
from operator import methodcaller


class NbaGamesScraper(AbstractScraper):
    def get_resource(self):
        games = []
        for month in MONTHS:
            season = self.args['season']
            month_text = month['text']
            endpoint = f'leagues/NBA_{season}_games-{month_text}.html'
            css_selectors = ('#schedule',)
            games_table = self.get_tables(endpoint, css_selectors)[0]
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