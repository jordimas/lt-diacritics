#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import logging
from pair import Word, Pair
from cleandiacritics import *

class Dictionary(object):

    def __init__(self):
        self.words = list()

    def load_dictionary(self):

        input_file = 'diccionari.txt'
        WORD = 0
        LEMA = 1
        POS = 2

        duplicated = set()
        with open(input_file) as f:
            while True:
                line = f.readline()
                if not line:
                    break

                components = line.split()
                _word = components[WORD].lower()

                if _word in duplicated:
                    continue
        
                duplicated.add(_word)

                lema =  components[LEMA].lower()
                pos = Word._convert_to_readable_pos(components[POS])
                word = Word(_word, lema, pos)
                self.words.append(word)

        logging.debug(f"Words load from dictionary {len(self.words)}")


    def get_pairs(self):
        word_to_wordsobj = {}
        pairs = {}
        for word in self.words:
            word_to_wordsobj[word.word] = word

        for word in self.words:
            no_diatricic_word = get_clean_diacritic(word.word)
            if no_diatricic_word == word.word:
                continue

            if no_diatricic_word not in word_to_wordsobj:
                continue

            no_diacritic = word_to_wordsobj[no_diatricic_word]

            pair = Pair(word, no_diacritic)
            logging.debug(f"{word.word} - {word.pos}, {no_diacritic.word} - {no_diacritic.pos}")
            pairs[word.word] = pair

        return pairs
