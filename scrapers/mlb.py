from operator import methodcaller
import re
from .abstract import AbstractScraper
from .helpers import get_table_rows, get_team_abbr


class MlbScraper(AbstractScraper):
    def __init__(self):
        base_url = 'https://www.baseball-reference.com'
        super().__init__(base_url)

    def get_teams(self, args):
        season = args['season']
        self.get(f'leagues/MLB/{season}.shtml')
        teams_table = self.driver.find_element_by_id('teams_standard_batting')
        table_rows = get_table_rows(teams_table, 'th')[:-1]

        def get_team(row):
            anchor = row[0].find_element_by_tag_name('a')
            title = anchor.get_attribute('title')
            words = title.split(' ')
            team = {}
            team['abbr'] = anchor.text
            if re.search("Sox|Jays", title):
                team['name'] = ' '.join(words[-2:])
                team['city'] = ' '.join(words[:-2])
            else:
                team['name'] = ' '.join(words[-1:])
                team['city'] = ' '.join(words[:-1])
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

    def get_games(self):
        pass

    def get_stats(self):
        pass
