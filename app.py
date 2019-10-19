from libs.utils import startup_script, get_finance_file_data
from libs.tasks import task_handler

import numpy as np 
import matplotlib.pyplot as plt

##############################
__VERSION__ = '0.0.1'
__DATE__ = '2019-09-22'
##############################

class App:

    def __init__(self):
        self.config = dict()
        self.data = dict()

    def run(self):
        self.config = startup_script(version=__VERSION__, update_release=__DATE__)
        self.data = get_finance_file_data(self.config)
        task_handler(self.config, self.data)
        # self.growth_investment([2000, 4000, 6000], [0.03, 0.065, 0.09], 30)


    def growth_investment(self, contribute_per_year: list, estimated_return: list, years: int):
        growth = dict()
        for c in contribute_per_year:
            growth[str(c)] = []
            print(" ")
            for r in estimated_return:
                amt_list = []
                contribute_yr = float(c)
                amt = 0.0
                contr = 0.0
                amt_list.append(amt)
                for year in range(years):
                    amt += contribute_yr
                    contr += contribute_yr
                    amt = np.round(amt * (1.0 + r),2)
                    amt_list.append(amt)
                tot_return = np.round((amt - contr)/contr * 100.0, 3)
                growth[str(c)].append(amt_list)
                print(f"${contribute_yr}/yr, {years} yrs at {r} annual return \t=\t ${amt} \ton\t ${contr} contributions... \ta return of {tot_return}")

        for key in growth.keys():
            leg = []
            for i, p in enumerate(growth[key]):
                plt.plot(list(range(len(p))), p)
                leg.append(str(estimated_return[i])+"%")
            plt.legend([leg[0], leg[1], leg[2]])
            plt.title("Growth of $" + str(key) + "/yr Investment")
            plt.show()       


app = App()

if __name__ == '__main__':
    app.run()