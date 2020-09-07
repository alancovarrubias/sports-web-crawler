import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_css_selector(resource, args):
    sport = args['sport']
    team = args['team']
    if sport == 'MLB':
        base_url = 'https://www.baseball-reference.com'
        if resource == 'teams':
            return '#teams_standard_batting',
        elif resource == 'players':
            return '#team_batting'
        elif resource == 'games':
            return '#team_schedule'
        elif resource == 'stats':
            pass
    elif sport == 'NBA':
        base_url = 'https://www.basketball-reference.com'
        if resource == 'teams':
            return '#team_vs_team'
        elif resource == 'players':
            return '#roster'
        elif resource == 'games':
            return '#schedule'
        elif resource == 'stats':
            away_team = args['away_team']
            home_team = args['home_team']
            return [
                f'#box-{away_team}-game-basic',
                f'#box-{away_team}-game-advanced',
                f'#box-{home_team}-game-basic',
                f'#box-{home_team}-game-advanced'
            ]


def resource_url(resource, args):
    sport = args['sport']
    season = args['season']
    team = args['team']
    if sport == 'MLB':
        base_url = 'https://www.baseball-reference.com'
        if resource == 'teams':
            endpoint = f'leagues/MLB/{season}.shtml'
        elif resource == 'players':
            endpoint = f'teams/{team}/{season}.html'
        elif resource == 'games':
            endpoint = f'teams/{team}/{season}-schedule-scores.shtml'
        elif resource == 'stats':
            game_url = args['game_url']
            endpoint = f'boxes/{game_url[0:3]}/{game_url}.html'
    elif sport == 'NBA':
        base_url = 'https://www.basketball-reference.com'
        if resource == 'teams':
            endpoint = f'leagues/NBA_{season}_standings.html'
        elif resource == 'players':
            endpoint = f'teams/{team}/{season}.html'
        elif resource == 'games':
            month = args['month']
            endpoint = f'leagues/NBA_{season}_games-{month}.html'
        elif resource == 'stats':
            game_url = args['game_url']
            endpoint = f'boxscores/{game_url}.html'
    return os.path.join(base_url, endpoint)


class WebDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        options = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(options, options=chrome_options)

    def get(self, resource, args):
        # home_team = args['home_team'].replace(' ', '')
        # away_team = args['away_team'].replace(' ', '')
        url = resource_url(resource, args)
        self.driver.get(url)
        tables = self.get_tables(resource, args)
        return tables

    def get_tables(self, resource, args):
        selectors = get_css_selector(resource, args)
        if isinstance(selectors, list):
            tables = []
            for selector in selectors:
                table = self.get_element(selector)
                tables.append(table)
            return tables
        else:
            return self.get_element(selectors)

    def get_element(self, selector):
        return self.driver.find_element_by_css_selector(selector)
