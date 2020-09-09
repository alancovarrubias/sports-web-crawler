import json


def get_sp(data):
    mp = data.split(":")
    return int(mp[0])*60 if (len(mp) == 1) else int(mp[0])*60 + int(mp[1])


def type_rtg(rtg, model):
    return int(rtg) if model == 'Player' else float(rtg)


class NbaStat:
    def __init__(self, model):
        self.model = model
        self.stat = {'model_type': model}

    def add_row_data(self, basic_row, advanced_row):
        if self.model == 'Player':
            self.stat['abbr'] = basic_row[0].get_attribute('data-append-csv')
        basic_data = [cell.text for cell in basic_row]
        advanced_data = [cell.text for cell in advanced_row]
        self.stat['sp'] = get_sp(basic_data[1])
        self.stat['fg'] = int(basic_data[2])
        self.stat['fga'] = int(basic_data[3])
        self.stat['fg3'] = int(basic_data[5])
        self.stat['fg3a'] = int(basic_data[6])
        self.stat['ft'] = int(basic_data[8])
        self.stat['fta'] = int(basic_data[9])
        self.stat['orb'] = int(basic_data[11])
        self.stat['drb'] = int(basic_data[12])
        self.stat['ast'] = int(basic_data[14])
        self.stat['stl'] = int(basic_data[15])
        self.stat['blk'] = int(basic_data[16])
        self.stat['tov'] = int(basic_data[17])
        self.stat['pf'] = int(basic_data[18])
        self.stat['pts'] = int(basic_data[19])
        self.stat['ortg'] = type_rtg(advanced_data[14], self.model)
        self.stat['drtg'] = type_rtg(advanced_data[15], self.model)

    def toJson(self):
        return self.stat
