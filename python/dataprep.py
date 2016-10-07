#!/usr/bin/python

#
# SonarSource BrainDevDay 2016 - Prepare mailing list data for TF
#
# See https://docs.python.org/2/library/mailbox.html for doc on
# mailbox module (used to parse mbox file)
# See https://docs.python.org/2/library/email.message.html for doc
# on email.message module (used to handle email message contents)
#
# See https://www.jwz.org/doc/threading.html on algorithm that can
# be used to build email discussion threads
#

import mailbox
import sys
import pprint
import csv

from collections import Counter

mailingListAddresses = [
    'user@sonar.codehaus.org',
    'sonarqube@googlegroups.com',
    'sonarlint@googlegroups.com'
]

def isToMailingList(addresses):
    for address in addresses:
        for mlAddress in mailingListAddresses:
            if mlAddress in address:
                return True
    return False

def sanitize_address(email):
    if '<' in email:
        openingChevron = email.find('<')
        closingChevron = email.find('>')
        return email[openingChevron + 1:closingChevron]
    else:
        return email

if __name__ == '__main__':

    mboxFilePath = None

    if len(sys.argv) < 2:
        print 'First arg must be a mbox file path'
        sys.exit(-1)
    else:
        mboxFilePath = sys.argv[1]

    sonarSourceMailingList = mailbox.mbox(mboxFilePath)

    # print "Got %d messages" % len(sonarSourceMailingList)

    rootMessages = dict([(message['Message-Id'], message) for message
        in sonarSourceMailingList.values()
        if not message['References']
        and not '@sonarsource.com' in message['From']])

    # print "Got %d root messages not from SonarSource" % len(rootMessages)

    rootMessageIds = rootMessages.keys()

    firstResponses = [message for message
        in sonarSourceMailingList.values()
        if message['References'] in rootMessageIds
        and isToMailingList(message.get_all('To', []))]

    # print "Got %d first responses" % len(firstResponses)

    respondersWithRootSubject = [
        (
            sanitize_address(message['From']),
            rootMessages[message['References']]['Subject']
        )
        for message in firstResponses
        if '@sonarsource.com' in message['From']]

    with open(mboxFilePath + '.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar="'", quoting=csv.QUOTE_MINIMAL)
        for address, subject in respondersWithRootSubject:
            spamwriter.writerow([address, subject])
