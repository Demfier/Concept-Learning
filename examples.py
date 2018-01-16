"""
Author: Gaurav Sahu, 10:00 16th January, 2018

Contains usage examples for the contexts module.

1. Given a list of object-attribute relations,
    - compute formal concepts
    - compute intent and extent
    - generate concept-lattice from concepts
"""

import fca

if __name__ == '__main__':
    # a simple object-attribute relation illustration using toy-example of
    # Star Alliance Airlines data mapping airlines with their destinations

    relation = []
    # Air Canada relation
    relation += [('Air Canada', 'Latin America'), ('Air Canada', 'Europe'),
                 ('Air Canada', 'Canada'), ('Air Canada', 'Asia Pacific'),
                 ('Air Canada', 'Middle East'), ('Air Canada', 'Africa'),
                 ('Air Canada', 'Mexico'), ('Air Canada', 'Caribbean'),
                 ('Air Canada', 'United States')]
    # Air New zealand relation
    relation += [('Air New Zealand', 'Europe'),
                 ('Air New Zealand', 'Asia Pacific'),
                 ('Air New Zealand', 'United States')]
    # All Nippon Airways relation
    relation += [('All Nippon Airways', 'Europe'),
                 ('All Nippon Airways', 'Asia Pacific'),
                 ('All Nippon Airways', 'United States')]
    # Ansett Australia relation
    relation += [('Ansett Australia', 'Asia Pacific')]
    # The Australian Airlines Group
    relation += [('The Austrian Airlines Group', 'Europe'),
                 ('The Austrian Airlines Group', 'Canada'),
                 ('The Austrian Airlines Group', 'Asia Pacific'),
                 ('The Austrian Airlines Group', 'Middle East'),
                 ('The Austrian Airlines Group', 'Africa'),
                 ('The Austrian Airlines Group', 'United States')]
    # British Midland relation
    relation += [('British Midland', 'Europe')]
    # Lufthansa relation
    relation += [('Lufthansa', 'Latin America '), ('Lufthansa', 'Europe'),
                 ('Lufthansa', 'Canada'), ('Lufthansa', 'Asia Pacific'),
                 ('Lufthansa', 'Middle East'), ('Lufthansa', 'Africa'),
                 ('Lufthansa', 'Mexico'), ('Lufthansa', 'United States')]
    # Mexicana relation
    relation += [('Mexicana', 'Latin America'), ('Mexicana', 'Canada'),
                 ('Mexicana', 'Mexico'), ('Mexicana', 'Caribbean'),
                 ('Mexicana', 'United States')]
    # Scandinavian Airlines relation
    relation += [('Scandinavian Airlines', 'Latin America'),
                 ('Scandinavian Airlines', 'Europe'),
                 ('Scandinavian Airlines', 'Asia Pacific'),
                 ('Scandinavian Airlines', 'Africa'),
                 ('Scandinavian Airlines', 'United States')]
    # Singapore Airlines relation
    relation += [('Singapore Airlines', 'Europe'),
                 ('Singapore Airlines', 'Canada'),
                 ('Singapore Airlines', 'Asia Pacific'),
                 ('Singapore Airlines', 'Middle East'),
                 ('Singapore Airlines', 'Africa'),
                 ('Singapore Airlines', 'United States')]
    # Thai Airways International
    relation += [('Thai Airways International', 'Latin America'),
                 ('Thai Airways International', 'Europe'),
                 ('Thai Airways International', 'Asia Pacific'),
                 ('Thai Airways International', 'Caribbean'),
                 ('Thai Airways International', 'United States')]
    # United Airlines relation
    relation += [('United Airlines', 'Latin America'),
                 ('United Airlines', 'Europe'),
                 ('United Airlines', 'Canada'),
                 ('United Airlines', 'Asia Pacific'),
                 ('United Airlines', 'Mexico'),
                 ('United Airlines', 'Caribbean'),
                 ('United Airlines', 'United States')]
    # VARIG relation
    relation += [('VARIG', 'Latin America'), ('VARIG', 'Europe'),
                 ('VARIG', 'Asia Pacific'), ('VARIG', 'Africa'),
                 ('VARIG', 'Mexico'), ('VARIG', 'United States')]

    concepts = fca.formalConcepts(relation)
    concepts.computeLattice()
    print("Star Alliance Airlines example")
    print(concepts)
    print

    # write to a dot file
    # Note: use linux command dot starAlliance.dot -Tpng -o starAlliance.png
    # to convert the dot file to png
    dotfile = open('starAlliance.dot', "w")
    concepts.dotPrint(dotfile)
    dotfile.close()
