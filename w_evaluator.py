import statistics

from  distr import Distr, get_distr_of_max_statistics

class WEvaluatorForIndex:
    def __init__(self, vals, auto_prediction, point, val):
        self.vals = vals
        self.auto_prediction = auto_prediction
        self.point = point
        self.val = val

        self.win_normed_list = None
        self.win_normed_distr = None
        self.mean_abs_win_normed = None

        self._init_win_info()

    def _init_win_info(self):
        divider = sum(self.vals)
        errs_val_normed = list([abs(self.vals[i] - self.val) / divider for i in range(len(self.vals))])
        errs_auto_normed = list([abs(self.vals[i] - self.auto_prediction[i]) / divider for i in range(len(self.vals))])

        win_normed_list = []
        for i in range(len(errs_auto_normed)):
            abs_w_normed = abs(errs_val_normed[i] - errs_auto_normed[i])
            if errs_auto_normed[i]<errs_val_normed[i]: # старое лучше, чем новое
                win_normed_list.append(-abs_w_normed)
            else:
                win_normed_list.append(abs_w_normed)

        self.win_normed_list = win_normed_list
        self.win_normed_distr = Distr(win_normed_list)

        self.mean_abs_win_normed = statistics.mean(list([abs(normed_win) for normed_win in self.win_normed_list]))


    def get_w_for_index(self, global_index):
        du_in_index = abs(global_index - self.point)
        win_normed_in_index = self.win_normed_list[global_index]

        statistic_distr = get_distr_of_max_statistics(self.win_normed_distr, len_subsample=du_in_index+1)

        w_unnormed = 0
        if win_normed_in_index > 0:
            w_unnormed += 1 - statistic_distr.get_p_of_event(win_normed_in_index, statistic_distr.get_max_x())

        if win_normed_in_index < 0:
            p = statistic_distr.get_p_of_event(win_normed_in_index, statistic_distr.get_max_x())
            w_unnormed -= p

        scale_koeff_for_w = self.mean_abs_win_normed
        w = w_unnormed * scale_koeff_for_w
        return w


if __name__ == "__main__":
    vals = [9, 3,3,3,3,3]
    auto_prediction = [3]*len(vals)
    point=0
    val=9.1

    eval = WEvaluatorForIndex(vals, auto_prediction, point, val)

    w_arr = []
    for index in range(len(vals)):
        w_arr.append(eval.get_w_for_index(index))

    print(w_arr)









