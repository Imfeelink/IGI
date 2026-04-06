import math
import random
from decimal import Decimal
from general_funcs import *

#1
def get_ln_series_member(x: Decimal, n: int) -> Decimal:
    '''calculates n-th member of ln(1-x) series.'''
    return (-1 * x**n / n)

#3
def get_spaces_commas(string: str) -> tuple[int, int]:
    '''returns count of spaces and commas of given string.'''
    spaces_count = 0
    commas_count = 0
    for symbol in string:
        if(symbol == ' '): spaces_count += 1
        elif(symbol == ','): commas_count += 1
    return (spaces_count, commas_count)

#4
def count_words_shorter_then(string: str, length: int) -> int:
    '''returns count of words shorter then given length.'''
    count = 0
    words = get_words_from_string(string)
    for word in words:
        if(len(word) < length): count += 1
    return count

def find_shortest_word_ending_on_letter(string: str, letter: str) -> str:
    '''returns the shortest word in string ending on given letter.'''
    shortest_word = None
    words = get_words_from_string(string)
    for word in words:
        if(shortest_word == None or (word[-1] == letter and len(word) < len(shortest_word))): shortest_word = word
    return shortest_word

def get_words_descending_order(string: str) -> list[str]:
    '''returns list of words from string in descending order.'''
    words = get_words_from_string(string)
    words = sorted(words, key=len, reverse=True)
    return words

#5
def user_input_fill_arr(arr: list):
    '''gets list and fills it with user input values
    stops working when user input is empty string or not a number'''
    while True:
        user_input = input("print your numbers(enter or dif symbol to stop): ")
        if not user_input:
            break
        try:
            for el in user_input.split():
                el = float(el)
                arr.append(el)
        except ValueError:
            break
    print("ending filling array")


def get_index_min_negative_el(arr: list) -> int:
    '''gets list
    returns index of minimal negative element
    if list doesn't contain negative elements returns None'''
    index = None
    for i in range(len(arr)):
        if(arr[i] < 0 and (index is None or arr[i] < arr[index])):
            index = i
    return index

def get_sum_between_negative_els(arr: list) -> float:
    '''gets list 
    return sum of elements between first two negative elements'''
    result = 0
    found_first = False
    for el in arr:
        if not found_first:
            if el < 0:
                found_first = True
        else:
            if el < 0:
                return result
            result += el
    return None