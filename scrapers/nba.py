from operator import methodcaller
import re
from .abstract import AbstractScraper
from .helpers import get_table_rows, get_team_abbr


class NbaScraper(AbstractScraper):
    def __init__(self):
        base_url = 'https://www.basketball-reference.com'
        super().__init__(base_url)

    def get_teams(self, args):
        season = args['season']
        self.get(f'leagues/NBA_{season}_standings.html')
        teams_table = self.driver.find_element_by_id(
            'team_vs_team')
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
        return [get_team(row) for row in table_rows]

    def get_players(self, args):
        season = args['season']
        team = args['team']
        self.get(f'teams/{team}/{season}.html')
        players_table = self.driver.find_element_by_id(
            'roster')
        table_rows = get_table_rows(players_table)

        def get_player(row):
            anchor = row[0].find_element_by_tag_name('a')
            link = anchor.get_attribute('href')
            player = {}
            player['name'] = anchor.text
            player['abbr'] = re.search("\w*\d{2}", link).group()
            player['position'] = row[1].text
            return player

        return [get_player(row) for row in table_rows]

    def get_games(self, args):
        season = args['season']
        months = (
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

        games = []
        for month in months:
            lowercased = month['text'].lower()
            self.get(f'leagues/NBA_{season}_games-{lowercased}.html')
            games_table = self.driver.find_element_by_id(
                'schedule').find_element_by_tag_name('tbody')
            rows = games_table.find_elements_by_css_selector(
                'tr:not(.thead)')

            def get_game(row):
                date = row.find_element_by_tag_name('th').text
                date_array = list(map(methodcaller('strip'), date.split(',')))
                cells = row.find_elements_by_tag_name('td')
                game = {}
                game['year'] = int(date_array[-1])
                game['month'] = month['numeric']
                game['day'] = int(date_array[1].split()[-1])
                game['away_team'] = get_team_abbr(cells[1])
                game['home_team'] = get_team_abbr(cells[3])
                return game

            month_games = [get_game(row) for row in rows]
            games += month_games

        return games

    def get_stats(self, args):
        game_url = args['game_url']
        home_team = args['home_team']
        away_team = args['away_team']
        self.get(f'boxscores/{game_url}.html')

        def add_advanced_stat(row, stat):
            cells = row.find_elements_by_tag_name('td')
            data = [cell.text for cell in cells]
            stat['ortg'] = data[13]
            stat['drtg'] = data[14]

        def build_basic_stat(row):
            stat = {}
            cells = row.find_elements_by_tag_name('td')
            data = [cell.text for cell in cells]
            mp = data[0].split(':')
            if (len(mp) == 1):
                stat['sp'] = int(mp[0])*60
            else:
                stat['sp'] = int(mp[0])*60 + int(mp[1])
            stat['fg'] = int(data[1])
            stat['fga'] = int(data[2])
            stat['fg3'] = int(data[4])
            stat['fg3a'] = int(data[5])
            stat['ft'] = int(data[7])
            stat['fta'] = int(data[8])
            stat['orb'] = int(data[10])
            stat['drb'] = int(data[11])
            stat['ast'] = int(data[13])
            stat['stl'] = int(data[14])
            stat['blk'] = int(data[15])
            stat['tov'] = int(data[16])
            stat['pf'] = int(data[17])
            stat['pts'] = int(data[18])
            return stat

        def get_team_stat(team):
            basic_stats_table = self.driver.find_element_by_id(
                f'box-{team}-game-basic')
            advanced_stats_table = self.driver.find_element_by_id(
                f'box-{team}-game-advanced')
            basic_team_row = basic_stats_table.find_element_by_tag_name(
                'tfoot').find_element_by_tag_name('tr')
            advanced_team_row = advanced_stats_table.find_element_by_tag_name(
                'tfoot').find_element_by_tag_name('tr')
            team_stat = build_basic_stat(basic_team_row)
            add_advanced_stat(advanced_team_row, team_stat)
            team_stat['model_type'] = 'Team'
            team_stat['abbr'] = team
            return team_stat

        def get_player_stats(team):
            player_stats = {}
            basic_stats_table = self.driver.find_element_by_id(
                f'box-{team}-game-basic')
            advanced_stats_table = self.driver.find_element_by_id(
                f'box-{team}-game-advanced')
            basic_rows = basic_stats_table.find_element_by_tag_name(
                'tbody').find_elements_by_tag_name('tr')
            advanced_rows = advanced_stats_table.find_element_by_tag_name(
                'tbody').find_elements_by_tag_name('tr')
            for row in basic_rows:
                cells = row.find_elements_by_tag_name('td')
                if len(cells) <= 1:
                    continue
                player = row.find_element_by_tag_name(
                    'th').get_attribute('data-append-csv')
                player_stat = build_basic_stat(row)
                player_stat['model_type'] = 'Player'
                player_stat['abbr'] = player
                player_stat['team'] = team
                player_stats[player] = player_stat
            for row in advanced_rows:
                cells = row.find_elements_by_tag_name('td')
                if len(cells) <= 1:
                    continue
                player = row.find_element_by_tag_name(
                    'th').get_attribute('data-append-csv')
                add_advanced_stat(row, player_stats[player])
            return list(player_stats.values())
        away_player_stats = get_player_stats(away_team)
        home_player_stats = get_player_stats(home_team)
        stats = away_player_stats + home_player_stats
        away_team_stat = get_team_stat(away_team)
        home_team_stat = get_team_stat(home_team)
        stats.append(away_team_stat)
        stats.append(home_team_stat)
        return stats
