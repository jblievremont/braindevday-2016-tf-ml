#!/usr/bin/python

#
# SonarSource BrainDevDay 2016 - Prepare mailing list data for TF - pass 2
#

import csv
import numpy
import sys

BLOCK_SIZE = 256
TRAIN_TEST_RATIO = 7

if __name__ == '__main__':

    csvFilePath = None

    if len(sys.argv) < 2:
        print 'First arg must be a mbox file path'
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

    subjectArray = numpy.zeros((len(subjects), BLOCK_SIZE), dtype=numpy.int8)
    addressArray = numpy.zeros(len(addresses), dtype=numpy.int8)

    for rowIndex in range(len(subjects)):
        adrIndex = sortedUniqueAddresses.index(addresses[rowIndex])
        addressArray[rowIndex] = adrIndex
        subjectBytes = [ord(subjectChar) for subjectChar in subjects[rowIndex]]
        subjectArray[rowIndex] = subjectBytes + [0] * (BLOCK_SIZE - len(subjectBytes))

    #print sortedUniqueAddresses
    #print subjectArray
    #print addressArray

    with open('addresses.txt', 'wb') as addressesFile:
        for address in sortedUniqueAddresses:
            addressesFile.write(address + '\n')

    with open('subjectsTrain.bin', 'wb') as subjectsFile:
        index = 0
        for subject in subjectArray:
            if index % TRAIN_TEST_RATIO:
                subjectsFile.write(bytearray(subject))
            index += 1

    with open('subjectsTest.bin', 'wb') as subjectsFile:
        index = 0
        for subject in subjectArray:
            if not index % TRAIN_TEST_RATIO:
                subjectsFile.write(bytearray(subject))
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
