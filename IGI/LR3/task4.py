'''
Counts number of words shorter then 7 symbols
Finds the shortest word ending in "a"
Prints words in descending order of their lengths.
Lab #3
v1
Kryshalovih Ivan Pavlovich
30.03.2026 
'''

import functions

STRING = "So she was considering in her own mind, as well as she could, for the hot day made her feel \
very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble \
of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by \
her."
#45
#need 46: stupid, WRONG, stupid RIGHT


@functions.repeat_run
def task4_main():
    lower_string = STRING.lower()
    print(functions.count_words_shorter_then(lower_string, 7))
    

if(__name__ == "__main__"):
    task4_main()