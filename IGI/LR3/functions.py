import math
from decimal import Decimal

def get_decimal_number(message: str) -> Decimal:
    '''returns float number, checks wrong input'''
    while True:
        user_input = input(message)
        try:
            x = Decimal(user_input)
            return x
        except:
            print("Wrong input! Try again")

def get_int_number(message: str) -> int:
    '''returns int number, checks wrong input'''
    while True:
        user_input = input(message)
        try:
            x = int(user_input)
            return x
        except:
            print("Wrong input! Try again")

def repeat_run(func):
    '''gets function, launches it and asking user if he needs to launch program again
    uses decorator'''
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)

            answer = input("Wanna launch program again(y - yes, n - no): ").strip().lower()
            if(answer == 'yes' or answer == 'y'):
                continue
            elif(answer == 'no' or answer == 'n'):
                break
            else:
                break  #можно допилить обработку неправильного ввода
    return wrapper

#1
def get_ln_series_member(x: float, n: int) -> float:
    '''calculates n-th member of ln(1-x) series'''
    return (-1 * x**n / n)

def get_spaces_commas(string: str) -> tuple[int, int]:
    '''returns count of spaces and commas of given string'''
    spaces_count = 0
    commas_count = 0
    for symbol in string:
        if(symbol == ' '): spaces_count += 1
        elif(symbol == ','): commas_count += 1
    return (spaces_count, commas_count)
