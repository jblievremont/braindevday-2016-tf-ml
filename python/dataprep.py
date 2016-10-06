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
        if not message['References']]

    print "Got %s root messages" % len(rootMessages)
