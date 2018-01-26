# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 10:00 16th January, 2018

Contains usage examples for the contexts module.

1. Given a list of object-attribute relations,
    - compute formal concepts
    - compute intent and extent
    - generate concept-lattice from concepts
"""

import concept_context as cnct
import time

if __name__ == '__main__':
    # a simple object-attribute relation illustration using toy-example of
    # Star Alliance Airlines data mapping airlines with their destinations

    relation = []
    # Air Canada relation
    relation += [('T1', 'b'), ('T1', 'd')]
    # Air New zealand relation
    relation += [('T2', 'b'), ('T2', 'e')]
    relation += [('T3', 'c')]
    relation += [('T4', 'a'), ('T4', 'b'), ('T4', 'c')]
    relation += [('T5', 'd')]
    relation += [('T6', 'b'), ('T6', 'c')]
    relation += [('T7', 'e')]

    concepts = cnct.formalConcepts(relation)
    start = time.clock()
    concepts.computeLattice()
    print("Star Alliance Airlines example")
    print(concepts)
    concepts.computeCanonicalBasis()
    print(concepts.canonical_basis)
    print(time.clock() - start)
    # write to a dot file
    # Note: use linux command dot starAlliance.dot -Tpng -o starAlliance.png
    # to convert the dot file to png
    dotfile = open('starAlliance_2.dot', "w")
    concepts.dotPrint(dotfile)
    dotfile.close()
