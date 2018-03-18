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


def calculateAndSavePacBasis(train_dir, test_dir, filter_pac=True):
    """
    Parameters:
    -----------------
    train_dir (Str): Path to the training file
    test_dir (Str): Path to the testing file
    """

    # Load training and testing data into a dataframe
    train_data = pd.read_csv(train_dir, sep='\t', names=['source', 'target',
                                                         'pos_info'])
    uniq_rows = []
    for src in train_data['source'].unique():
        try:
            uniq_rows.append(train_data[train_data['source'] == src].iloc[0])
        except IndexError:
            continue
    train_data = pd.DataFrame.from_records(uniq_rows)
    test_data = pd.read_csv(test_dir, sep='\t', names=['source', 'target',
                                                       'pos_info'])

    attribute_size = train_data['source'].size

    test_data = pd.merge(train_data, test_data, how='inner', on=['source',
                                                                 'target'])
    test_data.dropna(inplace=True)
    common_words = test_data['source']

    if len(common_words) == 0:
        return(0, {})

    # process training data
    train_data = train_data.apply(helper.iterLCS, axis=1)

    relations = helper.build_relations(train_data)

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
        premise = train_data['source'].isin(impl.premise)
        premise_data = train_data[premise]
        implId_opnSeq_map[idx] = helper.operation(premise_data)

    word_map = {}
    correct = 0
    for word in common_words:
        # gt => Ground Truth
        word_map[word] = {
            'gt': test_data[test_data['source'] == word]['target'].iloc[0]}
        for idx, impl in enumerate(concepts.canonical_basis):
            # use conclusion as it contains elements of premise too
            if word in impl.conclusion:
                opn_seq = implId_opnSeq_map[idx].split(' ')
                output = helper.apply_operation(opn_seq, word)
                word_map[word]['pac_output'] = output
                if word_map[word]['gt'] == output:
                    correct += 1
                # stop at the first match as basis is sorted by premise length
                break
    accuracy = correct / float(len(common_words))
    return(accuracy, word_map, concepts.canonical_basis, implId_opnSeq_map)


def findAllPacBases(training_files, method='uncov_test', level='medium',
                    filter_pac=True, best_of=1, start_fresh=False):
    """
    Calculates and stores the best PAC-basis for each of the languages
    """
    if method == 'uncov_test':
        testing_files = os.listdir(UNCOV_TEST_DIR)
        # remove this file as it's `high` version training file doesn't exist
        if level == 'high':
            testing_files.remove('scottish-gaelic-uncovered-test')
    elif method == 'dev':
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

    # Accuracy mapping for a language. It stores accuracies for `best_of`
    # number of PAC-bases. This is required because we don't get the best
    # PAC-basis in one shot
    acc_wrdMap = {}
    for idx, train_file in enumerate(training_files):
        lang = train_file.split('/')[-1]
        if lang + '.p' in os.listdir(PAC_DIR) and not start_fresh:
            continue
        print('*********Finding best pac-basis for {}...**********'.format(lang))
        for i in range(best_of):
            try:
                acc_wrdMap[lang].append(calculateAndSavePacBasis(
                    TRAIN_DIR + train_file,
                    UNCOV_TEST_DIR + testing_files[idx],
                    filter_pac))
            except KeyError:
                acc_wrdMap[lang] = [calculateAndSavePacBasis(
                    TRAIN_DIR + train_file,
                    UNCOV_TEST_DIR + testing_files[idx],
                    filter_pac)]
        acc_wrdMap[lang] = max(acc_wrdMap[lang], key=operator.itemgetter(0))

        # Save the best pac-basis for all the languages along with accuracy
        # word-map found for exact matching
        with open(PAC_DIR + lang + '.p', 'wb') as pac_out:
            pickle.dump(acc_wrdMap[lang], pac_out)
            print('***********Saved best PAC-basis for {} with accuracy {}%!***********'.format(lang, acc_wrdMap[lang][0] * 100))

if __name__ == '__main__':
    findAllPacBases(
        os.listdir(TRAIN_DIR),
        method='uncov_test',
        level='high',
        filter_pac=False,
        best_of=5)
