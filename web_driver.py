import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_css_selectors(resource_type, args):
    sport = args['sport']
    if sport == 'MLB':
        if resource_type == 'teams':
            return ('#teams_standard_batting')
        elif resource_type == 'players':
            return ('#team_batting')
        elif resource_type == 'games':
            return ('#team_schedule')
        elif resource_type == 'stats':
            away_team = args['away_team'].replace(' ', '')
            home_team = args['home_team'].replace(' ', '')
            return (
                f'#{away_team}batting',
                f'#{away_team}pitching',
                f'#{home_team}batting',
                f'#{home_team}pitching'
            )
    elif sport == 'NBA':
        if resource_type == 'teams':
            return ('#team_vs_team')
        elif resource_type == 'players':
            return ('#roster')
        elif resource_type == 'games':
            return ('#schedule')
        elif resource_type == 'stats':
            away_team = args['away_team']
            home_team = args['home_team']
            return (
                f'#box-{away_team}-game-basic',
                f'#box-{away_team}-game-advanced',
                f'#box-{home_team}-game-basic',
                f'#box-{home_team}-game-advanced'
            )


def resource_url(resource_type, args):
    sport = args['sport']
    season = args['season']
    team = args['team']
    endpoint = ''
    if sport == 'MLB':
        base_url = 'https://www.baseball-reference.com'
        if resource_type == 'teams':
            endpoint = f'leagues/MLB/{season}.shtml'
        elif resource_type == 'players':
            endpoint = f'teams/{team}/{season}.html'
        elif resource_type == 'games':
            endpoint = f'teams/{team}/{season}-schedule-scores.shtml'
        elif resource_type == 'stats':
            game_url = args['game_url']
            endpoint = f'boxes/{game_url[0:3]}/{game_url}.shtml'
    elif sport == 'NBA':
        base_url = 'https://www.basketball-reference.com'
        if resource_type == 'teams':
            endpoint = f'leagues/NBA_{season}_standings.html'
        elif resource_type == 'players':
            endpoint = f'teams/{team}/{season}.html'
        elif resource_type == 'games':
            month = args['month']
            endpoint = f'leagues/NBA_{season}_games-{month}.html'
        elif resource_type == 'stats':
            game_url = args['game_url']
            endpoint = f'boxscores/{game_url}.html'
    return os.path.join(base_url, endpoint)


class WebDriver:
    def __init__(self, resource_type, args):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        options = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(options, options=chrome_options)
        self.resource_type = resource_type
        self.url = resource_url(resource_type, args)

    def get(self):
        self.driver.get(self.url)
        return self.driver.page_source

    def get_element(self, selector):
        return self.driver.find_element_by_css_selector(selector)
