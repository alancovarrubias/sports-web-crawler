from operator import methodcaller
import re
from .abstract import AbstractScraper
from .helpers import get_table_rows, get_team_abbr
from data_classes.mlb_stat import MlbStat

PITCHING = 'Pitching'
BATTING = 'Batting'
PLAYER = 'Player'
TEAM = 'Team'


class MlbScraper(AbstractScraper):
    def get_teams(self, args):
        teams_table = self.get('teams', args)

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
        players_table = self.get('players', args)

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
        teams = args['teams'].split(',')
        games = []
        team_links = {}
        for team in teams:
            args['team'] = team
            games_table = self.get('games', args)
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

    def get_stats(self, args):
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
