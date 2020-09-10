import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr
from operator import methodcaller


class MlbGamesScraper(AbstractScraper):
    def get_resource(self):
        games = []
        team_links = {}
        season = self.key_store.args['season']
        teams = self.key_store.args['teams'].split(',')
        for team in teams:
            endpoint = f'teams/{team}/{season}-schedule-scores.shtml'
            css_selectors = ('#team_schedule',)
            games_table = self.get_tables(endpoint, css_selectors)[0]
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