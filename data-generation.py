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
from pair import *
from cleandiacritics import *
from dictionary import Dictionary
from corpus import Corpus
import datetime
import operator

ERROR_NOT_DETECTED = 0
ERROR_DETECTED = 1
ERROR_NOT_INCORPUS = 2

_toktok = ToktokTokenizer()


def init_logging():
    logfile = 'data-generation.log'

    if os.path.isfile(logfile):
        os.remove(logfile)

    logging.basicConfig(filename=logfile, level=logging.DEBUG,
                        format='%(message)s')

    logger = logging.getLogger('')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)



def export_diacritics_with_no_rules(pairs):

    selected_pairs = []  

    for pair in pairs.values():
        diacritic = pair.diacritic
        no_diacritic = pair.no_diacritic

        if diacritic.detected != ERROR_DETECTED:
            continue

        frequency = no_diacritic.frequency * 100 / diacritic.frequency
        if frequency > 5: # 5%
            logging.debug(f"Discarted {diacritic.frequency} - {no_diacritic.frequency} - {frequency}")
            continue

        selected_pairs.append(pair)


    position = 0
    with open('diacritics-rules.csv', 'w') as writer:
        msg = f"diacritic_word\tdiacritic_pos\tdiacritic_freq\t"
        msg += f"no_diacritic_word\tno_diacritic_pos\tno_diacritic_freq\t"
        msg += f"cnt\n"
        writer.write(msg)

        sorted_pairs = sorted(selected_pairs, key=lambda x: x.diacritic.frequency, reverse=True)

        for pair in sorted_pairs:
            diacritic = pair.diacritic
            no_diacritic = pair.no_diacritic

            msg = f"{diacritic.word}\t{diacritic.pos}\t{diacritic.frequency}\t"
            msg += f"{no_diacritic.word}\t{no_diacritic.pos}\t{no_diacritic.frequency}\t{position}\n"
            position = position + 1
            writer.write(msg)
            


def analysis(corpus):
    dictionary = Dictionary()
    dictionary.load_dictionary()
    pairs = dictionary.get_pairs()

    diacritics, no_diacritics = Corpus().get_dictionaries_frequencies_and_sentences(corpus, pairs)
    update_pairs(pairs, diacritics, no_diacritics)

    diacritics_corpus = 0
    position = 0
    not_found_in_corpus_pos = {}
    with open('diacritics.csv', 'w') as writer:
        msg = f"diacritic_word\tdiacritic_pos\tdiacritic_freq\t"
        msg += f"no_diacritic_word\tno_diacritic_pos\tno_diacritic_freq\t"
        msg += f"total_freq\tcnt\n"

        writer.write(msg)
        for pair in pairs.values():
            diacritic = pair.diacritic
            no_diacritic = pair.no_diacritic

            if diacritic.frequency == 0 and no_diacritic.frequency == 0:
                logging.debug(f"Frequency 0: {diacritic.word}, {diacritic.pos}")
                pos = diacritic.pos
                if pos in not_found_in_corpus_pos:
                    counter = not_found_in_corpus_pos[pos]
                else:
                    counter = 0

                counter = counter + 1
                not_found_in_corpus_pos[pos] = counter
                continue

            total_freq = diacritic.frequency + no_diacritic.frequency

            msg = f"{diacritic.word}\t{diacritic.pos}\t{diacritic.frequency}\t"
            msg += f"{no_diacritic.word}\t{no_diacritic.pos}\t{no_diacritic.frequency}\t{total_freq}\t{position}\n"
            diacritics_corpus = diacritics_corpus + 1
            position = position + 1
            writer.write(msg)

    diacritics_dict = len(pairs)
    pdiacritics_dict = diacritics_dict * 100 / len(dictionary.words)
    pdiacritics_corpus = diacritics_corpus * 100 / diacritics_dict
    

    logging.info(f"Total unique words in dictionary: {len(dictionary.words)}")
    logging.info(f"Diacritic/no diacritic {diacritics_dict} ({pdiacritics_dict:.2f}%) (in dictionary)")
    logging.info(f"Diacritic/no diacritic {diacritics_corpus} ({pdiacritics_corpus:.2f}%) (in corpus)")


    len_pos = total = sum(int(v) for v in not_found_in_corpus_pos.values())
    for pos in not_found_in_corpus_pos:
        counter = not_found_in_corpus_pos[pos]
        pcounter = counter * 100 / len_pos
        logging.info(f"Not found in corpus, category {pos} - {counter}  ({pcounter:.2f}%)")

    return pairs



command = 'curl --data "language=ca-ES"  --data-urlencode "text@{0}" {1} > "{2}" 2>/dev/null'
server = 'http://172.17.0.2:7001/v2/check'

def run_lt(filename):
    matches = 0

    try:
        txt_file = filename + ".txt"
        json_file = filename + ".json"

        cmd = command.format(txt_file, server, json_file)
        os.system(cmd)

        with open(json_file) as f:
            data = json.load(f)
            matches = data['matches']
            matches = len(matches)

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
    
    except Exception as e:
        logging.error(e)

    return matches

def _remove_diacritic_sentence(sentence, diacritic):
    clean = get_clean_diacritic(diacritic)
    return sentence.replace(diacritic, clean)


def _write_debug_files(filename_diacritics, filename_nodiacritics, pair):

    try:
        diacritic = pair.diacritic.word
        sentences = pair.diacritic.sentences

        with open(filename_diacritics + ".txt", "w") as diac_writer, \
             open(filename_nodiacritics  + ".txt", "w") as nodiac_writer:
            for sentence in sentences[:5]:
                sentence_nodiac = _remove_diacritic_sentence(sentence, diacritic)
                nodiac_writer.write(sentence_nodiac + "\n")
                diac_writer.write(sentence + "\n")

    except Exception as e:
        logging.error(e)



def process_corpus(corpus, pairs):

    logging.info("process_corpus")
    cnt = 0

    writer = open('diacritics-lt.csv', 'w')
    msg = f"diacritic.word\tdiacritic_pos\tdiacritic_freq\t"
    msg += f"no_diacritic.word\tno_diacritic_pos\tno_diacritic_freq\t"
    msg += f"total_freq\tcnt\tdetected\n"
    writer.write(msg)


    position = 0    
    for pair in pairs.values():
        diacritic = pair.diacritic
        sentences = pair.diacritic.sentences
        no_diacritic = pair.no_diacritic
        logging.debug(f"{diacritic.word} - pos: {cnt} sentences: {len(sentences)}")

        if len(sentences)> 0:
            same_errors = 0
            cnt = cnt + 1

            name = get_clean_diacritic(diacritic.word)
            filename_diacritics = f'data/{name}_dia'
            filename_nodiacritics = f'data/{name}_nodia'
            _write_debug_files(filename_diacritics, filename_nodiacritics, pair)

            errors_diac = run_lt(filename_diacritics)
            errors_nodiac = run_lt(filename_nodiacritics)
            if errors_diac == errors_nodiac:
                detected = ERROR_NOT_DETECTED
            else:
                detected = ERROR_DETECTED
        else:
            detected = ERROR_NOT_INCORPUS
            errors_diac = errors_nodiac = 0
     
        diacritic.detected = detected
        total_freq = diacritic.frequency + no_diacritic.frequency
        msg = f"{diacritic.word}\t{diacritic.pos}\t{diacritic.frequency}\t"
        msg += f"{no_diacritic.word}\t{no_diacritic.pos}\t{no_diacritic.frequency}\t{total_freq}\t{position}\t"
        msg += f"{detected}\n"
        position = position + 1
        writer.write(msg)

        if detected != ERROR_DETECTED:
            print(f"*** {diacritic.word} {diacritic.frequency} - {no_diacritic.word} {no_diacritic.frequency}")
            for sentence in sentences[:10]:
                print("   " + sentence)

    writer.close()

    export_diacritics_with_no_rules(pairs)

def main():
    print("Generates diacritic data from dictionary.")
    CORPUS = "5000.txt"
#    CORPUS = "500000.txt"
#    CORPUS = "tgt-train.txt"
#    CORPUS = "ca_dedup.txt"

    start_time = datetime.datetime.now()

    init_logging()
    pairs = analysis(CORPUS)
    process_corpus(CORPUS, pairs)

    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    logging.info(s)

if __name__ == "__main__":
    main()
