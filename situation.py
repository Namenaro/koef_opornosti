from ECG_getter import get_mini_ECG
from draw_utils import make_arrows

import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero

class Situation:
    def __init__(self):
        self.signal = get_mini_ECG()


    def add_fact(self, point):
        pass

    def make_prediction(self, val, point, b1, b2):
        pass


    def draw_all_about_prediction(self, ax, val, point, b1, b2):
        ax.vlines(x=point, ymin=0, ymax=val, colors='orange', lw=2, label='предсказание')
        self._draw_bassin(ax, len(self.signal), b1, b2)

    def draw_all_about_auto(self, axs):
        pass

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

    axs.legend(fancybox=True, framealpha=0.5)
    plt.show()