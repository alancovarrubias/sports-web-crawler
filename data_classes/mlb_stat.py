import json
import re

PITCHING = 'Pitching'
BATTING = 'Batting'
PLAYER = 'Player'
TEAM = 'Team'


def convert_numeric(text):
    if len(text) == 0:
        return 0
    elif "." in text:
        return float(text)
    else:
        return int(text)


def get_abbr(cell):
    anchor = cell.find_element_by_tag_name('a')
    abbr = re.search(r"[a-z]*\d{2}", anchor.get_attribute('href')).group()
    return abbr


class MlbStat:
    def __init__(self, stat_type, model):
        self.stat_type = stat_type
        self.model = model
        self.stat = {'model_type': model}

    def add_row_data(self, row):
        if self.stat_type == PITCHING:
            self.add_pitching_stat(row)
        elif self.stat_type == BATTING:
            self.add_batting_stat(row)

    def add_batting_stat(self, batting_row):
        text_data = [cell.text for cell in batting_row]
        if self.model == PLAYER:
            self.stat['abbr'] = get_abbr(batting_row[0])
        self.stat['ab'] = convert_numeric(text_data[1])
        self.stat['r'] = convert_numeric(text_data[2])
        self.stat['h'] = convert_numeric(text_data[3])
        self.stat['rbi'] = convert_numeric(text_data[4])
        self.stat['bb'] = convert_numeric(text_data[5])
        self.stat['so'] = convert_numeric(text_data[6])
        self.stat['pa'] = convert_numeric(text_data[7])
        self.stat['ba'] = convert_numeric(text_data[8])
        self.stat['obp'] = convert_numeric(text_data[9])
        self.stat['slg'] = convert_numeric(text_data[10])
        self.stat['ops'] = convert_numeric(text_data[11])

    def add_pitching_stat(self, pitching_row):
        text_data = [cell.text for cell in pitching_row]
        if self.model == PLAYER:
            self.stat['abbr'] = get_abbr(pitching_row[0])
        self.stat['ip'] = convert_numeric(text_data[1])
        self.stat['h'] = convert_numeric(text_data[2])
        self.stat['r'] = convert_numeric(text_data[3])
        self.stat['er'] = convert_numeric(text_data[4])
        self.stat['bb'] = convert_numeric(text_data[5])
        self.stat['so'] = convert_numeric(text_data[6])
        self.stat['hr'] = convert_numeric(text_data[7])
        self.stat['era'] = convert_numeric(text_data[8])

    def toJson(self):
        return self.stat
