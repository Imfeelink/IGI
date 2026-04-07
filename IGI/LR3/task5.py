'''
create list by user input or by generator
check if user input is correct 
return index of minimal negative element
return sum of elements between first two negative elements
Lab #3
v1
Kryshalovich Ivan Pavlovich
01.04.2026 
'''

import task_funcs
import generators
import decorators

@decorators.repeat_run
def task5_main():
    arr = []
    choice = input("1: enter value \n2: generate random values \ninput: ").strip()
    if choice == "1":
        task_funcs.user_input_fill_arr(arr)
    elif choice == "2":
        generators.gen_fill_arr_float(arr)

    print()

    index = task_funcs.get_index_min_negative_el(arr)
    if index is None:
        print("array doesn't contain negative element")
    else:
        print(f"minimal negative element index: {index}")

    print()

    sum = task_funcs.get_sum_between_negative_els(arr)
    if sum is None:
        print("there is no 2 negative elements in array")
    else: 
        print(f"sum of elements between first two negative elements: {sum}")
    print(arr)

if(__name__ == "__main__"):
    task5_main()