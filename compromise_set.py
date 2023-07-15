from w_handler import WHandler

def v1_better_than_val2(val1, val2):
    if val1 > val2:
        return True
    return False

class CompromiseSet:
    def __init__(self, vals, auto_prediction, point, val):
        self.indexes_pareto = None
        self.slayter_front_ws = None
        self.slayter_compromise_front_win = None


        self.point=point

        self.w_handler = WHandler(vals, auto_prediction, point, val)
        self._init()


    def get_W(self):
        return sum(self.slayter_front_ws)

    def get_pareto_indexes(self):
        return self.indexes_pareto

    def get_slayter_front_ws(self):
        return self.slayter_front_ws

    def get_win_normed_list(self):
        return self.w_handler.get_win_normed_list()

    def get_errs_normed(self):
        return self.w_handler.get_errs_normed()

    def get_win_compromise_front(self):
        return self.slayter_compromise_front_win

    def _init(self):
        self.indexes_pareto = [self.point]
        win_normed_list = self.w_handler.get_win_normed_list()

        # перебираем левее начиная с ближайших индексов
        etalon_win = win_normed_list[self.point]
        i = self.point
        lefts_slayter_wins = []

        current_best = etalon_win
        while True:
            new_index_in_arr = i - 1
            if new_index_in_arr < 0:
                break
            new_value = win_normed_list[new_index_in_arr]
            if v1_better_than_val2(new_value, current_best):
                current_best = new_value
                self.indexes_pareto.append(new_index_in_arr)
            lefts_slayter_wins.append(current_best)
            i = new_index_in_arr
        lefts_slayter_wins = list(reversed(lefts_slayter_wins))

        # перебираем правее начиная с ближайших индексов
        i = self.point
        rights_slayter_wins = []
        current_best = etalon_win
        while True:
            new_index_in_arr = i + 1
            if new_index_in_arr == len(win_normed_list):
                break
            new_value = win_normed_list[new_index_in_arr]
            if v1_better_than_val2(new_value, current_best):
                current_best = new_value
                self.indexes_pareto.append(new_index_in_arr)
            rights_slayter_wins.append(current_best)
            i = new_index_in_arr

        self.slayter_compromise_front_win = lefts_slayter_wins + [etalon_win] + rights_slayter_wins
        self.slayter_front_ws = self.w_handler.get_all_ws(self.slayter_compromise_front_win)

