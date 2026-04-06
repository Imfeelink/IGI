from decimal import Decimal

def get_decimal_number(message: str) -> Decimal:
    '''returns float number, checks wrong input.'''
    while True:
        user_input = input(message)
        try:
            x = Decimal(user_input)
            return x
        except ValueError:
            print("Wrong input! Try again")

def get_int_number(message: str) -> int:
    '''returns int number, checks wrong input.'''
    while True:
        user_input = input(message)
        try:
            x = int(user_input)
            return x
        except ValueError: 
            print("Wrong input! Try again")

def get_words_from_string(string: str) -> str:
    '''returns list of words from string.'''
    clean_string = string.replace(',', ' ').replace('.', ' ')
    return clean_string.split()