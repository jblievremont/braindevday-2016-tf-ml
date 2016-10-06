#!/usr/bin/python

#
# SonarSource BrainDevDay 2016 - Prepare mailing list data for TF
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
