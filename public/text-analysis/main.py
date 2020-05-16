import os
import pymorphy2
import string
import re

import itertools

ukrainian_letters = ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ',
                     'з', 'х', 'ї', 'ґ', 'є', 'ж', 'д', 'л', 'о', 'р', 'п', 'а', 'в', 'i',
                     'ф', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', "'", "’"]


class Text(object):
    """docstring for Text"""

    def __init__(self, file_content, clean_up=False):
        self.morph = pymorphy2.MorphAnalyzer(lang='uk')

        # Split file into sentences
        sentences = re.split(r'\.\s|\n|\?|\!', file_content)
        sentences = [re.sub(r'[^А-ЩЬЮЯҐЄІЇа-щьюяґєії]', ' ', s) for s in sentences]
        sentences = [s.split(' ') for s in sentences]

        if clean_up:
            def is_ukr_word(word):
                # Check if the word is ukrainian
                # Returns Bool value
                letters = list(word)
                for letter in letters:
                    if not letter.lower() in ukrainian_letters:
                        return False
                return True
            
            def is_valid_word(word):
                w = word.strip(string.punctuation+'«»')
                return is_ukr_word(w) and len(w) > 2 and self.morph.parse(w)[0].tag.POS in ['NOUN', 'ADJF', 'NPRO', 'VERB', 'ADVB']
            
            sentences = [list(filter(is_valid_word, s)) for s in sentences]
        sentences = [list(filter(lambda x: len(x) > 0, s)) for s in sentences]

        self.sentences = [' '.join(s) for s in sentences]
        self.all_words = [leaf for tree in sentences for leaf in tree]

        # Num of words
        self.num_words = len(self.all_words)
        # Num of sentences
        self.num_sent = len(self.sentences)

    def analyse(self):
        """Returns number of words, number of sentences, average word length and average sentence length in tuple """

        # Average length of word
        total_length = 0
        for word in self.all_words:
            total_length += len(word)
        av_word_len = total_length/self.num_words

        # Average length of sentence
        total_length = 0
        for sentence in self.sentences:
            total_length += len(sentence)
        av_sent_len = total_length/self.num_words

        return self.num_words, self.num_sent, av_word_len, av_sent_len

    def freq_dict(self, list_of_words=None):
        unique_words = set(list_of_words)
        # num_of_un_words = len(unique_words)
        freq_dict = {}
        for un_word in unique_words:
            freq_dict[un_word.lower()] = list_of_words.count(un_word)

        # Sort by frequency
        sorted_words = sorted(freq_dict, key=freq_dict.get)
        sorted_words.reverse()

        new_freq_dict = {}
        for word in sorted_words:
            new_freq_dict[word] = freq_dict[word]
        return new_freq_dict

    def get_relative_lemma_freq(self):
        """Returns key value pair of lemmas and relative frequency
        {key(str):value(float)}
        """
        lemmas = []
        for word in self.all_words:
            p = self.morph.parse(word)[0]
            lemmas.append(p.normal_form)

        lemmas_dict = self.freq_dict(list_of_words=lemmas)

        out = []
        for word in lemmas_dict:
            out.append(f'{word} - {self.get_POS_for_word(word)} - {lemmas_dict[word]}')
        return out

    def get_POS_for_word(self, word):
        return self.morph.parse(word)[0].tag.POS

    def get_parts_of_speach_freq(self):
        """Returns key value pair of parts of speach frequency"""
        parts_of_speech = {}
        for word in self.all_words:
            pos = self.get_POS_for_word(word)

            if pos in parts_of_speech:
                parts_of_speech[pos] += 1
            else:
                parts_of_speech[pos] = 0

        return parts_of_speech


if __name__ == '__main__':

    # Helper functions
    def dict_to_text(dictionary):
        """ Transform dictionary to str for readability """
        text = ''
        for key in dictionary:
            text += f'{key} - {dictionary[key]}\n'
        return text

    def create_report(f_path, fff):
        """Creates report in the folder"""
        report = ''
        for file in [fff]:
            if file.startswith(".") or file.startswith("report") or file.startswith("readme"):
                return
            if not file.endswith(".txt"):
                return

            try:
                with open(f_path + os.sep + file, mode='r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception:
                continue

            text = Text(file_content)
            text_c = Text(file_content, clean_up=True)

            text_c_lemma_count = '\n'.join(text_c.get_relative_lemma_freq())
            text_c_parts_count = dict_to_text(text_c.get_parts_of_speach_freq())

            def analyse_formatted(text):
                num_words, num_sent, av_word_len, av_sent_len = text.analyse()
                return f"""
Number of words: {num_words},
Number of sentences: {num_sent},
Average word length: {av_word_len},
Average sentence length: {av_sent_len}
"""

            report += f"""
File: {file},
Type: Науково-публицистичний,
            
BEFORE CLEAN-UP 
{analyse_formatted(text)}

AFTER CLEAN-UP 
{analyse_formatted(text_c)}
Lemmatization:
{text_c_lemma_count}

Parts of speech:
{text_c_parts_count}
"""
        with open(os.path.join(f_path, f'report_{fff}'), 'w', encoding='utf-8') as f:
            f.write(report)
    
    def is_valid_file(file):
        if file.startswith(".") or file.startswith("report") or file.startswith("readme"):
            return False
        if not file.endswith(".txt"):
            return False
        return True

    for root, dirs, files in os.walk(os.getcwd()):
        path = root.split(os.sep)
        for file in files:
            if is_valid_file(file):
                create_report(root, file)
    
    for d in ['easy', 'complex', 'moderate']:
        content = '' 
        for root, dirs, files in os.walk(d):
            for file in files:
                if not is_valid_file(file):
                    continue
                try:
                    with open(root + os.sep + file, mode='r', encoding='utf-8') as f:
                        content += f.read() + '\n'
                except Exception:
                    continue
        
        text = Text(content)
        text_c = Text(content, clean_up=True)
        
        num_words, _, _, _ = text.analyse()
        num_words_c, _, _, _ = text_c.analyse()

        text_c_lemma_count = '\n'.join(text_c.get_relative_lemma_freq())

        report = f"""
BEFORE CLEAN-UP 

Total words: {num_words},

AFTER CLEAN-UP 

Total words: {num_words_c},
Lemmatization:
{text_c_lemma_count}
        """

        with open(f'{d}/report.txt', 'w', encoding='utf-8') as f:
            f.write(report)

