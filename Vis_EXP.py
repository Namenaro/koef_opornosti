import statistics

from auto import Auto, Fact
from w_handler import WHandler
from compromise_set import CompromiseSet


def t1():
    print("")
    print('\033[95m' + "===================================================")
    print("                1.Идеально хорошая, идеально плохая точки:    " + '\033[0m')
    vals = [9, 3, 3, 3, 3, 3,3]
    mean = statistics.mean(vals)
    auto = Auto(bassin_len=len(vals))
    auto.set_constant(mean)


    good_point = 0
    vis_koef_calc(vals, good_point, auto)

    bad_point = 4
    vis_koef_calc(vals, bad_point, auto)

def vis_koef_calc(vals, point, auto):
    auto_prediction = auto.get_prediction_without_facts()

    compromise_set = CompromiseSet(vals, auto_prediction, point, val=vals[point])
    print("W прямого попадания = " + str(compromise_set.get_W()))



if __name__ == '__main__':
    t1()
