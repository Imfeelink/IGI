'''
Counts number of words shorter then 7 symbols
Finds the shortest word ending in "a"
Prints words in descending order of their lengths.
Lab #3
v1
Kryshalovih Ivan Pavlovich
30.03.2026 
'''

import task_funcs
import decorators

STRING = "So she was considering in her own mind, as well as she could, for the hot day made her feel \
very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble \
of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by \
her."

@decorators.repeat_run
def task4_main():
    lower_string = STRING.lower()
    print(f"count of words shorter than 7 symbols: {task_funcs.count_words_shorter_then(lower_string, 7)}")
    print(f"the shortest word ending on 'a': {task_funcs.find_shortest_word_ending_on_letter(lower_string, 'a')}")
    print("words in descending order:")
    sorted_words = task_funcs.get_words_descending_order(lower_string)
    for word in sorted_words:
        print(word)

if(__name__ == "__main__"):
    task4_main()