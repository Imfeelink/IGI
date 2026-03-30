'''
Gets string
Returns number of spaces and commas
Lab #3
v1
Kryshalovih Ivan Pavlovich
30.03.2026 
'''

import functions

@functions.repeat_run
def task3_main():
    '''Gets string
    Returns number of spaces and commas'''
    string_to_search = input("print your string: ")
    result = functions.get_spaces_commas(string_to_search)
    print(f"spaces: {result[0]}, commas: {result[1]}")


if(__name__ == "__main__"):
    task3_main()