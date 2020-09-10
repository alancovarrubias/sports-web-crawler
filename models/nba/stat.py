import json
from const.models import PLAYER


def get_sp(data):
    mp = data.split(':')
    return int(mp[0])*60 if (len(mp) == 1) else int(mp[0])*60 + int(mp[1])


def type_rtg(rtg, model):
    return int(rtg) if model == PLAYER else float(rtg)


class NbaStat:
    def __init__(self, model, basic_row, advanced_row):
        self.model = model
        self.stat = self.build_stat(basic_row, advanced_row)

    def build_stat(self, basic_row, advanced_row):
        stat = {}
        if self.model == PLAYER:
            stat['abbr'] = basic_row[0].get_attribute('data-append-csv')

        basic_data = [cell.text for cell in basic_row]
        stat['sp'] = get_sp(basic_data[1])
        stat['fg'] = int(basic_data[2])
        stat['fga'] = int(basic_data[3])
        stat['fg3'] = int(basic_data[5])
        stat['fg3a'] = int(basic_data[6])
        stat['ft'] = int(basic_data[8])
        stat['fta'] = int(basic_data[9])
        stat['orb'] = int(basic_data[11])
        stat['drb'] = int(basic_data[12])
        stat['ast'] = int(basic_data[14])
        stat['stl'] = int(basic_data[15])
        stat['blk'] = int(basic_data[16])
        stat['tov'] = int(basic_data[17])
        stat['pf'] = int(basic_data[18])
        stat['pts'] = int(basic_data[19])

        advanced_data = [cell.text for cell in advanced_row]
        stat['ortg'] = type_rtg(advanced_data[14], self.model)
        stat['drtg'] = type_rtg(advanced_data[15], self.model)
        return stat

    def toJson(self):
        return self.stat
