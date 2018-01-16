# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 14:59 16th January, 2018

Implements Query class containing queries to be used for PAC-Learning
For more information, see:
 - D. Angluin: Queries and Concept Learning, 1988
 - D. Borchmann, T. Hanika and S. Obiedkov: On the Usability of Probabaly
   Correct Implication Bases, 2017
"""

import random


class Query(object):
    """Contains the six type of queries used in PAC"""
    def __init__(self, _input):
        self._input = _input
        self.targetHypothesis = []  # Find out what this target should be

    def member(self):
        """
        Tells if the given element is present in the target hypothesis
        """
        # _input ∈ targetHypothesis
        return(self._input in self.targetHypothesis)

    def equivalent(self, restricted=False):
        """Will tell if the input set is equivalent to the target hypothesis"""
        if !isinstance(self._input, set):
            print "Input must be a set for the equivalence query"
        else:
            if self._input == self.targetHypothesis:
                return {'bool': True, 'counter_example': None}
            else:
                # counter_example ∈ _input △ targetHypothesis
                return({'bool': False, 'counter_example':
                        random.choice(list(
                            self._input.symmetric_difference(
                                self.targetHypothesis)))})

    def subset(self, restricted=False):
        print "Yet to implement"

    def superset(self, restricted=False):
        print "Yet to implement"

    def disjoint(self, restricted=False):
        print "Yet to implement"

    def exhaustive(self, restricted=False):
        print "Yet to implement"
