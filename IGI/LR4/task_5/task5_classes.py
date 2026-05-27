import numpy as np
from numpy import random
import math

class GeneralTaskFuncs():
    numbers_range = 100

    def __init__(self, rows: int, columns: int):
        '''creates ndarray with given size filled with zeros'''
        self.rows = rows
        self.columns = columns
        self.arr = np.zeros((rows, columns))

    def random_arr(self):
        '''
        fills self ndarray with random numbers in self.numbers_range range
        '''
        self.arr = random.randint(self.numbers_range, size = (self.rows, self.columns))

    def get_el_by_index(self, index1: int, index2: int):
        '''returns index element'''
        return self.arr[index1, index2]

    def get_arr_slice(self, slice):
        return self.arr[slice]

    def sum_arr(self, given_arr: np.array):
        if self.arr.shape != given_arr.shape:
            raise ValueError("Given array has different size!")
        
        self.arr += given_arr
        return self.arr

    def multiply_arr(self, given_arr: np.array):
        if self.arr.shape != given_arr.shape:
            raise ValueError("Given array has different size!")
        
        self.arr *= given_arr
        return self.arr

    def sqrt_arr(self):
        '''extracts the square root of each element in array'''
        np.sqrt(self.arr)

    def get_mean(self):
        '''returns mean of array'''
        return np.mean(self.arr)
    
    def get_median(self):
        '''returns meadian of array'''
        return np.median(self.arr)
    
    def get_corrcoef(self):
        '''returns matrix of Pearson correlation coefficients'''
        return np.corrcoef(self.arr)
    
    def get_variance(self):
        '''returns variance(dispersion) of array'''
        return round(self.arr.var(), 2)
    
    def get_std(self):
        '''returns standard deviation of array elements'''
        return round(self.arr.std(), 2)
    
class Task14Var(GeneralTaskFuncs):
    def get_sum_beneath_diag(self):
        '''
        returns sum of elements placed beneath main diagonal
        '''
        return np.tril(self.arr, k=-1).sum()
    
    def get_std_diag(self):
        '''
        returns std of elements of main diagonal using numpy func
        '''
        main_diagonal = self.arr.diagonal()
        return round(np.std(main_diagonal), 2)

    def get_std_formula(self):
        '''
        returns std of elements of main diagonal using formula
        '''
        if self.rows < 2 or self.columns < 2:
            return 0
        main_diagonal = self.arr.diagonal()
        mean = main_diagonal.mean()
        denominator = len(main_diagonal)
        return round(math.sqrt(sum((x - mean)**2 for x in main_diagonal) / denominator), 2)
