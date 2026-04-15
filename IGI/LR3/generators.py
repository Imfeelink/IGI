import random

#5 generators
def gen_fill_arr_int(arr: list, size: int):
    '''generator: 
    gets list and fills it with random int numbers from -1000 to 1000'''
    for i in range(size):
        yield arr.append(random.randint(-1000, 1000))

def gen_fill_arr_float(arr: list, size: int):
    '''generator: 
    gets list and fills it with random float numbers from -1000 to 1000
    rounds values to 2 digits after point'''
    for i in range(size):
        yield arr.append(round(random.uniform(-1000, 1000), 2))