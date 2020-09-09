import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr
from constant import PITCHING, BATTING, TEAM, PLAYER
from data_classes.mlb_stat import MlbStat


class MlbStatsScraper(AbstractScraper):
    def get_resource(self):
        args = []
        tables = self.get('stats', args)
        away_tables = tables[:2]
        home_tables = tables[2:]

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