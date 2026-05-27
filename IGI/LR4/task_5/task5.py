"""
using numpy create matrix with random numbers
test functions
calculate sum of elements beneath main diagonal,
standard deviation for the elements of the main diagonal using:
numpy func and self-made function
Lab 4
variant 14
v1
Kryshalovich Ivan Pavlovich
14.05.2026
"""

from task5_classes import *

#np.s_[a:b, c:d] - slice

def task5_main():
    try:
        arr_obj = Task14Var(3, 3)
        print("\t\tBase Functionality:")
        arr_obj.random_arr()
        print(arr_obj.arr)
        print()
        print("el by index: ", arr_obj.get_el_by_index(2,1))
        print("array slice: \n", arr_obj.get_arr_slice(np.s_[0:2, 1:3]))
        arr_to_sum = np.array([[0,1,0], [2,1,0], [0, 5, 2]])
        print("sum of two arrays: \n", arr_obj.sum_arr(arr_to_sum))
        arr_to_mult = np.array([[1,2,1], [1,1,3], [2,1,1]])
        print("result of multiplying two arrays: \n", arr_obj.multiply_arr(arr_to_mult))
        print("mean: ", arr_obj.get_mean())
        print("meadian: ", arr_obj.get_median())
        print("corroef: \n", arr_obj.get_corrcoef())
        print("variance: ", arr_obj.get_variance())
        print("standard deviation(std): ", arr_obj.get_std())

        print("\n\t\t14 Variant Functionality:")
        print("sum of elements beneath main diagonal: ", arr_obj.get_sum_beneath_diag())
        print("std of main diagonal: ", arr_obj.get_std_diag())
        print("std of main diagonal using formula: ", arr_obj.get_std_formula())  
    except ValueError as err:
        print("ValueError! ", err)
    except Exception as err:
        print("Unexpected Error!", err)

if __name__ == '__main__':
    task5_main()