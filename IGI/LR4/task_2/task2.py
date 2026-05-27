'''
Analyze text from file 
Print info by task: sentence count, count declarative, interrogative and exclamatory,
average sentence and word length.
Get list of dates and words, where 3rd letter from end is consonant and last but one is vowel,
count of words starting with vowel, count and ordinal number words that have two identical letters in a row
Print words in alphabet order 
Save to zip archieve
Get info about zip archieve
Kryshalovich Ivan Pavlovich
task2
var14
03.05.2026
'''

import sys
import os

#appends parent folder(LR4) to system path Python 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import mixins
from task2_classes import *

def task2_main():
    analyze_manager = VariantAnalyzer("file_to_analyze.txt", "file_info.txt")
    analyze_manager.analyze_save_info()

if __name__ == "__main__":
    task2_main()