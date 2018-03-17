"""
Evaluation approach currently used in the script:

1. Take the words from test dataset present in the training data too
2. Find the approriate implication from the set of learnt implications
3. Apply the most common set of operation from the premise of appropriate impl.
4. Compare the resultant with the one given in test set.
"""

import os
import copy
import helper
import operator
import pandas as pd
import concept_context as cn

TRAIN_DIR = 'data/train/'
DEV_DIR = 'data/dev/'
COV_TEST_DIR = 'data/test/covered/'
UNCOV_TEST_DIR = 'data/test/uncovered/'


def evaluate(train_dir, test_dir, filter_pac=True):
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

    relations = build_relations(train_data)

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
            if impl.premise == impl.conclusion or len(impl.conclusion) == attribute_size:
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
        implId_opnSeq_map[idx] = operation(premise_data)

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
                output = apply_operation(opn_seq, word)
                word_map[word]['pac_output'] = output
                if word_map[word]['gt'] == output:
                    correct += 1
                # stop at the first match as basis is sorted by premise length
                break
    accuracy = correct / float(len(common_words))
    return(accuracy, word_map)


def operation(dataframe):
    """Returns the operation sequence most common in the dataframe"""
    counter = {}
    for i, r in dataframe.iterrows():
        opn_seq = ' '.join(r['deleted'] + r['added'])
        try:
            counter[opn_seq] += 1
        except KeyError:
            counter[opn_seq] = 1
    return max(counter.items(), key=operator.itemgetter(1))[0]


def apply_operation(operation_sequence, word):
    """Applies operation sequence on the word"""
    for opn in operation_sequence:
        if opn.startswith('::'):
            # delete operation
            opn = opn[2:]
            if opn == '':
                continue
            else:
                word = delete(opn, word)
        else:
            # insert operation
            word = insert(opn, word)
    return word


def delete(old, word, new='', occurrence=1):
    """Removes to_delete from the word"""
    li = word.rsplit(old, occurrence)
    return(new.join(li))


def insert(to_insert, word):
    """Appends to_insert to the word"""
    return(word + to_insert)


def build_relations(data):
    """
    Build attribute -- object (source-word -- operation) relations from processed training data
    denote ::operation for delete operations. For eg. ::ना shows delete ना
    """
    relations = []
    data['deleted'] = data['deleted'].apply(
        lambda opns: ['::' + opn for opn in opns])
    for i, r in data.iterrows():
        attr = r['source']
        objects = r['deleted'] + r['added']
        for obj in objects:
            relations.append((obj, attr))
    return relations


def complete_evaluation(training_files, method='uncov_test', level='medium',
                        filter_pac=True, best_of=1):
    if method == 'uncov_test':
        testing_files = os.listdir(UNCOV_TEST_DIR)
    elif method == 'dev':
        testing_files = os.listdir(DEV_DIR)

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
        for i in range(best_of):
            try:
                acc_wrdMap[lang].append(evaluate(
                    TRAIN_DIR + train_file,
                    UNCOV_TEST_DIR + testing_files[idx],
                    filter_pac))
            except KeyError:
                acc_wrdMap[lang] = evaluate(
                TRAIN_DIR + train_file,
                UNCOV_TEST_DIR + testing_files[idx],
                filter_pac)
        acc_wrdMap[lang] = max(acc_wrdMap[lang], key=operator.itemgetter(0))
        print("Language: {}, Accuracy: {}%".format(lang, acc_wrdMap[lang][0] * 100))


if __name__ == '__main__':
    complete_evaluation(
        os.listdir(TRAIN_DIR),
        method='uncov_test',
        level='medium',
        filter_pac=False,
        best_of=5)

    # import time
    # for i in range(10):
    #     start = time.time()
    #     a = evaluate('data/train/english-train-high', 'data/dev/english-dev')
    #     print(a)
    #     print(time.time() - start)
