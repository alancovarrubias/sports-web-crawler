import re
from const.mlb import PITCHING, BATTING
from const.models import TEAM, PLAYER
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr
from models.mlb.stat import MlbStat


class MlbStatsScraper(AbstractScraper):
    def get_resource(self):
        game_url = self.key_store.args['game_url']
        away_team = self.key_store.args['away_team'].replace(' ', '')
        home_team = self.key_store.args['home_team'].replace(' ', '')
        endpoint = f'boxes/{game_url[0:3]}/{game_url}.shtml'
        css_selectors = (
            f'#{away_team}batting',
            f'#{away_team}pitching',
            f'#{home_team}batting',
            f'#{home_team}pitching'
        )
        stats_tables = self.get_tables(endpoint, css_selectors)
        away_tables = stats_tables[:2]
        home_tables = stats_tables[2:]

        def get_team_stat(tables):
            batting_table, pitching_table = tables
            css_config = {'section': 'tfoot', 'cells': 'th, td'}
            batting_rows = get_table_rows(batting_table, css_config)
            pitching_rows = get_table_rows(pitching_table, css_config)
            team_pitching_stat = MlbStat(PITCHING, TEAM)
            team_batting_stat = MlbStat(BATTING, TEAM)
            team_batting_stat.add_row_data(batting_rows[0])
            team_pitching_stat.add_row_data(pitching_rows[0])
            return {BATTING: team_batting_stat.toJson(), PITCHING: team_pitching_stat.toJson()}

        def get_player_stats(tables):
            batting_table, pitching_table = tables
            css_config = {'cells': 'th, td'}
            batting_rows = get_table_rows(batting_table, css_config)
            pitching_rows = get_table_rows(pitching_table, css_config)
            pitching_stats = []
            for pitching_row in pitching_rows:
                pitching_stat = MlbStat(PITCHING, PLAYER)
                pitching_stat.add_row_data(pitching_row)
                pitching_stats.append(pitching_stat.toJson())
            batting_stats = []
            for batting_row in batting_rows:
                batting_stat = MlbStat(BATTING, PLAYER)
                batting_stat.add_row_data(batting_row)
                batting_stats.append(batting_stat.toJson())
            return batting_stats

        away_player_stats = get_player_stats(away_tables)
        home_player_stats = get_player_stats(home_tables)
        away_team_stat = get_team_stat(away_tables)
        home_team_stat = get_team_stat(home_tables)
        return {'away_player_stats': away_player_stats, 'home_player_stats': home_player_stats, 'away_team_stat': away_team_stat, 'home_team_stat': home_team_stat}