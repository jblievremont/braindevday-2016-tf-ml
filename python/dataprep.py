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

from collections import Counter

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

    print "Got %d messages" % len(sonarSourceMailingList)

    rootMessages = [message for message
        in sonarSourceMailingList.values()
        if not message['References']
        and not '@sonarsource.com' in message['From']]

    print "Got %d root messages not from SonarSource" % len(rootMessages)

    rootMessageIds = [message['Message-ID'] for message
        in rootMessages]

    firstResponses = [message for message
        in sonarSourceMailingList.values()
        if message['References'] in rootMessageIds]

    print "Got %d first responses" % len(firstResponses)

    firstSonarSourceResponders = Counter(map(sanitize_address, [
        message['From'] for message
        in firstResponses
        if '@sonarsource.com' in message['From']]))

    print "First responders from SS: "
    pprint.pprint(firstSonarSourceResponders)
