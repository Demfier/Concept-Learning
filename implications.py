# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 23:20 15th January, 2018

Implements the implication related methods for a given context.
"""


class Implication(object):
    """
    An Implication consists of two sets: *premise* and *conclusion*

    Examples
    ========

    >>> imp = Implication(set(('a', 'b',)), set(('c',)))
    >>> imp
    a, b => c
    >>> print imp
    a, b => c
    >>> imp.is_respected(set(('a', 'b',)))
    False
    >>> imp.is_respected(set(('a', 'b', 'd')))
    False
    >>> imp.is_respected(set(('a', 'b', 'c',)))
    True
    >>> imp.is_respected(set(('a', 'c',)))
    True
    >>> imp.is_respected(set(('b')))
    True
    >>> imp.is_respected(set(('c')))
    True
    """

    def __init__(self, premise_=frozenset(), conclusion_=frozenset()):
        """
        Create implication from two sets of attributes
        """
        self.premise = premise_
        self.conclusion = conclusion_

    def __deepcopy__(self, memo):
        return Implication(self.premise.copy(), self.conclusion.copy())

    def get_premise(self):
        """
        Return premise of implication
        """
        return self.premise

    def get_conclusion(self):
        """
        Return conclusion of implication
        """
        return self.conclusion

    def get_reduced_conclusion(self):
        return self.conclusion - self.premise

    def __repr__(self):
        try:
            premise = ", ".join([element for element in self.premise])
            short_conclusion = self.conclusion - self.premise
            conclusion = ", ".join([element for element in short_conclusion])
        except BaseException:
            premise = ", ".join([str(element) for element in self.premise])
            short_conclusion = self.conclusion - self.premise
            conclusion = ", ".join([str(element)
                                    for element in short_conclusion])
        return " => ".join((premise, conclusion,))

    def __unicode__(self):
        return self.__repr__()

    def __cmp__(self, other):
        if ((self.premise == other.premise) and
                (self.conclusion == other.conclusion)):
            return 0
        else:
            return -1

    def __hash__(self):
        return hash(frozenset((frozenset(self.premise),
                               frozenset(self.conclusion))))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return(self.premise == other.premise and
               self.conclusion == other.conclusion)

    def is_respected(self, some_set):
        """Checks whether implication repects `some_set or not.
        In other words, is `some_set` a model of implication?"""
        # if some_set contains every element from premise and not every
        # element from conclusion then it doesn't respect an implication
        # TODO: refactor
        if isinstance(some_set, set):
            return(self.conclusion.issubset(some_set) or not
                   self.premise.issubset(some_set))
        else:
            # Assume a partial example
            return (self.conclusion.issubset(some_set[1]) or
                    not self.premise.issubset(some_set[0]))


def findSpecialImplication(implications, membership_oracle,
                           closure_operator, counter_example):
    """Returns first implication (A --> B) such that it's premise(A)
    is not a subset of counter_example(C) and
    member(C ∩ A) is false. The latter condition can also be interpreted as
    C ∩ A is not a model of context(K).
    """
    for implication in implications:
        if counter_example.intersection(implication.premise) \
           != implication.premise and not membership_oracle(
                counter_example.intersection(implication.premise),
                closure_operator):
            return implication
    return None


def is_respected(implications, some_set):
    """Checks where some_set respects a set of implications
    """
    for impl in implications:
        if not impl.is_respected(some_set):
            return False
        else:
            continue
    return True
