import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt

def growth_investment(contribute_per_year: list=[3000, 4500, 6000], estimated_return: list=[0.03, 0.06, 0.09], years: int=30):
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
            plt.ylabel("Amount ($)")
            plt.xlabel("Years from Current Year")
            plt.show()       