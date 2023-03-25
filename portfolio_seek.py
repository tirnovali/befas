import pandas as pd
import random as rd
from itertools import combinations
import math


# input_data("training_tabu_data.xlsx")


class TS:
    def __init__(
        self, path, seed, tabu_tenure, initial_solution, sector_sd, risk_total
    ):
        self.path = path
        self.seed = seed
        self.tabu_tenure = tabu_tenure
        self.initial_solution = initial_solution
        self.sector_sd = sector_sd
        self.risk_total = risk_total
        self.instance_dict = self.input_data()
        self.tabu_table, self.best_solution, self.best_objvalue = self.TSearch()

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

    def swap(self, n, p, q):
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

    def objfun(self, solution, show=False):
        """Takes a set of stocks,
        Return the objective function value of the solution
        """
        dict = self.instance_dict
        l_dict = len(dict)
        risk_cumulative = 0  # starting risk
        objfun_value = 0

        for i in range(l_dict):
            if self.printKthBit(solution, i + 1):  # Decides whether stock included
                if dict[i]["std"] < self.sector_sd:
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

    def TSearch(self):
        tenure = self.tabu_tenure
        tabu_table = self.get_tabuestructure()
        best_solution = self.initial_solution
        best_objvalue = self.objfun(best_solution)
        current_solution = self.initial_solution
        current_objvalue = self.objfun(current_solution)

        print(
            "\n"
            "#" * 30,
            "Short-term memory TS with Tabu Tenure: {}\nInitial Solution: {:022b}, Initial Objvalue: {}".format(
                tenure, current_solution, current_objvalue
            ),
            "#" * 30,
            sep="\n\n",
        )

        iter = 1
        terminate = 0

        while terminate < 100:
            print(
                "\n\n### ITERATION [{}]###\nCurrent_Objvalue: {}\nBest_Objvalue: {}\nBest_solution: {:022b}\n".format(
                    iter, current_objvalue, best_objvalue, best_solution
                ), "-"*30, sep="\n"
            )

            # Searching the whole neighborhoods:
            for move in tabu_table:
                # if the bits are different at positions.
                candidate_solution = self.swap(current_solution, move[0], move[1])
                candidate_objvalue = self.objfun(candidate_solution)
                tabu_table[move]["MoveValue"] = candidate_objvalue

            # Admissible move

            while True:
                # maximization
                # select the move with the highest ObjValue in the neighborhood
                best_move = max(tabu_table, key=lambda x: tabu_table[x]["MoveValue"])
                best_move_value = tabu_table[best_move]["MoveValue"]
                tabu_time = tabu_table[best_move]["tabu_time"]

                # Not Tabu
                if tabu_time < iter:
                    # Make the move
                    current_solution = self.swap(current_solution, best_move[0], best_move[1])
                    current_objvalue = self.objfun(current_solution)

                    # Best improving move
                    if best_move_value > best_objvalue:
                        best_solution = current_solution
                        best_objvalue = current_objvalue
                        print(
                            ">> best_move: {}, Objvalue: {}, Best_solution: {:022b} => Best Improving => Admissible".format(
                                best_move, current_objvalue, current_solution
                            )
                        )
                        # Start from beginning with new best solution
                        terminate = 0
                    else:
                        print(
                            "##Termination: {}## best_move: {}, Objvalue: {} => Least non-improving => "
                            "Admissible".format(terminate, best_move, current_objvalue)
                        )
                        terminate += 1
                    
                    # Update tabu time for the move
                    tabu_table[best_move]['tabu_time'] = iter + tenure
                    iter += 1
                    break
                    
                 # If tabu
                else:
                    # Aspiration
                    if best_move_value > best_objvalue:
                        # Make the move
                        current_solution = self.swap(current_solution, best_move[0], best_move[1])
                        current_objvalue = self.objfun(current_solution)
                        best_solution = current_solution
                        best_objvalue = current_objvalue
                        print("   best_move: {}, Objvalue: {} => Aspiration => Admissible".format(best_move, current_objvalue))
                        
                        terminate = 0
                        iter += 1
                        
                        break

                    else:
                        tabu_table[best_move]["MoveValue"] = float('inf')
                        print("   best_move: {}, Objvalue: {} => Tabu => Inadmissible".format(best_move, current_objvalue))
                        
                        continue

        return tabu_table, best_solution, best_objvalue                