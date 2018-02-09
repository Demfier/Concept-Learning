# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 23:20 15th January, 2018

Implements some helper methods used in the module.
"""

import re
import string
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
        if re.search(x, s2):
            s = x
            while re.search(s, s2):
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
