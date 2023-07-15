from ECG_getter import get_mini_ECG
from draw_utils import make_arrows
import statistics

from auto import Auto, Fact
from w_handler import WHandler

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

    def make_prediction(self, d):
        pass


    def draw_all_about_prediction(self, ax, d):
        ax.vlines(x=d.point, ymin=0, ymax=d.val, colors='red', lw=2, label='предсказание')
        self._draw_bassin(ax, len(self.signal), d.b1, d.b2)

    def draw_all_about_auto(self, ax):
        prediction = self.auto.get_prediction()
        ax.plot(prediction, color='green', alpha=0.5, label="авто")
        for fact in self.auto.facts:
            ax.scatter(fact.point, fact.val, color='green')

    def draw_signal(self, ax):
        ax.plot(self.signal, color='black', label="сигнал")
        ax.set_xticks(range(0, len(self.signal), 5))
        make_arrows(ax)

    #-------------------------------------------------------

    def _draw_bassin(self, ax, bassin_len, b_1, b_2):
        ax.axvspan(0, b_1, facecolor='0.2', alpha=0.5)
        ax.axvspan(b_2, bassin_len, facecolor='0.2', alpha=0.5)



if __name__ == "__main__":
    situation = Situation()
    fig, axs = plt.subplots()
    situation.draw_signal(axs)


    d = Prediciton(val=40, point=20, b1=10, b2=30)
    situation.draw_all_about_prediction(axs, d)

    situation.add_fact(point=25)
    situation.add_fact(point=40)
    situation.add_fact(point=21)
    situation.draw_all_about_auto(axs)





    axs.legend(fancybox=True, framealpha=0.5)
    plt.show()