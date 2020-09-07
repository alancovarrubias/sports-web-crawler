from operator import methodcaller
import re
from .abstract import AbstractScraper
from .helpers import get_table_rows, get_team_abbr
from data_classes.nba_stat import NbaStat

MONTHS = (
    {'text': 'October', 'numeric': 10},
    {'text': 'November', 'numeric': 11},
    {'text': 'December', 'numeric': 12},
    {'text': 'January', 'numeric': 1},
    {'text': 'February', 'numeric': 2},
    {'text': 'March', 'numeric': 3},
    {'text': 'April', 'numeric': 4},
    {'text': 'May', 'numeric': 5},
    {'text': 'June', 'numeric': 6}
)


class NbaScraper(AbstractScraper):
    def get_teams(self, args):
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

    def get_players(self, args):
        players_table = self.get('players', args)
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

    def get_games(self, args):
        season = args['season']

        games = []
        for month in MONTHS:
            args['month'] = month['text'].lower()
            games_table = self.get('games', args)
            css_config = {'rows': 'tr:not(.thead)', 'cells': 'th, td'}
            table_rows = get_table_rows(games_table, css_config)

            def get_game(row):
                date = row[0].text
                date_array = list(map(methodcaller('strip'), date.split(',')))
                game = {}
                game['year'] = int(date_array[-1])
                game['month'] = month['numeric']
                game['day'] = int(date_array[1].split()[-1])
                game['away_team'] = get_team_abbr(row[2])
                game['home_team'] = get_team_abbr(row[4])
                return game

            month_games = [get_game(row) for row in table_rows]
            games += month_games

        return {'games': games}

    def get_stats(self, args):
        stat_tables = self.get('stats', args)
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
