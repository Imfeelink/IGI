import sys
import os

#appends parent folder(LR4) to system path Python 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import mixins
import re

class BaseTextAnalyzer(mixins.LogMixin):
    #filename - filename with text to analyze
    def __init__(self, filename: str, saved_info_filename: str):
        self.filename = filename
        self.saved_info_filename = saved_info_filename
        self.filetext = self._read_file()

    # _ means it's method used inside class
    def _read_file(self):
        '''reads file and returns its text
        if file is empty, returns empty string'''
        try:
            with open(self.filename, 'r') as myfile:
                return myfile.read()
        except FileNotFoundError:
            self.log("Error! File not found")
            return ""

    def save_info_to_file(self, report_text: str, filename: str):
        '''saves given text to file'''
        with open(filename, "w", encoding="utf-8") as output_file:
            output_file.write(report_text)
        self.log("analysis information saved to file")

    def _get_words_list(self) -> int:
        return re.findall(r'[a-zA-Zа-яА-ЯёЁ0-9]+', self.filetext)
    
    def _get_total_chars(self, words: list) -> int:
        return sum(len(word) for word in words)

    def sentence_count(self) -> int:
        '''counts . ! ? in any order and count'''
        pattern = r'(?<!\s)[.!?]+(?=\s|$)'
        punctuation_groups = re.findall(pattern, self.filetext)
        return len(punctuation_groups)
    
    def declarative_sentence_count(self) -> int:
        '''counts declarative sentences
        declaratives sentences ends on '.' '''
        pattern = r'(?<![\s.!?])\.+(?=\s|$)'
        declarative_sentences = re.findall(pattern, self.filetext)
        return len(declarative_sentences)
    
    def interrogative_sentence_count(self) -> int:
        '''counts interrogative sentences
        interrogative sentence ends on '?', '!?' or '?!' '''
        interrogative_sentence = re.findall(r'[^\s.!?][^.!?]*[!?]*\?[!?]*', self.filetext)
        return len(interrogative_sentence)
    
    def exclamatory_sentence_count(self) -> int:
        '''counts exclamatory sentences
        exclamatory sentence ends on '!' '''
        exclamatory_sentences = re.findall(r'[^\s.!?][^.!?]*!+(?![.?])', self.filetext)
        return len(exclamatory_sentences)

    def avg_sentence_length(self) -> int:
        '''returns average sentence length'''
        sentences = self.sentence_count()
        words = self._get_words_list()
        total_chars = self._get_total_chars(words)
        if sentences > 0:
            return round(total_chars / sentences, 2)
        else:
            return 0

    def avg_word_length(self) -> int:
        '''returns average word length'''
        words = self._get_words_list()
        total_chars = self._get_total_chars(words)
        if len(words) > 0:
            return round(total_chars / len(words), 2)
        else:
            return 0

    def smiles_count(self) -> int:
        '''returns smiles count
        ?: used to group brackets and get entire regular expression except of only what in brackets'''
        smiles = re.findall(r'[:;]-*(?:\(+|\)+|\[+|\]+)', self.filetext)
        return len(smiles)

#14 var functions
class VariantAnalyzer(BaseTextAnalyzer, mixins.ZipArchieverMixin): 
    def __init__(self, filename: str, saved_info_filename: str):
        super().__init__(filename, saved_info_filename) 

    def analyze_save_info(self):
        '''uses every task function, saves info to string, and writes this string to file'''
        sencs = self.sentence_count()
        dec_sencs = self.declarative_sentence_count()
        interg_sencs = self.interrogative_sentence_count()
        excl_sencs = self.exclamatory_sentence_count()
        avg_senc_len = self.avg_sentence_length()
        avg_word_length = self.avg_word_length()
        years_list = self.get_year_dates()
        spec_end_words_list = self.get_specific_ending_words()
        vowel_words = self.count_vowel_starting_words()
        double_let_word_index_tuples_list = self.get_double_letter_words_with_index()
        formatted_double_letters = ", ".join(f"{word}: {idx}" for idx, word in double_let_word_index_tuples_list)
        if not formatted_double_letters:
            formatted_double_letters = "Not found"

        alphabetical_words_list = self.get_alphabetical_words()

        report = (
            f"  1. Sentences: {sencs}\n"
            f"  2. Declarative sentences: {dec_sencs}\n"
            f"  3. Interrogative_sentences: {interg_sencs}\n"
            f"  4. Exclamatory sentences: {excl_sencs}\n"
            f"  5. Average sentence length: {avg_senc_len}\n"
            f"  6. Average word length: {avg_word_length}\n"
            f"  7. Years: {', '.join(years_list)}\n"
            f"  8. Specific ending words: {', '.join(spec_end_words_list)}\n"
            f"  9. Words starting with vowel letter: {vowel_words}\n"
            f"  10. Words with two identical letters in a row with index: {formatted_double_letters}\n"
            f"  11. Words in alphabetical order: {', '.join(alphabetical_words_list)}"
        )

        self.log("---Task Info---")
        print(report)
        self.save_info_to_file(report, self.saved_info_filename)
        
        archive_name = "info_file.zip"
        self.pack_to_zip(self.saved_info_filename, archive_name)
        self.log("File packed to zip")

        self.log("Archive info")
        self.print_zip_info(archive_name)

    def get_year_dates(self) -> list:
        '''returns list of dates in "yyyy" format'''
        pattern = r'\b\d{4}\b'
        return re.findall(pattern, self.filetext)

    def get_specific_ending_words(self) -> list:
        '''returns list of words where the 2nd letter from end is vowel and third from end is consonant'''
        consonants = r'[bcdfghjklmnpqrstvwxzбвгджзйклмнпрстфхцчшщ]'
        vowels = r'[aeiouyаеёиоуыэюя]'
        any_letter = r'[a-zа-яё]'
        
        pattern = rf'\b{any_letter}*{consonants}{vowels}{any_letter}\b'
        
        return re.findall(pattern, self.filetext, flags=re.IGNORECASE)
    
    def count_vowel_starting_words(self) -> int:
        '''counts words that starting with vowel letter
        returns number of such words'''
        pattern = r'\b[aeiouyаеёиоуыэюя][a-zа-яё]*\b'
        words = re.findall(pattern, self.filetext, flags=re.IGNORECASE)
        return len(words)
    
    def get_double_letter_words_with_index(self) -> list:
        '''returns list of tuples that contains index and word that has 2 identical letter in a row'''

        all_words = re.findall(r'\b[a-zа-яё]+\b', self.filetext, flags=re.IGNORECASE)
        
        result =[]

        for index, word in enumerate(all_words, start=1):
            if re.search(r'([a-zа-яё])\1', word, flags=re.IGNORECASE):
                result.append((index, word))
                
        return result
    
    def get_alphabetical_words(self) -> list:
        '''returns list of words in alphabetical order'''
        all_words = re.findall(r'\b[a-zа-яё]+\b', self.filetext, flags=re.IGNORECASE)
        
        return sorted(all_words, key=str.lower)    
    
    