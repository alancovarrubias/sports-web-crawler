from models.abstract import AbstractModel
from const.models import PLAYER

def get_sp(data):
    mp = data.split(':')
    return int(mp[0])*60 if (len(mp) == 1) else int(mp[0])*60 + int(mp[1])

def type_rtg(rtg, model_type):
    return int(rtg) if model_type == PLAYER else float(rtg)

class NbaStat(AbstractModel):
    def __init__(self, model_type, row, advanced_row):
        if model_type == PLAYER:
            self.abbr = row[0].get_attribute('data-append-csv')
        self.model_type = model_type
        advanced_row_text = [cell.text for cell in advanced_row]
        self.ortg = type_rtg(advanced_row_text[14], model_type)
        self.drtg = type_rtg(advanced_row_text[15], model_type)
        super().__init__(row)

    def build(self, row):
        row_text = [cell.text for cell in row]
        self.sp = get_sp(row_text[1])
        self.fg = int(row_text[2])
        self.fga = int(row_text[3])
        self.fg3 = int(row_text[5])
        self.fg3a = int(row_text[6])
        self.ft = int(row_text[8])
        self.fta = int(row_text[9])
        self.orb = int(row_text[11])
        self.drb = int(row_text[12])
        self.ast = int(row_text[14])
        self.stl = int(row_text[15])
        self.blk = int(row_text[16])
        self.tov = int(row_text[17])
        self.pf = int(row_text[18])
        self.pts = int(row_text[19])
