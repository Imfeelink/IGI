'''
calculates sum of a series until epsilant precision
counts necessary members
prints result of python function calculating same sum of a series 
Lab #3
v1
Kryshalovich Ivan Pavlovich
29.03.2026 
'''
import task_funcs
from task_funcs import math
import decorators
from general_funcs import *
EPS = 0.001
MAX_ITERATIONS = 500

@decorators.repeat_run
def task1_main():
    '''calculates sum of a series until epsilant precision
    counts necessary members
    prints result of python function calculating same sum of a series'''
    print("Task 1")

    while True:
        x = get_decimal_number("print x, |x| < 1: ")
        if(abs(x) < 1): break

    sum = 0

    for i in range(1, MAX_ITERATIONS+1):
        member = task_funcs.get_ln_series_member(x, i)
        print(f"x = {x:<8}", end="\t")
        print(f"n = {i:<8}", end="\t")
        print(f"ln(1-x) = {round(sum, 5):<8}", end="\t")
        print(f"Math ln(1-x) = {round(math.log(1-x), 5):<12}", end="\t")
        print("eps = {EPS}")
        if(abs(member) < EPS):
            break
        elif(i == MAX_ITERATIONS):
            print("Needed accuracy wasn't achieved")
        sum += member 

if(__name__ == "__main__"):
    task1_main()