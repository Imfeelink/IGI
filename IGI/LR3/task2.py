'''
Gets int numbers and subtracts them from 10000
Ends when result of last subtract is negative
Lab #3
v1
Kryshalovih Ivan Pavlovich
30.03.2026 
'''

import task_funcs
import decorators
from general_funcs import *

@decorators.repeat_run
def task2_main():
    '''Gets int numbers and subtracts them from 10000
    Ends when result of last subtract is negative'''
    task_number = 10000
    while(task_number >= 0):
        print(f"Changing number: {task_number}")
        num = get_int_number("print int num: ")
        task_number -= num
    
    print(f"Program ended, result: {task_number}")

if(__name__ == "__main__"):
    task2_main()