import json

PITCHING = 'Pitching'
BATTING = 'Batting'
PLAYER = 'Player'
TEAM = 'Team'


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
        self.stat['fg'] = int(text_data[2])
        self.stat['fga'] = int(text_data[3])

    def add_pitching_stat(self, pitching_row):
        text_data = [cell.text for cell in pitching_row]
        self.stat['fg'] = int(text_data[2])
        self.stat['fga'] = int(text_data[3])
        self.stat['fg3'] = int(text_data[5])
        self.stat['fg3a'] = int(text_data[6])
        self.stat['ft'] = int(text_data[8])
        self.stat['fta'] = int(text_data[9])
        self.stat['orb'] = int(text_data[11])
        self.stat['drb'] = int(text_data[12])
        self.stat['ast'] = int(text_data[14])
        self.stat['stl'] = int(text_data[15])
        self.stat['blk'] = int(text_data[16])
        self.stat['tov'] = int(text_data[17])
        self.stat['pf'] = int(text_data[18])
        self.stat['pts'] = int(text_data[19])

    def toJson(self):
        return self.stat
