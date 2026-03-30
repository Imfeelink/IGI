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
def get_ln_series_member(x: Decimal, n: int) -> Decimal:
    '''calculates n-th member of ln(1-x) series'''
    return (-1 * x**n / n)

#3
def get_spaces_commas(string: str) -> tuple[int, int]:
    '''returns count of spaces and commas of given string'''
    spaces_count = 0
    commas_count = 0
    for symbol in string:
        if(symbol == ' '): spaces_count += 1
        elif(symbol == ','): commas_count += 1
    return (spaces_count, commas_count)

def get_words_from_string(string: str) -> str:
    '''returns list of words from string'''
    clean_string = string.replace(',', ' ').replace('.', ' ')
    return clean_string.split()

#4
def count_words_shorter_then(string: str, length: int) -> int:
    '''returns count of words shorter then given length'''
    count = 0
    words = get_words_from_string(string)
    for word in words:
        if(len(word) < length): count += 1
    return count

#4
def find_shortest_word_ending_on_letter(string: str, letter: str) -> str:
    '''returns the shortest word in string ending on given letter'''
    shortest_word = None
    words = get_words_from_string(string)
    for word in words:
        if(shortest_word == None or (word[-1] == letter and len(word) < len(shortest_word))): shortest_word = word
    return shortest_word

#4
def get_words_descending_order(string: str) -> list[str]:
    '''returns list of words from string in descending order'''
    words = get_words_from_string(string)
    words = sorted(words, key=len, reverse=True)
    return words