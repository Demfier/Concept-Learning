# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 14:39 16th January, 2018

Contains methods needed for computing basis
"""

import implications as imp
import closure_operators
import oracle

import sys


def kclosure(s, k, cxt):
    """Return the closure of s in cxt restricted to the first k attributes."""
    closure = set(cxt.attributes[:k])
    for o in cxt.examples():
        if s == closure:
            break
        if s <= o:
            closure &= o
    return closure


# todo: optimize!
def compare_tuples(p, r):
    diff = p[1] ^ r[1]
    if diff:
        return 1 if sorted(diff)[0] in p[1] else -1
    else:
        return 0


def canonical_basis(cxt, close=closure_operators.simple_closure):
    preclosed = [(set(cxt.objects), set())]
    basis = []
    # each preclosed is (extent, intent) or (extent, premise, implication)
    # assuming that premise and implication.premise are the same object
    for i in range(len(cxt.attributes)):
        preclosed, basis = update_preclosed(i, cxt, preclosed, close)
    return basis


def update_preclosed(i, cxt, preclosed,
                     close=closure_operators.simple_closure):

    m = cxt.attributes[i]
    extent = cxt.get_attribute_extent_by_index(i)

    def context_closure(s): return kclosure(s, i + 1, cxt)

    old_stable_impl = []    # stores implications
    new_stable_impl = []    # stores implications
    min_mod_impl = []       # stores implications

    non_min_mod = []        # stores triples
    mod_extra = []          # stores pairs or triples

    new_preclosed = []

    for p in preclosed:
        if p[0] <= extent:  # p[1] -> m holds
            if is_concept(p):
                process_modified_concept(p, m, min_mod_impl, mod_extra,
                                         new_preclosed)
            else:
                process_modified_implication(p, m, min_mod_impl,
                                             non_min_mod,
                                             new_preclosed)
        else:               # p[1] -> m does not hold
            new_preclosed.append(p)
            if is_concept(p):       # p[1] remains closed
                process_stable_concept(p, m, extent, new_stable_impl,
                                       new_preclosed,
                                       context_closure)
            else:                   # p[1] remains pseudo-closed
                old_stable_impl.append(p[2])

    basis = old_stable_impl + new_stable_impl + min_mod_impl
    n = len(basis)
    basis += [p[2] for p in non_min_mod]
    for j in range(len(non_min_mod) - 1, -1, -1):
        impl = non_min_mod[j][2]
        del basis[n + j]
        premise = impl.premise
        premise |= close(premise, basis)    # sic! changing impl.premise
        if premise != impl.get_conclusion():
            basis.append(impl)
            mod_extra.append(non_min_mod[j])

    mod_extra.sort(cmp=compare_tuples)

    return new_preclosed + mod_extra, basis


def process_stable_concept(p, m, extent, new_stable_impl, new_preclosed,
                           closure):
    # p is of the form (extent, intent)
    new_extent = p[0] & extent
    new_premise = p[1].copy()
    new_premise.add(m)
    for i in new_stable_impl:
        if not i.is_respected(new_premise):
            break
    else:
        new_conclusion = closure(new_premise)
        if new_conclusion == new_premise:
            new_preclosed.append((new_extent, new_premise))
        else:
            impl = imp.Implication(new_premise, new_conclusion)
            new_stable_impl.append(impl)
            new_preclosed.append((new_extent, impl.premise, impl))


def process_modified_implication(p, m, min_mod_impl, non_min_mod,
                                 new_preclosed):
    # p is of the form (extent, premise, implication)
    p[2].get_conclusion().add(m)
    for i in min_mod_impl:
        if i.premise <= p[1]:   # p[1] is no longer preclosed
            p[1].add(m)         # assuming that p[1] is p[2].premise
            non_min_mod.append(p)
            break
    else:                       # p[1] remains psuedo-closed
        min_mod_impl.append(p[2])
        new_preclosed.append(p)


def process_modified_concept(p, m, min_mod_impl, mod_concepts, new_preclosed):
    # p is of the form (extent, intent)
    for i in min_mod_impl:
        if i.premise <= p[1]:   # p[1] is no longer preclosed
            break
    else:                       # p[1] becomes psuedo-closed
        impl = imp.Implication(p[1].copy(), p[1].copy())
        impl.get_conclusion().add(m)
        min_mod_impl.append(impl)
        new_preclosed.append((p[0], impl.premise, impl))
    p[1].add(m)
    mod_concepts.append(p)


def is_concept(p):
    return len(p) == 2


def generalizedComputeDgBasis(attributes, aclose,
                              close=closure_operators.simple_closure,
                              imp_basis=[],
                              cond=lambda x: True):
    """Computes the Duquenne-Guigues basis using optimized Ganter's algorithm.

    `aclose` is a closure operator on the set of attributes.
    """
    relative_basis = []

    a = close(set(), imp_basis)
    i = len(attributes)

    while len(a) < len(attributes):
        a_closed = set(aclose(a))
        if a != a_closed and cond(a):
            relative_basis.append(imp.Implication(a.copy(), a_closed.copy()))
        if (a_closed - a) & set(attributes[: i]):
            a -= set(attributes[i:])
        else:
            if len(a_closed) == len(attributes):
                return relative_basis
            a = a_closed
            i = len(attributes)
        for j in range(i - 1, -1, -1):
            m = attributes[j]
            if m in a:
                a.remove(m)
            else:
                b = close(a | set([m]), relative_basis + imp_basis)
                if not (b - a) & set(attributes[: j]):
                    a = b
                    i = j
                    break
    return relative_basis


def horn1(formal_concept, closure_operator, membership_oracle,
          equivalence_oracle=None):
    """Computes DG Basis for a given set of attributes using horn1 algorithm
    """
    hypothesis = set()
    # NOTE: counter_example is a set
    while True:
        # sample `hypothesis` => set([a, e, d => c, b])
        counter_example = equivalence_oracle(
            hypothesis,
            formal_concept,
            membership_oracle,
            closure_operator)
        # terminating condition
        if counter_example['value'] is None:
            break

        # starting edge case
        if len(hypothesis) == 0:
            hypothesis.add(imp.Implication(
                frozenset(counter_example['value']),
                frozenset(formal_concept.context.attributes)))
            continue

        for implication in hypothesis.copy():
            # if an implication doesn't repect the counter example,
            # modify it's conclusion (also called strengthening)
            if not implication.is_respected(counter_example['value']):
                hypothesis.remove(implication)
                hypothesis.add(imp.Implication(
                    frozenset(implication.premise),
                    frozenset(implication.conclusion.intersection(
                        counter_example['value']))))
            else:
                # special_implication (A --> B) is the first implication
                # such that it's premise(A) is not a subset of
                # counter_example(C) and member(C ∩ A) is false. The latter
                # condition can also be interpreted as C ∩ A is not a model
                # of context(K)
                special_implication = imp.findSpecialImplication(
                    hypothesis,
                    membership_oracle,
                    closure_operator,
                    counter_example['value'])
                if special_implication:
                    hypothesis.remove(special_implication)
                    hypothesis.add(imp.Implication(
                        frozenset(counter_example['value'].intersection(
                            special_implication.premise)),
                        frozenset(special_implication.conclusion.union(
                            special_implication.premise.difference(
                                counter_example['value'])))))
                else:
                    hypothesis.add(imp.Implication(
                        counter_example['value'],
                        set(formal_concept.context.attributes)))
    return hypothesis


def pac_basis(formal_concept, closure_operator, membership_oracle):
    hypothesis = set()
    # NOTE: counter_example is a set
    i = 0  # number of queries
    while True:
        counter_example = oracle.approx_equivalent(
            set(hypothesis), membership_oracle, formal_concept,
            closure_operator, i, 0.1, 0.1)

        if counter_example['value'] is None:
            break

        if len(hypothesis) == 0:
            hypothesis.add(imp.Implication(
                counter_example['value'],
                set(formal_concept.context.attributes)))
            continue

        i += 1
        for implication in hypothesis.copy():
            # if an implication doesn't repect the counter example,
            # modify it's conclusion (also called strengthening)
            if not implication.is_respected(counter_example['value']):
                hypothesis.remove(implication)
                hypothesis.add(imp.Implication(
                    implication.premise,
                    implication.conclusion.intersection(
                        counter_example['value'])))
            else:
                # special_implication (A --> B) is the first implication
                # such that it's premise(A) is not a subset of
                # counter_example(C) and member(C ∩ A) is false. The latter
                # condition can also be interpreted as C ∩ A is not a model
                # of context(K)
                special_implication = imp.findSpecialImplication(
                    hypothesis,
                    membership_oracle,
                    closure_operator,
                    counter_example['value'])
                if special_implication:
                    hypothesis.remove(special_implication)
                    hypothesis.add(imp.Implication(
                        counter_example['value'].intersection(
                            special_implication.premise),
                        special_implication.conclusion.union(
                            special_implication.premise.difference(
                                counter_example['value']))))
                else:
                    hypothesis.add(imp.Implication(
                        counter_example['value'],
                        set(formal_concept.context.attributes)))
    return hypothesis
