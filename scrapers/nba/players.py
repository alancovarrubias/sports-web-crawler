import re
from scrapers.helpers import get_table_rows, get_team_abbr
from scrapers.abstract import AbstractScraper


class NbaPlayersScraper(AbstractScraper):
    def get_resource(self):
        season = self.args['season']
        team = self.args['team']
        endpoint = f'teams/{team}/{season}.html'
        css_selectors = ('#roster',)
        players_table = self.get_tables(endpoint, css_selectors)[0]
        table_rows = get_table_rows(players_table)

        def get_player(row):
            anchor = row[0].find_element_by_tag_name('a')
            link = anchor.get_attribute('href')
            player = {}
            player['name'] = anchor.text
            player['abbr'] = re.search(r"\w*\d{2}", link).group()
            player['position'] = row[1].text
            return player

        players = [get_player(row) for row in table_rows]
        return {'players': players}
