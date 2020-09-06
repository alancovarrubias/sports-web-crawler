from operator import methodcaller
import re
from .abstract import AbstractScraper
from .helpers import get_table_rows, get_team_abbr


class MlbScraper(AbstractScraper):
    def __init__(self):
        base_url = 'https://www.baseball-reference.com'
        super().__init__(base_url)

    def get_teams(self, season):
        self.get(f'leagues/MLB/{season}.shtml')
        teams_table = self.driver.find_element_by_id(
            'team_vs_team')
        table_rows = get_table_rows(teams_table)

        def get_team(row):
            team = {}
            text_array = row[0].text.split()
            if text_array[-1] == "Blazers":
                team['name'] = ' '.join(text_array[1:])
                team['city'] = text_array[0]
            else:
                team['name'] = text_array[-1]
                team['city'] = ' '.join(text_array[:-1])
            team['abbr'] = get_team_abbr(row[0])
            return team
        return [get_team(row) for row in table_rows]

    def get_players(self, args):
        season = args['season']
        team = args['team']

        self.get(f'teams/{team}/{season}.html')
        players_table = self.driver.find_element_by_id(
            'roster')
        table_rows = get_table_rows(players_table)

        def get_player(row):
            player = {}
            player['name'] = row[0].text
            player['abbr'] = row[0].get_attribute('data-append-csv')
            player['position'] = row[1].text
            return player

        return [get_player(row) for row in table_rows]
