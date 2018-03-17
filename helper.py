# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 23:20 15th January, 2018

Implements some helper methods used in the module.
"""

import re
import string
import operator
from itertools import chain, combinations


def lcs(s1, s2):
    """
    Iterative longest continuous sequence. No one character matchings
    Inputs: string 1 (s1) and string 2 (s2)
    Output: lcs
    """
    longest = ""
    i = 0
    for x in s1:
        # Use re.escape to avoid errors if while cards are present in the query
        if re.search(re.compile(re.escape(x)), s2):
            s = x
            while re.search(re.compile(re.escape(s)), s2):
                if len(s) > len(longest):
                    longest = s
                if i+len(s) == len(s1):
                    break
                s = s1[i:i+len(s)+1]
            i += 1
    return longest


def iterLCS(pdf):
    """
    Input: pdf (pandas dataframe) having 'source' and 'target' columns
    """
    sw1 = pdf['source']
    sw2 = pdf['target']
    longList = []
    while True:
        tempVal = lcs(sw1, sw2)
        if len(tempVal) <= 1:
            break

        longList.append(tempVal)
        sw1 = sw1.replace(tempVal, '#', 1)
        sw2 = sw2.replace(tempVal, '!', 1)
    pdf['common'] = longList
    pdf['deleted'] = [item for item in sw1.split('#') if len(item) > 0]

    if len(pdf['deleted']) == 0:
        pdf['deleted'] = ['']

    pdf['added'] = [item for item in sw2.split('!') if len(item) > 0]

    if len(pdf['added']) == 0:
        pdf['added'] = ['']
    return pdf


def powerset(iterable):
    """
    Taken from itertools recipes -->
    https://docs.python.org/3/library/itertools.html#recipes
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def build_relations(data):
    """
    Build attribute -- object (source-word -- operation) relations from
    processed training data denote ::operation for delete operations.
    For eg. ::ना shows delete ना
    """
    relations = []
    data['deleted'] = data['deleted'].apply(
        lambda opns: ['::' + opn for opn in opns])
    for i, r in data.iterrows():
        attr = r['source']
        objects = r['deleted'] + r['added']
        for obj in objects:
            relations.append((obj, attr))
    return relations


def operation(dataframe):
    """Returns the most common operation sequence in the dataframe"""
    counter = {}
    for i, r in dataframe.iterrows():
        opn_seq = ' '.join(r['deleted'] + r['added'])
        try:
            counter[opn_seq] += 1
        except KeyError:
            counter[opn_seq] = 1
    return max(counter.items(), key=operator.itemgetter(1))[0]


def apply_operation(operation_sequence, word):
    """Applies operation sequence on the word"""
    for opn in operation_sequence:
        if opn.startswith('::'):
            # delete operation
            opn = opn[2:]
            if opn == '':
                continue
            else:
                word = delete(opn, word)
        else:
            # insert operation
            word = insert(opn, word)
    return word


def delete(old, word, new='', occurrence=1):
    """Removes to_delete from the word"""
    li = word.rsplit(old, occurrence)
    return(new.join(li))


def insert(to_insert, word):
    """Appends to_insert to the word"""
    return(word + to_insert)
