# -*- coding: utf-8 -*-

import os

##################################################################################

class FreqCount :
    def __init__(self, input_path: str, output_path: str, encoding = "utf-8") :
        self.input_path = input_path
        self.output_path = output_path
        self.encoding = encoding

        self.sentence_dic = {}
        self.eojeol_dic = {}
        self.emjeol_dic = {}
        self.morph_dic = {}

    ##############################################################################

    def load_folder(self) :
        for filename in os.listdir(self.input_path) :
            file_path = os.path.join(self.input_path, filename)
            self.load_file(file_path)

    def load_file(self, file_path: str) :
        with open(file_path, 'r', encoding = self.encoding) as file :
            while 1 :
                line = file.readline()
                if not line :
                    break

                line = line.strip()
                if len(line) == 0 :
                    continue

                if line[:3] == "#%#" :
                    sentence = line[3:].strip()
                    eojeol = sentence.split()
                    emjeol = [i for i in list(sentence) if i.strip()]

                    self.make_dic(self.sentence_dic, [sentence])
                    self.make_dic(self.eojeol_dic, eojeol)
                    self.make_dic(self.emjeol_dic, emjeol)

                else :
                    line = line.split()

                    morph_list = [i for i in line[1:] if i.replace('+', '')]

                    for morph in morph_list :
                        morph = morph.rsplit("/", 1)
                        self.make_morph_dic(morph)

    ##############################################################################

    def make_dic(self, dic: dict, key: list) :
        for i in key :
            if i in dic.keys() :
                dic[i] += 1
            else :
                dic[i] = 1

    def make_morph_dic(self, morph: list) :
        lex, tag = morph[0], morph[1]

        if tag in self.morph_dic.keys() :
            if lex in self.morph_dic[tag].keys() :
                self.morph_dic[tag][lex] += 1
            else :
                self.morph_dic[tag][lex] = 1
        else :
            self.morph_dic[tag] = {}
            self.morph_dic[tag][lex] = 1

    ##############################################################################

    def make_file_path(self) :
        sentence_freq_file_path = self.output_path + '/' + "sentence_freq.map"
        eojeol_freq_file_path = self.output_path + '/' + "eojeol_freq.map"
        emjeol_freq_file_path = self.output_path + '/' + "emjeol_freq.map"
        morph_freq_folder_path = self.output_path + '/' + "morph_tag_lex_freq"

        self.create_folder(self.output_path)
        self.create_folder(morph_freq_folder_path)

        self.write_dic(sentence_freq_file_path, self.sentence_dic, True)
        self.write_dic(eojeol_freq_file_path, self.eojeol_dic, True)
        self.write_dic(emjeol_freq_file_path, self.emjeol_dic, True)

        for tag in self.morph_dic.keys() :
            tag_lex_file_path = f'{morph_freq_folder_path}/{tag}_lex_freq.map'
            self.write_dic(tag_lex_file_path, self.morph_dic[tag], True)

    def write_dic(self, path: str, dic: dict, sort_desc: bool) :
        with open(path, 'w', encoding = self.encoding) as file :
            dic = self.sort_dic(dic, sort_desc)

            for key, value in dic.items() :
                file.write(f'{key}\t{value}\n')

    ##############################################################################

    def sort_dic(self, dic: dict, sort_desc = True) -> dict :
            return dict(sorted(dict(sorted(dic.items())).items(), key = lambda x : x[1], reverse = sort_desc))

    def create_folder(self, dir: str):
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except OSError:
            print ('Error: Creating directory. ' +  dir)


##################################################################################

if __name__ == "__main__" :
    input_path = "***********************"
    output_path = "***********************"
    encoding = "utf-8"

    freq = FreqCount(input_path, output_path, encoding)
    freq.load_folder()
    freq.make_file_path()