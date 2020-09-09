import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr


class NbaTeamsScraper(AbstractScraper):
    def get_resource(self):
        args = []
        teams_table = self.get('teams', args)
        table_rows = get_table_rows(teams_table)

        def get_team(row):
            team = {}
            team_text = row[0].text
            words = team_text.split()
            team['abbr'] = get_team_abbr(row[0])
            if re.search("Blazers", team_text):
                team['name'] = ' '.join(words[1:])
                team['city'] = ' '.join(words[:1])
            else:
                team['name'] = ' '.join(words[-1:])
                team['city'] = ' '.join(words[:-1])
            return team

        teams = [get_team(row) for row in table_rows]
        return {'teams': teams}
