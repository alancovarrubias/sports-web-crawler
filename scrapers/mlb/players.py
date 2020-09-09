import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr


class MlbPlayersScraper(AbstractScraper):
    def get_resource(self):
        season = self.args['season']
        team = self.args['team']
        endpoint = f'teams/{team}/{season}.html'
        css_selectors = ('#team_batting',)
        players_table = self.get_tables(endpoint, css_selectors)[0]

        table_rows = get_table_rows(players_table)

        def get_player(row):
            player = {}
            player['name'] = row[1].find_element_by_tag_name('a').text
            player['abbr'] = row[1].get_attribute('data-append-csv')
            player['position'] = row[0].text
            return player

        players = [get_player(row) for row in table_rows]
        return {'players': players}