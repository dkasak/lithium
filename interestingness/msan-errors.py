#!/usr/bin/env python

from optparse import OptionParser

import timedRun


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
    timeString = " (%.3f seconds)" % runinfo.elapsedtime
    if runinfo.sta == timedRun.ASAN_EXIT_CODE:
        print 'Exit status: ' + runinfo.msg + timeString
        return True
    else:
        print "[Uninteresting] It didn't crash." + timeString
        return False
