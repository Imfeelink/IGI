'''
calculates sum of a series until epsilant precision
counts necessary members
prints result of python function calculating same sum of a series 
Lab #3
v1
Kryshalovih Ivan Pavlovich
29.03.2026 
'''
import functions
from functions import math
EPS = 0.001
MAX_ITERATIONS = 500

@functions.repeat_run
def task1_main():
    '''calculates sum of a series until epsilant precision
    counts necessary members
    prints result of python function calculating same sum of a series'''
    print("Task 1")

    while True:
        x = functions.get_decimal_number("print x, |x| < 1: ")
        if(abs(x) < 1): break

    sum = 0

    for i in range(1, MAX_ITERATIONS+1):
        member = functions.get_ln_series_member(x, i)
        if(abs(member) < EPS):
            print(f"x = {x} \
                    n = {i} \
                    ln(1-x) = {sum} \
                    Math ln(1-x) = {math.log(1-x)} \
                    eps = {EPS}")
            break
        elif(i == MAX_ITERATIONS):
            print("Needed accuracy wasn't achieved")
        sum += member 

if(__name__ == "__main__"):
    task1_main()