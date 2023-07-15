import statistics
import math
import matplotlib.pyplot as plt

# сюда добавлются известные факты о значениях переменной в разных точках
# возвращается поточечное предсказание в тех же единицах измерения, что и vals (без нормаировки)

class Fact:
    def __init__(self,val ,point):
        self.val = val
        self.point = point



class Auto:
    def __init__(self, bassin_len):
        self.bassin_len = bassin_len  # длина итогового предсказания будет такая, индексы идут с нуля

        self.facts = []

        self.constant = None

    def add_fact(self, point, val):
        self.constant = None
        fact = Fact(val, point=point)
        self.facts.append(fact)
        self.facts.sort(key=lambda f: f.point)


    def set_constant(self, constant):
        self.constant = constant
        self.facts = []

    def get_prediction(self):
        if self.constant is not None:
            return [self.constant] * self.bassin_len
        return self.get_prediction_by_facts_interpolation()

    def get_prediction_by_facts_interpolation(self):
        result = []
        if self.facts[0].point != 0:
            dist_to_left = self.facts[0].point
            result += [self.facts[0].val] * dist_to_left

        for i in range(len(self.facts)-1):
            val_current = self.facts[i].val
            point_current = self.facts[i].point

            val_next = self.facts[i+1].val
            point_next = self.facts[i+1].point

            vals_diff = val_next - val_current
            num_steps = point_next - point_current
            interolation_step = vals_diff/num_steps
            for j in range(num_steps):
                result.append(val_current + j*interolation_step)



        if self.facts[-1].point != self.bassin_len-1:
            dist_to_right = self.bassin_len - self.facts[-1].point
            result += [self.facts[-1].val] * dist_to_right
        else:
            result.append(self.facts[-1].val)

        return result

if __name__ == "__main__":
    fig, ax = plt.subplots()

    auto = Auto(bassin_len=7)
    auto.set_constant(5)
    prediction = auto.get_prediction()
    #ax.plot(prediction)


    auto.add_fact(point=1, val=1)
    auto.add_fact(point=2, val=0)
    auto.add_fact(point=4, val=3)

    prediction = auto.get_prediction()


    ax.plot(prediction)
    for fact in auto.facts:
        ax.scatter(fact.point, fact.val, color='green')
    ax.set_xticks(range(0, len(prediction)))


    plt.show()

