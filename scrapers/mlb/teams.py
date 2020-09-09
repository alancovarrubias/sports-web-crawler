import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr


class MlbTeamsScraper(AbstractScraper):
    def get_resource(self):
        season = self.key_store.args['season']
        endpoint = f'leagues/MLB/{season}.shtml'
        css_selectors = ('#teams_standard_batting',)
        teams_table = self.get_tables(endpoint, css_selectors)[0]
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