import re
from scrapers.abstract import AbstractScraper
from scrapers.helpers import get_table_rows, get_team_abbr
from models.nba_stat import NbaStat


class NbaStatsScraper(AbstractScraper):
    def get_resource(self):
        away_team = self.key_store.args['away_team']
        home_team = self.key_store.args['home_team']
        game_url = self.key_store.args['game_url']
        endpoint = f'boxscores/{game_url}.html'
        css_selectors = (
            f'#box-{away_team}-game-basic',
            f'#box-{away_team}-game-advanced',
            f'#box-{home_team}-game-basic',
            f'#box-{home_team}-game-advanced'
        )
        stat_tables = self.get_tables(endpoint, css_selectors)
        away_tables = stat_tables[:2]
        home_tables = stat_tables[2:]

        def get_team_stat(tables):
            basic_stats_table, advanced_stats_table = tables
            css_config = {'section': 'tfoot', 'cells': 'th, td'}
            basic_rows = get_table_rows(basic_stats_table, css_config)
            advanced_rows = get_table_rows(advanced_stats_table, css_config)
            team_stat = NbaStat('Team')
            team_stat.add_row_data(basic_rows[0], advanced_rows[0])
            return team_stat.toJson()

        def get_player_stats(tables):
            basic_stats_table, advanced_stats_table = tables
            css_config = {'rows': 'tr:not(.thead)', 'cells': 'th, td'}
            basic_rows = get_table_rows(basic_stats_table, css_config)
            advanced_rows = get_table_rows(advanced_stats_table, css_config)
            player_stats = []
            for basic_row, advanced_row in zip(basic_rows, advanced_rows):
                if len(basic_row) <= 2:
                    continue
                player_stat = NbaStat('Player')
                player_stat.add_row_data(basic_row, advanced_row)
                player_stats.append(player_stat.toJson())
            return player_stats

        away_player_stats = get_player_stats(away_tables)
        home_player_stats = get_player_stats(home_tables)
        away_team_stat = get_team_stat(away_tables)
        home_team_stat = get_team_stat(home_tables)
        return {'away_player_stats': away_player_stats, 'home_player_stats': home_player_stats, 'away_team_stat': away_team_stat, 'home_team_stat': home_team_stat}