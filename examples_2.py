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

    wines = []
    # Air Canada relation
    wines.append(('Trollinger', '15C'))
    wines.append(('Trollinger', '16C'))

    wines.append(('Beaujolais', '15C'))
    wines.append(('Beaujolais', '16C'))
    wines.append(('Beaujolais', '17C'))

    wines.append(('Burgundy', '15C'))
    wines.append(('Burgundy', '16C'))
    wines.append(('Burgundy', '17C'))
    wines.append(('Burgundy', '18C'))

    wines.append(('Bordeaux', '15C'))
    wines.append(('Bordeaux', '16C'))
    wines.append(('Bordeaux', '17C'))
    wines.append(('Bordeaux', '18C'))
    wines.append(('Bordeaux', '19C'))

    wines.append(('Barolo', '16C'))
    wines.append(('Barolo', '17C'))
    wines.append(('Barolo', '18C'))
    wines.append(('Barolo', '19C'))

    wines.append(('Barbera', '16C'))
    wines.append(('Barbera', '17C'))
    wines.append(('Barbera', '18C'))

    wines.append(('Brunello', '17C'))
    wines.append(('Brunello', '18C'))
    wines.append(('Brunello', '19C'))

    wines.append(('Negroamaro', '17C'))
    wines.append(('Negroamaro', '18C'))

    concepts = cnct.formalConcepts(wines)
    start = time.clock()
    concepts.computeLattice()
    print("Star Alliance Airlines example")
    print(concepts)
    concepts.computeCanonicalBasis(epsilon=0.5, delta=0.4)
    for impl in concepts.canonical_basis:
        print(impl)
    print(time.clock() - start)
    # write to a dot file
    # Note: use linux command dot starAlliance.dot -Tpng -o starAlliance.png
    # to convert the dot file to png
    # dotfile = open('wines.dot', "w")
    # concepts.dotPrint(dotfile)
    # dotfile.close()
