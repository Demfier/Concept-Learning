# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 18:56 18th March, 2018

Code to learn regex for each of the implication clusters
"""
import os
import operator
import _pickle as pickle

PAC_DIR = 'data/out/pac/'
REGEX_DIR = 'data/out/regex/'


def deterministicRegexLearning(cluster):
    """
    Inspired by the Algorithm 1 discussed in:
        > Algorithms for Learning Regular Expressions, Henning Fernau

    Approach: Transforms words into blocks and aligns them to form a regex
    """

    # Build block stream from the cluster of words
    # block_stream contains each word in `blocked` form
    block_stream = []
    for word in cluster:
        blocks = []
        block = ''
        for char in word:
            if block == '':
                block += char
            else:
                if block[-1] == char:
                    block += char
                else:
                    blocks.append(block)
                    block = char
        else:
            blocks.append(block)
        block_stream.append(blocks)

    block_stream = sorted(block_stream, key=len)
    max_len = len(block_stream[-1])
    # At these indexes, a block inside another block would start
    combine_indexes = list(set([len(block) for block in block_stream]))
    # Align the blocks and build regex
    regexp = ''
    # TODO: Complete this part


def extract_prefixes(word):
    """
    Extracts all possible prefixes possible for a word
    """
    return([word[:i + 1] for i in range(len(word))])


def extract_suffixes(word):
    """
    Extracts all possible suffixes possible for a word
    """
    return([word[-i - 1:] for i in range(len(word))])


def naiveRegexLearning(cluster):
    """
    Assuming a word is made up of two parts: prefix and suffix
    We find the top `n` most occuring prefixes and suffixes

    So the regex for a cluster would be ^prefix*suffix$
    """
    prefix_dict = dict()
    suffix_dict = dict()
    for word in cluster:
        for prefix in extract_prefixes(word):
            try:
                prefix_dict[prefix] += 1
            except KeyError:
                prefix_dict[prefix] = 1

        for suffix in extract_suffixes(word):
            try:
                suffix_dict[suffix] += 1
            except KeyError:
                suffix_dict[suffix] = 1

    # convert count --> percent
    prefix_count_sum = sum(prefix_dict.values())
    suffix_count_sum = sum(suffix_dict.values())
    prefix_dict = dict((k, float(v/prefix_count_sum)) for k, v in prefix_dict.items())
    suffix_dict = dict((k, float(v/suffix_count_sum)) for k, v in suffix_dict.items())

    # sort the prefix and suffix dicts by value
    prefix_dict = sorted(prefix_dict.items(), key=operator.itemgetter(1), reverse=True)[:4]
    suffix_dict = sorted(suffix_dict.items(), key=operator.itemgetter(1), reverse=True)[:4]
    return(prefix_dict, suffix_dict)


def learnRegexForAllPacBases(pac_files):
    no_regex = []
    for pac_file in pac_files:
        pac_data = pickle.load(open(PAC_DIR + pac_file, 'rb'))
        try:
            pac_basis = pac_data[2]
        except IndexError:
            no_regex.append(pac_file)
            continue
        implId_map = pac_data[3]
        for idx, implication in enumerate(pac_basis):
            regex = naiveRegexLearning(implication.conclusion)
            implId_map[idx] = {'opn_seq': implId_map[idx],
                               'regex': regex}

        with open(REGEX_DIR + pac_file, 'wb') as regex_out:
            pickle.dump(implId_map, regex_out)

if __name__ == '__main__':
    learnRegexForAllPacBases(os.listdir(PAC_DIR))
