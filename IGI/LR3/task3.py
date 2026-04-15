'''
Gets string
Returns number of spaces and commas
Lab #3
v1
Kryshalovich Ivan Pavlovich
30.03.2026 
'''

import task_funcs
import decorators

@decorators.repeat_run
def task3_main():
    '''Gets string
    Returns number of spaces and commas'''
    string_to_search = input("print your string: ")
    result = task_funcs.get_spaces_commas(string_to_search)
    print(f"spaces: {result[0]}, commas: {result[1]}")


if(__name__ == "__main__"):
    task3_main()