from w_handler import WHandler

def v1_better_val2(val1, val2):
    if val1> val2:
        return True
    return False

class CompromiseSet:
    def __init__(self, vals, auto_prediction, point, val):
        self.indexes_pareto = None
        self.slayter_front_ws = None

        self.point=point


        self.w_handler = WHandler(vals, auto_prediction, point, val)
        self._init()


    def get_W(self):
        return sum(self.slayter_front_ws)

    def _init(self):
        self.indexes_pareto = [self.point]
        win_normed_list = self.w_handler.get_win_normed_list()

        # перебираем левее начиная с ближайших индексов
        etalon = win_normed_list[self.point]
        i = self.point
        lefts_slayter_wins = []

        current_best = etalon
        while True:
            new_index_in_arr = i - 1
            if new_index_in_arr < 0:
                break
            new_value = win_normed_list[new_index_in_arr]
            if v1_better_val2(new_value, current_best):
                current_best = new_value
                self.indexes_pareto.append(new_index_in_arr)
            lefts_slayter_wins.append(current_best)
            i = new_index_in_arr
        lefts_slayter_wins = list(reversed(lefts_slayter_wins))

        # перебираем правее начиная с ближайших индексов
        i = self.point
        rights_slayter_wins = []
        current_best = etalon
        while True:
            new_index_in_arr = i + 1
            if new_index_in_arr == len(win_normed_list):
                break
            new_value = win_normed_list[new_index_in_arr]
            if v1_better_val2(new_value, current_best):
                current_best = new_value
                self.indexes_pareto.append(new_index_in_arr)
            rights_slayter_wins.append(current_best)
            i = new_index_in_arr

        self.slayter_front_ws = lefts_slayter_wins + [etalon] + rights_slayter_wins
