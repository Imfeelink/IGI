import sys
import os

#appends parent folder(LR4) to system path Python 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import mixins
import re

class BaseTextAnalyzer(mixins.LogMixin):
    #filename - имя файла, в котором текст для анализа
    def __init__(self, filename: str):
        self.filename = filename
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

    def _get_words_list(self) -> int:
        return re.findall(r'[a-zA-Zа-яА-ЯёЁ0-9]+', self.filetext)
    
    def _get_total_chars(self, words: list) -> int:
        return sum(len(word) for word in words)

    def sentence_count(self) -> int:
        '''counts . ! ? in any order and count'''
        punctuation_groups = re.findall(r'[^\s.!?][^.!?]*[.!?]+', self.filetext)
        return len(punctuation_groups)
    
    def declarative_sentence_count(self) -> int:
        '''counts declarative sentences
        declaratives sentences ends on '.' '''
        declarative_sentences = re.findall(r'[^\s.!?][^.!?]*[.]+(?![!?])', self.filetext)
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

class TaskTextAnalyzer(BaseTextAnalyzer, mixins.ZipArchieverMixin):
    pass
