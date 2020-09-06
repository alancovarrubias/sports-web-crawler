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
        table_rows = get_table_rows(teams_table, {'cells': 'th'})[:-1]

        def get_team(row):
            anchor = row[0].find_element_by_tag_name('a')
            title = anchor.get_attribute('title')
            words = title.split(' ')
            team = {}
            team['abbr'] = anchor.text
            if re.search(r"Sox|Jays", title):
                team['name'] = ' '.join(words[-2:])
                team['city'] = ' '.join(words[:-2])
            else:
                team['name'] = ' '.join(words[-1:])
                team['city'] = ' '.join(words[:-1])
            return team
        teams = [get_team(row) for row in table_rows]
        return {'teams': teams}

    def get_players(self, args):
        season = args['season']
        team = args['team']

        self.get(f'teams/{team}/{season}.shtml')
        players_table = self.driver.find_element_by_id('team_batting')

        table_rows = get_table_rows(players_table)

        def get_player(row):
            player = {}
            player['name'] = row[1].find_element_by_tag_name('a').text
            player['abbr'] = row[1].get_attribute('data-append-csv')
            player['position'] = row[0].text
            return player

        players = [get_player(row) for row in table_rows]
        return {'players': players}

    def get_games(self, args):
        season = args['season']
        teams = args['teams'].split(',')
        games = []
        team_links = {}
        for team in teams:
            self.get(f'teams/{team}/{season}-schedule-scores.shtml')
            games_table = self.driver.find_element_by_id('team_schedule')
            rows = get_table_rows(games_table, {'rows': 'tr:not(.thead)'})
            for row in rows:
                away = row[3].text == '@'
                if away:
                    continue
                game = {}
                game_link = row[1].find_element_by_tag_name(
                    'a').get_attribute('href')
                if team not in team_links:
                    team_links[team] = re.search(
                        r"[A-Z]{3}", game_link).group()
                game['date'] = row[0].get_attribute('csk')
                game['home_team'] = team
                game['away_team'] = row[4].text
                games.append(game)
        return {'games': games, 'team_links': team_links}

    def get_stats(self):
        pass
