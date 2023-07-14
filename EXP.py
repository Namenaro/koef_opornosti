import statistics
from auto import Auto, Fact

def t1():
    print("")
    print('\033[95m' + "===================================================")
    print("                1.Идеально хорошая, идеально плохая точки:    " + '\033[0m')
    vals_ = [9, 3, 3, 3, 3, 3,3]
    good_point = 0
    bad_point = 4
    vis_koef_calc(vals_, good_point)

def vis_koef_calc(vals, point):
    mean = statistics.mean(vals)
    auto = Auto(bassin_len=len(vals))
    auto.set_constant(mean)
    auto_prediction = auto.get_prediction_without_facts()
    


if __name__ == '__main__':