# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 14:59 16th January, 2018

Implements the six types of oracles to be used for PAC-Learning
For more information, see:
 - D. Angluin: Queries and Concept Learning, 1988
 - D. Borchmann, T. Hanika and S. Obiedkov: On the Usability of Probabaly
   Correct Implication Bases, 2017
"""

import random
import math
import implications as imp


def member(_input_set, closure_operator):
    """
    Tells if the given element is present in the target hypothesis
    """
    # _input ∈ targetHypothesis
    return(_input_set == set(closure_operator(_input_set)))


def equivalent(_input_set, formal_concept, membership_oracle,
               closure_operator, restricted=False):
    """Will tell if the input set is equivalent to the intents of the
    context or not. If not, returns a counter-example.
    Here _input_set (H) is a set of implications of the form A --> B,
    context_intents = Int(K)"""
    if not isinstance(_input_set, set):
        print("Inputs must be a set for the equivalence query")
    else:
        # input = intents
        for i in range(pow(2, len(formal_concept.context.attributes))):
            # sample potential_counter_example => set(['b', 'd'])
            potential_counter_example = genCounterExample(formal_concept)
            is_member = membership_oracle(potential_counter_example,
                                          closure_operator)
            respects = imp.is_respected(_input_set, potential_counter_example)
            if ((is_member and not respects) or (not is_member and respects)):
                return {'bool': False, 'value': potential_counter_example}
        return {'bool': True, 'value': None}


def approx_equivalent(_input_set, membership_oracle, formal_concept,
                      closure_operator, i, epsilon=0.1, delta=0.1):
    # input = intents
    l_i = math.floor((i - math.log(delta, 2)) / epsilon)
    for i in range(int(l_i)):
        sample = genCounterExample(formal_concept)
        is_member = membership_oracle(sample, closure_operator)
        respects = imp.is_respected(_input_set, sample)
        if ((is_member and not respects) or (not is_member and respects)):
            return {'bool': False, 'value': sample}
    return {'bool': True, 'value': None}


def subset(restricted=False):
    """Will tell if the input is a subset of the target hypothesis"""
    if not isinstance(_input, set):
        print("Input must be a set for the subset query")
    else:
        # _input ⊆ targetHypothesis
        if _input.issubset(targetHypothesis):
            return {'bool': True, 'value': None}
        else:
            return {'bool': False, 'value': random.choice(list(
                _input.difference(targetHypothesis)))}


def superset(restricted=False):
    """Will tell if the input is a superset of the target hypothesis"""
    if not isinstance(_input, set):
        print("Input must be a set for the superset query")
    else:
        # _input ⊇ targetHypothesis
        if _input.issuperset(targetHypothesis):
            return {'bool': True, 'value': None}
        else:
            return {'bool': False, 'value': random.choice(list(
                targetHypothesis.difference(_input)))}


def disjoint(restricted=False):
    """Will tell if the input is disjoint from target hypothesis"""
    if not isinstance(_input, set):
        print("Input must be a set for the disjointness query")
    else:
        # _input ∩ targetHyothesis = ϕ
        if _input.intersection(targetHypothesis) == set([]):
            return {'bool': True, 'value': None}
        else:
            return {'bool': False, 'value': random.choice(list(
                _input.intersection(targetHypothesis)))}


def exhaustive(restricted=False):
    print("`exaustive` method is still to be implemented")


def genCounterExample(formal_concept, oracle_type='equivalence'):
    """Leaving room for generating counter-examples for other types of
    oracles too"""
    if oracle_type == 'equivalence':
        attributes = formal_concept.context.attributes
        counter_example = set()
        for attr in attributes:
            if random.random() > 0.5:
                counter_example.add(attr)
        return counter_example
