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
    return(sorted(_input_set) == closure_operator(_input_set))


def equivalent(_input_set, formal_concept, closure_operator, restricted=False):
    """Will tell if the input set is equivalent to the intents of the
    context or not. If not, returns a counter-example.
    Here _input_set (H) is a set of implications of the form A --> B,
    context_intents = Int(K)"""
    intents = [concept.intent for concept in formal_concept.concepts]
    intents = set(intents)
    if not isinstance(_input_set, set) or not isinstance(intents, set):
        print "Inputs must be a set for the equivalence query"
    else:
        # input = intents
        if _input_set == intents:
            return {'bool': True, 'value': None}
        else:
            # choose whether to return a +ve or -ve counter-example
            nature = random.choice([1, 0])
            return({'bool': False, 'value': genCounterExample(
                nature, formal_concept, _input_set, closure_operator,
                oracle_type='equivalence')})


def approx_equivalent(_input_set, membership_oracle, formal_concept,
                      closure_operator, i, epsilon=0.1, delta=0.1):
    return approx_equivalent_lambda(_input_set, membership_oracle,
                                    formal_concept, closure_operator,
                                    i, epsilon, delta)


def approx_equivalent_lambda(_input_set, membership_oracle,
                             formal_concept, closure_operator,
                             i, epsilon, delta):
    l_i = math.ceil((i - math.log(delta, 2)) / epsilon)
    context_attributes = formal_concept.context.attributes
    for j in range(int(l_i)):
        # random subset of attributes
        sample = set(random.sample(
                    context_attributes,
                    random.choice(range(len(context_attributes)))))
        if (membership_oracle(sample, closure_operator) and not imp.is_respected(_input_set, sample)) or\
           (not membership_oracle(sample, closure_operator) and imp.is_respected(_input_set, sample)):
            return {'bool': False, 'value': sample}
    return {'bool': True, 'value': None}


def subset(restricted=False):
    """Will tell if the input is a subset of the target hypothesis"""
    if not isinstance(_input, set):
        print "Input must be a set for the subset query"
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
        print "Input must be a set for the superset query"
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
        print "Input must be a set for the disjointness query"
    else:
        # _input ∩ targetHyothesis = ϕ
        if _input.intersection(targetHypothesis) == set([]):
            return {'bool': True, 'value': None}
        else:
            return {'bool': False, 'value': random.choice(list(
                _input.intersection(targetHypothesis)))}


def exhaustive(restricted=False):
    print("`exaustive` method is still to be implemented")


def genCounterExample(nature, formal_concept, _input_set,
                      closure_operator, oracle_type='equivalence'):
    """Leaving room for generating counter-examples for other types of
    oracles too"""
    if oracle_type == 'equivalence':
        intents = [concept.intent for concept in formal_concept.concepts]
        intents = set(intents)
        if nature:
            # generate positive counter-example
            # Such a counter-example C ⊆ Int(K)
            return set(random.sample(intents, random.choice(range(len(intents)))))
        else:
            # generate negative counter-example
            # Such a counter-example C is closed in H but not K
            context_attributes = formal_concept.context.attributes
            potential_counter_example = set()
            while True:
                potential_counter_example = set(random.sample(
                    context_attributes,
                    random.choice(range(len(context_attributes)))))
                # Check for negative counter example
                if closed_in_implication_set(
                    potential_counter_example, _input_set) and \
                    sorted(potential_counter_example) != \
                        closure_operator(potential_counter_example):
                        break
                else:
                    # Generate another counter example
                    continue
            return potential_counter_example
    return None


def closed_in_implication_set(counter_example, _input_set):
    for implication in _input_set:
        if not implication.premise.issubset(counter_example) or \
          implication.conclusion.issubset(counter_example):
            continue
        else:
            return False
    return True
