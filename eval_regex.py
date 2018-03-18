"""
Evaluation approach currently used in the script:

1. Take the words from test dataset present in the training data too
2. Find the approriate implication from the set of learnt implications
3. Apply the most common set of operation from the premise of appropriate impl.
4. Compare the resultant with the one given in test set.
"""

import os
import copy
import json
import helper
import operator
import pandas as pd
import _pickle as pickle
import concept_context as cn

DEV_DIR = 'data/dev/'
PAC_DIR = 'data/out/pac/'
TRAIN_DIR = 'data/train/'
EVAL_DIR = 'data/out/eval/'
REGEX_DIR = 'data/out/regex/'
COV_TEST_DIR = 'data/test/covered/'
UNCOV_TEST_DIR = 'data/test/uncovered/'


def evaluate(lang, test_dir):
    """
    Parameters:
    -----------------
    train_dir (Str): Path to the training file
    test_dir (Str): Path to the testing file
    """
    test_data = pd.read_csv(test_dir, sep='\t', names=['source', 'target',
                                                       'pos_info'])

    # if regex hasn't been learnt, the langauage can't be evaluated
    try:
        regex_data = pickle.load(open(REGEX_DIR + lang + '.p', 'rb'))
    except FileNotFoundError:
        return(None, None)

    pac_data = pickle.load(open(PAC_DIR + lang + '.p', 'rb'))
    pac_basis = pac_data[2]
    word_map = {}

    correct_guess = 0
    for test_word in test_data['source'].unique():
        word_map[test_word] = {'gt': test_data[test_data['source'] == test_word]['target'].iloc[0]}
        matched_cluster = []
        # identify cluster for the test_word
        for imp_id in regex_data:
            possible_suffixes = regex_data[imp_id]['regex'][1]
            for suffix, perc in possible_suffixes:
                if test_word.endswith(suffix):
                    matched_cluster.append((imp_id, suffix, perc))
                    continue
        if matched_cluster == []:
            matched_cluster = (0, regex_data[imp_id]['regex'][1][0][0], regex_data[imp_id]['regex'][1][0][1])
        else:
            matched_cluster = max(matched_cluster, key=operator.itemgetter(2))
        opn_seq = regex_data[matched_cluster[0]]['opn_seq']
        inflected_word = helper.apply_operation(opn_seq.split(' '), test_word)
        word_map[test_word]['pac_re_output'] = inflected_word
        if inflected_word == word_map[test_word]['gt']:
            correct_guess += 1
    accuracy = float(correct_guess) / len(word_map)
    return(accuracy, word_map)


def complete_evaluation(training_files, method='uncov_test', level='medium'):
    if method == 'uncov_test':
        testing_files = os.listdir(UNCOV_TEST_DIR)
    elif method == 'dev':
        testing_files = os.listdir(DEV_DIR)

    for file in copy.copy(training_files):
        if not file.endswith(level):
            training_files.remove(file)

    training_files = sorted(training_files)
    testing_files = sorted(testing_files)
    if len(training_files) != len(testing_files):
        testing_files = ['-'.join(file.split('-')[:-2]) + '-uncovered-test' for file in training_files]
    # sort the list so that trainig and testing files are aligned

    # accuracy mapping for a language
    acc_wrdMap = {}
    for idx, train_file in enumerate(training_files):
        lang = train_file.split('/')[-1]
        try:
            acc_wrdMap[lang].append(evaluate(
                lang,
                UNCOV_TEST_DIR + testing_files[idx]))
        except KeyError:
            acc_wrdMap[lang] = evaluate(
                lang,
                UNCOV_TEST_DIR + testing_files[idx])
        print(
            "Language: {}, Accuracy: {}%".format(
                lang,
                acc_wrdMap[lang][0]))

    with open(EVAL_DIR + 'eval_regex_' + level + '.json', 'w') as re_out:
        json.dump(acc_wrdMap, re_out)


if __name__ == '__main__':
    complete_evaluation(
        os.listdir(TRAIN_DIR),
        method='uncov_test',
        level='high')
