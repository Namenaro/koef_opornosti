from ECG_getter import get_mini_ECG
from draw_utils import make_arrows
from auto import Auto, Fact
from compromise_set import CompromiseSet
from w_handler import WHandler
from html_logger import HtmlLogger

import statistics
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero


class Prediciton:
    def __init__(self, val, point, b1, b2):
        self.val = val
        self.point = point
        self.b1 = b1
        self.b2 = b2

class Situation:
    def __init__(self):
        self.signal = get_mini_ECG()

        # инициализируем авто-предсказатель
        mean = statistics.mean(self.signal)
        self.auto = Auto(bassin_len=len(self.signal))
        self.auto.set_constant(mean)


    def add_fact(self, point):
        self.auto.add_fact(point, val=self.signal[point])

    def show_prediction_process(self, axs, axs_slayter_ws, ax_win_normed, ax_win_front, d):
        bassin_vals = self.signal[d.b1: d.b2+1]
        global_indexes = list(range(d.b1, d.b2 + 1))
        compromise_set = CompromiseSet(vals=bassin_vals, auto_prediction=self.auto.get_prediction(), point=d.point, val=d.val)
        pareto_points_local = compromise_set.get_pareto_indexes()
        pareto_global = list([local + d.b1 for local in pareto_points_local])
        self._draw_pareto(axs, pareto_global)


        ws = compromise_set.get_slayter_front_ws()
        axs_slayter_ws.set_xticks(range(0, len(self.signal), 5))
        axs_slayter_ws.set_xlim(xmax=len(self.signal), xmin=0)
        axs_slayter_ws.scatter(d.point, 0, color='red')
        self._draw_bassin(axs_slayter_ws, len(self.signal), d.b1, d.b2)
        self._draw_slayter_front_ws(axs_slayter_ws, ws, global_indexes)
        print("W=" + str(compromise_set.get_W()))

        win_normed_list = compromise_set.get_win_normed_list()
        errs_val_normed, errs_auto_normed = compromise_set.get_errs_normed()
        ax_win_normed.set_xticks(range(0, len(self.signal), 5))
        ax_win_normed.set_xlim(xmax=len(self.signal), xmin=0)
        ax_win_normed.scatter(d.point, 0, color='red')
        self._draw_win_normed(ax_win_normed, win_normed_list, errs_val_normed, errs_auto_normed, global_indexes)
        self._draw_bassin(ax_win_normed, len(self.signal), d.b1, d.b2)

        win_normed_front = compromise_set.get_win_compromise_front()
        ax_win_front.set_xticks(range(0, len(self.signal), 5))
        ax_win_front.set_xlim(xmax=len(self.signal), xmin=0)
        ax_win_front.scatter(d.point, 0, color='red')
        self._draw_win_normed_front(ax_win_front, win_normed_front, global_indexes)
        self._draw_bassin(ax_win_front, len(self.signal), d.b1, d.b2)


    def draw_prediction(self, ax, d):
        ax.vlines(x=d.point, ymin=0, ymax=d.val, colors='red', lw=2, label='предсказание')
        self._draw_bassin(ax, len(self.signal), d.b1, d.b2)

    def draw_all_about_auto(self, ax):
        prediction = self.auto.get_prediction()
        ax.plot(prediction, color='green', alpha=0.5, label="авто")
        for fact in self.auto.facts:
            ax.scatter(fact.point, fact.val, color='green')

    def draw_signal(self, ax):
        coords = list(range(0, len(self.signal)))
        ax.bar(coords, self.signal,  color='black', label="сигнал", alpha=0.4)
        ax.set_xticks(range(0, len(self.signal), 5))
        make_arrows(ax)

    #-------------------------------------------------------

    def _draw_bassin(self, ax, bassin_len, b_1, b_2):
        ax.axvspan(0, b_1, facecolor='0.2', alpha=0.5)
        ax.axvspan(b_2, bassin_len, facecolor='0.2', alpha=0.5)

    def _draw_pareto(self, ax, pareto_indexes):
        slayter_vals = list([self.signal[i] for i in pareto_indexes])
        ax.scatter(pareto_indexes, slayter_vals, color='blue', label="парето")

    def _draw_slayter_front_ws(self,ax,ws, global_indexes):
        ax.bar(global_indexes, ws, color='yellow', label="w слейтер фронт", alpha=0.4)
        make_arrows(ax)

    def _draw_win_normed(self, ax, win_normed, errs_val_normed, errs_auto_normed, global_indexes):
        ax.bar(global_indexes, win_normed, color='blue', label="win_normed", alpha=0.4)
        ax.plot(global_indexes,errs_val_normed, label='ошибка нового')
        ax.plot(global_indexes,errs_auto_normed, label='ошибка старого')
        make_arrows(ax)

    def _draw_win_normed_front(self, ax, win_normed_front, global_indexes):
        ax.bar(global_indexes, win_normed_front, color='blue', label="win_normed_front", alpha=0.4)
        make_arrows(ax)

if __name__ == "__main__":
    log = HtmlLogger("VIS_situation")
    situation = Situation()
    fig, axss = plt.subplots(4, sharex=True, figsize=(8, 12), dpi=80)
    axs = axss[0]
    axs_slayter_ws = axss[3]
    ax_win_normed = axss[1]
    ax_win_front = axss[2]

    situation.draw_signal(axs)


    d = Prediciton(val=100, point=20, b1=10, b2=30)
    situation.draw_prediction(axs, d)

    #situation.add_fact(point=25)
    #situation.add_fact(point=40)
    #situation.add_fact(point=21)
    situation.draw_all_about_auto(axs)

    #fig_slayter, axs_slayter = plt.subplots()
    situation.show_prediction_process(axs, axs_slayter_ws, ax_win_normed, ax_win_front, d)


    for ax in axss:
        ax.legend(fancybox=True, framealpha=0.5)

    #log.add_fig(fig)

    plt.show()
