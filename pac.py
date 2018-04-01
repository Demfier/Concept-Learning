# -*- coding: utf-8 -*-
"""
Author: Gaurav Sahu, 23:05 23th January, 2018

Calcuates PAC-basis for a given training data and stores it
For more information, see:
 - D. Angluin: Queries and Concept Learning, 1988
 - D. Borchmann, T. Hanika and S. Obiedkov: On the Usability of Probabaly
   Correct Implication Bases, 2017
"""

# required to dump formalConcepts class's object which contains a lambda
# function

import os
import sys
import copy
import helper
import operator
import _pickle as pickle
import pandas as pd
import concept_context as cn

TRAIN_DIR = 'data/train/'
DEV_DIR = 'data/dev/'
COV_TEST_DIR = 'data/test/covered/'
UNCOV_TEST_DIR = 'data/test/uncovered/'
PAC_DIR = 'data/out/pac/'


def calculateAndSavePacBasis(train_dir, filter_pac=True):
    """
    Parameters:
    -----------------
    train_dir (Str): Path to the training file
    test_dir (Str): Path to the testing file
    """

    # Load training and testing data into a dataframe
    pac_per_pos = dict()
    train_data = pd.read_csv(train_dir, sep='\t', names=['source', 'target',
                                                         'pos_info'])

    uniq_pos_list = train_data['pos_info'].unique()
    uniq_pos = set()
    for pos_group in uniq_pos_list:
        for pos in pos_group.split(';'):
            uniq_pos.add(pos)
    for pos in uniq_pos:
        print("for pos ==> {}".format(pos))
        temp_train_data = []
        for row in train_data.iterrows():
            if pos in row[1]['pos_info'].split(';'):
                temp_train_data.append(row[1])
            else:
                continue
        temp_train_data = pd.DataFrame.from_records(temp_train_data)

        attribute_size = temp_train_data['source'].size

        # process training data
        temp_train_data = temp_train_data.apply(helper.iterLCS, axis=1)

        relations = helper.build_relations(temp_train_data)

        # Build the concept lattice
        concepts = cn.formalConcepts(relations)
        concepts.computeLattice()

        # Find canonical basis
        concepts.computeCanonicalBasis(epsilon=0.1, delta=0.1, basis_type='pac')

        print("Total implications: {}\n".format(len(concepts.canonical_basis)))

        unique_conclusions = []
        for impl in copy.deepcopy(concepts.canonical_basis):
            if len(impl.premise) == 0:
                concepts.canonical_basis.remove(impl)
            if filter_pac:
                # Remove implications of the form C --> M and C --> C
                if impl.premise == impl.conclusion or len(
                        impl.conclusion) == attribute_size:
                    concepts.canonical_basis.remove(impl)
            unique_conclusions.append(frozenset(impl.conclusion))

        print("Total UNIQUE conclusions: {}\n".format(len(set(unique_conclusions))))
        concepts.canonical_basis = set(
            sorted(
                list(
                    concepts.canonical_basis),
                reverse=True))

        implId_opnSeq_map = {}
        for idx, impl in enumerate(concepts.canonical_basis):
            premise = temp_train_data['source'].isin(impl.premise)
            premise_data = temp_train_data[premise]
            implId_opnSeq_map[idx] = helper.operation(premise_data)

        pac_per_pos[pos] = (concepts.canonical_basis, implId_opnSeq_map)
    return pac_per_pos


def findAllPacBases(training_files, method='uncov_test', level='medium',
                    filter_pac=True, start_fresh=False):
    """
    Calculates and stores the best PAC-basis per POS config per language
    """
    if method == 'uncov_test':
        testing_files = os.listdir(UNCOV_TEST_DIR)
        test_dir = UNCOV_TEST_DIR
        # remove this file as it's `high` version training file doesn't exist
        if level == 'high':
            testing_files.remove('scottish-gaelic-uncovered-test')
    elif method == 'dev':
        test_dir = DEV_DIR
        testing_files = os.listdir(DEV_DIR)
        if level == 'high':
            testing_files.remove('scottish-gaelic-dev')

    for file in copy.copy(training_files):
        if not file.endswith(level):
            training_files.remove(file)

    training_files = sorted(training_files)
    testing_files = sorted(testing_files)
    assert len(training_files) == len(testing_files)
    # sort the list so that trainig and testing files are aligned

    acc_wrdMap = {}
    for idx, train_file in enumerate(training_files):
        lang = train_file.split('/')[-1]
        # if lang + '.p' in os.listdir(PAC_DIR) and not start_fresh:
        #     continue
        print('*********Finding best pac-basis for {}...**********'.format(lang))
        pac_per_pos = calculateAndSavePacBasis(
            TRAIN_DIR + train_file,
            filter_pac)
        try:
            for pos in pac_per_pos:
                acc_wrdMap[lang][pos].append(pac_per_pos[pos])
        except KeyError:
            acc_wrdMap[lang] = {pos: [pac_per_pos[pos]]}

        for pos in copy.deepcopy(acc_wrdMap[lang]):
            acc_wrdMap[lang][pos] = max(acc_wrdMap[lang][pos], key=operator.itemgetter(0))

        # Save the best pac-basis for all the languages along with accuracy
        # word-map found for exact matching
        for pos in acc_wrdMap[lang]:
            print('***********Saved best PAC-basis for {} at POS {} with accuracy {}%!***********'.format(lang, pos, acc_wrdMap[lang][pos][0] * 100))
        # with open(PAC_DIR + lang + '.p', 'wb') as pac_out:
        #     pickle.dump(acc_wrdMap[lang], pac_out)

if __name__ == '__main__':
    findAllPacBases(
        os.listdir(TRAIN_DIR),
        method='dev',
        level='low',
        filter_pac=False)
