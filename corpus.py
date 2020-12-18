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
import os
import json
from nltk.tokenize.toktok import ToktokTokenizer
from pair import *

class Corpus(object):

    def __init__(self):
        self._toktok = ToktokTokenizer()

    def _get_tokenized_sentence(self, sentence):
        return self._toktok.tokenize(sentence)        

    '''
        Returns a dictionary with word, sentences
    '''
    def _select_sentences_with_diacritics(self, filename, diacritics):
        logging.debug("_select_sentences_with_diacritics")

        diacritics_sentences = {}
        SHORT_SENTENCE = 10
        with open(filename, "r") as source:
            while True:
                src = source.readline().lower()

                if not src:
                    break
            
                words = self._get_tokenized_sentence(src)
                for word in words:
                    if word not in diacritics:
                        continue

                    if len(words) < SHORT_SENTENCE:
                        continue

                    if word in diacritics_sentences:
                        sentences = diacritics_sentences[word]
                    else:
                        sentences = []

                    if len(sentences) < 10 and src not in sentences:
                        sentences.append(src)
                        diacritics_sentences[word] = sentences

        for diacritic in diacritics_sentences.keys():
            sentences = diacritics_sentences[diacritic]
            logging.debug(f"{diacritic}")
            #for sentence in sentences:
            #    logging.debug(f"  {sentence}")
                

        return diacritics_sentences


    def get_dictionaries_frequencies_and_sentences(self, corpus, pairs):
        logging.debug("set_dictionaries_frequencies_and_sentences")

        diacritics, no_diacritics = get_words_dictionaries(pairs)

        lines = 0
        words_in_corpus = 0
        with open(corpus, "r") as source:
            while True:

                src = source.readline().lower()

                if not src:
                    break

                lines = lines + 1
                words = self._get_tokenized_sentence(src)
                words_in_corpus += len(words)

                for word in words:
                    if word in diacritics:
                        frequency = diacritics[word]
                        diacritics[word] = frequency + 1

                        pair = pairs[word]
                        if len(pair.diacritic.sentences) < 10 and src not in pair.diacritic.sentences:
                            pair.diacritic.sentences.append(src)

                    if word in no_diacritics:
                        frequency = no_diacritics[word]
                        no_diacritics[word] = frequency + 1

        logging.info(f"Read corpus {corpus}, lines {lines}, words {words_in_corpus}")
        return diacritics, no_diacritics

