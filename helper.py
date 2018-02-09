# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 23:20 15th January, 2018

Implements some helper methods used in the module.
"""

from itertools import chain, combinations


def powerset(iterable):
    """Taken from itertools recipes -->
       https://docs.python.org/3/library/itertools.html#recipes"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))
