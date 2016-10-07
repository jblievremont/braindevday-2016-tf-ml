#!/usr/bin/python

#
# SonarSource BrainDevDay 2016 - Prepare mailing list data for TF - pass 2
#

import csv
import numpy
import sys
import nltk
import pprint
import struct

from nltk.corpus import stopwords

BLOCK_SIZE = 25
TRAIN_TEST_RATIO = 7

if __name__ == '__main__':

    csvFilePath = None

    if len(sys.argv) < 2:
        print 'First arg must be a CSV file path'
        sys.exit(-1)
    else:
        csvFilePath = sys.argv[1]

    addresses = []
    subjects = []

    with open(csvFilePath, 'rb') as csvfile:
        mlReader = csv.reader(csvfile, delimiter=',', quotechar="'")
        for address, subject in mlReader:
            addresses.append(address)
            subjects.append(subject)

    sortedUniqueAddresses = sorted(list(set(addresses)))

    tokenized_subjects = [
        nltk.word_tokenize(subject) for subject in subjects
    ]
    stopwords_en = stopwords.words('english')
    flattened_subjects = [
        word.lower()
        for subject in tokenized_subjects
        for word in subject
        if word not in stopwords_en
    ]
    sortedUniqueTokens = sorted(list(set(flattened_subjects)))
    uniqueTokenDict = dict([(token, index) for (index, token) in enumerate(sortedUniqueTokens)])

    subjectArray = numpy.zeros((len(subjects), BLOCK_SIZE), dtype=numpy.int16)
    addressArray = numpy.zeros(len(addresses), dtype=numpy.int8)

    for rowIndex in range(len(subjects)):
        adrIndex = sortedUniqueAddresses.index(addresses[rowIndex])
        addressArray[rowIndex] = adrIndex
        subjectWordIndices = [
            uniqueTokenDict[token.lower()]
            for subject in tokenized_subjects
            for token in subject
            if uniqueTokenDict.has_key(token)
        ][0:BLOCK_SIZE]
        subjectArray[rowIndex] = subjectWordIndices + [0] * (BLOCK_SIZE - len(subjectWordIndices))

    #print sortedUniqueAddresses
    #print subjectArray
    #print addressArray

    with open('addresses.txt', 'wb') as addressesFile:
        for address in sortedUniqueAddresses:
            addressesFile.write(address + '\n')

    with open('tokens.txt', 'wb') as tokensFile:
        for token in sortedUniqueTokens:
            tokensFile.write(token + '\n')

    with open('subjectsTrain.bin', 'wb') as subjectsFile:
        index = 0
        for subject in subjectArray:
            if index % TRAIN_TEST_RATIO:
                for tokenIndex in subject:
                    subjectsFile.write(tokenIndex)
            index += 1

    with open('subjectsTest.bin', 'wb') as subjectsFile:
        index = 0
        for subject in subjectArray:
            if not index % TRAIN_TEST_RATIO:
                for tokenIndex in subject:
                    subjectsFile.write(tokenIndex)
            index += 1

    with open('labelsTrain.bin', 'wb') as labelsFile:
        index = 0
        for label in addressArray:
            if index % TRAIN_TEST_RATIO:
                labelsFile.write(chr(label))
            index += 1

    with open('labelsTest.bin', 'wb') as labelsFile:
        index = 0
        for label in addressArray:
            if not index % TRAIN_TEST_RATIO:
                labelsFile.write(chr(label))
            index += 1
