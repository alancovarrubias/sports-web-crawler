from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from operator import methodcaller
import os
import re


class Scraper:
	def __init__(self):
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		options = ChromeDriverManager().install()
		self.driver = webdriver.Chrome(options, options=chrome_options)

	def get(self, endpoint):
		url = os.path.join('https://www.basketball-reference.com', endpoint)
		self.driver.get(url)

	def get_teams(self, season):
		self.get(f'leagues/NBA_{season}_standings.html')
		teams_table = self.driver.find_element_by_id(
			'team_vs_team').find_element_by_tag_name('tbody')

		rows = teams_table.find_elements_by_tag_name('tr')
		cell_rows = [row.find_elements_by_tag_name('td') for row in rows]
		cell_rows = [row for row in cell_rows if row]

		def get_team(row):
			team = {}
			text_array = row[0].text.split()
			if text_array[-1] == "Blazers":
				team['name'] = ' '.join(text_array[1:])
				team['city'] = text_array[0]
			else:
				team['name'] = text_array[-1]
				team['city'] = ' '.join(text_array[:-1])
			team['abbr'] = self.__get_team_abbr(row[0])
			return team
		return [get_team(row) for row in cell_rows]

	def get_players(self, season, team):
		self.get(f'teams/{team}/{season}.html')
		players_table = self.driver.find_element_by_id(
			'roster').find_element_by_tag_name('tbody')
		rows = players_table.find_elements_by_tag_name('tr')

		def get_player(row):
			cells = row.find_elements_by_tag_name('td')
			player = {}
			player['name'] = cells[0].text
			player['abbr'] = cells[0].get_attribute('data-append-csv')
			player['position'] = cells[1].text
			return player

		return [get_player(row) for row in rows]

	def get_games(self, season):
		months = (
			{'text': 'October', 'numeric': 10}, {'text': 'November', 'numeric': 11},
			{'text': 'December', 'numeric': 12}, {'text':'January', 'numeric': 1},
			{ 'text': 'February', 'numeric': 2}, {'text': 'March', 'numeric': 3},
			{'text': 'April', 'numeric': 4}, {'text': 'May', 'numeric': 5},
			{'text':'June', 'numeric': 6}
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
				game['away_team'] = self.__get_team_abbr(cells[1])
				game['home_team'] = self.__get_team_abbr(cells[3])
				return game

			month_games = [get_game(row) for row in rows]
			games += month_games

		return games
	
	def get_stats(self, game_url, home_team, away_team):
		self.get(f'boxscores/{game_url}.html')
		def get_team_stats(team):
			team_stats = {}
			basic_stats_table = self.driver.find_element_by_id(f'box-{team}-game-basic')
			advanced_stats_table = self.driver.find_element_by_id(f'box-{team}-game-advanced')
			basic_rows = basic_stats_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			advanced_rows = advanced_stats_table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
			for row in basic_rows:
				cells = row.find_elements_by_tag_name('td')
				if len(cells) <= 1:
					continue
				player = row.find_element_by_tag_name('th').get_attribute('data-append-csv')
				data = [cell.text for cell in cells]
				team_stat = {}
				team_stat['player'] = player
				team_stat['team'] = team
				mp = data[0].split(':')
				team_stat['sp'] = int(mp[0])*60 + int(mp[1])
				team_stat['fg'] = int(data[1])
				team_stat['fga'] = int(data[2])
				team_stat['fg3'] = int(data[4])
				team_stat['fg3a'] = int(data[5])
				team_stat['ft'] = int(data[7])
				team_stat['fta'] = int(data[8])
				team_stat['orb'] = int(data[10])
				team_stat['drb'] = int(data[11])
				team_stat['ast'] = int(data[13])
				team_stat['stl'] = int(data[14])
				team_stat['blk'] = int(data[15])
				team_stat['tov'] = int(data[16])
				team_stat['pf'] = int(data[17])
				team_stat['pts'] = int(data[18])
				team_stats[player] = team_stat
			for row in advanced_rows:
				cells = row.find_elements_by_tag_name('td')
				if len(cells) <= 1:
					continue
				player = row.find_element_by_tag_name('th').get_attribute('data-append-csv')
				data = [cell.text for cell in cells]
				team_stats[player]['ortg'] = data[13]
				team_stats[player]['drtg'] = data[14]
			return list(team_stats.values())
		home_team_stats = get_team_stats(home_team)
		away_team_stats = get_team_stats(home_team)
		return home_team_stats + away_team_stats

	def __get_team_abbr(self, cell): return cell.find_element_by_tag_name(
		'a').get_attribute('href').split('/')[-2]
