#!/usr/bin/env python

from optparse import OptionParser
import hashlib
import os.path

import timedRun

first_run = True


def md5_for_file(fname, block_size=2**20):
    md5 = hashlib.md5()
    with open(fname, 'r') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.digest()


def parseOptions(arguments):
    parser = OptionParser()
    parser.disable_interspersed_args()
    parser.add_option('-t', '--timeout', type='int', action='store', dest='condTimeout',
                      default=120,
                      help='Optionally set the timeout. Defaults to "%default" seconds.')

    options, args = parser.parse_args(arguments)

    return options.condTimeout, args


def interesting(cliArgs, tempPrefix):
    (timeout, args) = parseOptions(cliArgs)

    runinfo = timedRun.timed_run(args, timeout, tempPrefix)

    global first_run
    if first_run:
        original_file = args[-1]
        global original_hash
        original_hash = md5_for_file(original_file)
        first_run = False

    timeString = " (%.3f seconds)" % runinfo.elapsedtime
    new_hash = md5_for_file(args[-1])

    if new_hash == original_hash:
        print 'Original file, always interesting. ' + runinfo.msg + timeString
        return True
    elif runinfo.sta == timedRun.CRASHED:
        print 'Exit status: ' + runinfo.msg + timeString
        return True
    else:
        print "[Uninteresting] It is normal." + timeString
        return False
