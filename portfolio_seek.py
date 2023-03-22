import pandas as pd
import random as rd
from itertools import combinations
import math


# input_data("training_tabu_data.xlsx")


class TS:
    def __init__(self, path, seed, tabu_tenure, initial_solution):
        self.path = path
        self.seed = seed
        self.tabu_tenure = tabu_tenure
        self.initial_solution = initial_solution
        self.instance_dict = self.input_data()
        # self.tabu_str, self.Best_solution, self.Best_objvalue = self.TSearch()

    def input_data(self):
        """Takes the path of the excel file of the SMTWTP instances.
        Returns a dict of jobs number as Key and weight, processing time (hours) and due date (hours) as values.
        """
        return pd.read_excel(
            self.path,
            names=[
                "index",
                "code",
                "risk",
                "group",
                "groupcode",
                "std",
                "fundreturn",
                "1m",
                "3m",
            ],
            index_col=0,
            sheet_name=0,
        ).to_dict("index")

    def get_tabuestructure(self):
        """Takes a dict (input data)
        Returns a dict of tabu attributes(pair of jobs that are swapped) as keys and [tabu_time, MoveValue,
        frequency count, penalized MoveValue]
        """
        dict = {}
        for swap in combinations(self.instance_dict.keys(), 2):
            dict[swap] = {"tabu_time": 0, "MoveValue": 0, "freq": 0}
        return dict

    def swap(n, p, q):
        """
        reverse the bits if they aren't equal each other
        """
        # if bits are different at position `p` and `q`
        if (((n & (1 << p)) >> p) ^ ((n & (1 << q)) >> q)) == 1:
            n ^= 1 << p
            n ^= 1 << q

        return n

    def printKthBit(self, n, k):
        return (n >> (k - 1)) % 2

    def get_InitialSolution(self, show=False):
        n_jobs = len(self.instance_dict)  # Number of funds
        # set it manually (write it with bit format)

        stock_set = 0b0000000000000000111111

        # initial_solution = list(range(1, n_jobs + 1))
        # rd.seed(self.seed)
        # rd.shuffle(initial_solution)
        # if show == True:
        #     print("initial Random Solution: {}".format(initial_solution))
        return stock_set

    def Objfun(self, solution, show=False):
        """Takes a set of stocks,
        Return the objective function value of the solution
        """
        dict = self.instance_dict
        l_dict = len(dict)
        objfun_value = 0

        for i in range(l_dict):
            if self.printKthBit(solution, i + 1):  # Decides whether stock included
                objfun_value += 1 * dict[i]["fundreturn"]

        if show == True:
            print(
                "\n",
                "#" * 8,
                "The Objective function value for {:022b} solution schedule is: {:.4f}".format(
                    solution, objfun_value
                ),
                "#" * 8,
            )
        return objfun_value

    def TSearch():
        pass
