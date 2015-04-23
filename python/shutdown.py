#!/usr/bin/python

import sys
import time
import string
import subprocess
from optparse import OptionParser

def shutdown():
    print "Shutdown now..."
    if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
        subprocess.call(["shutdown", "/s"])
    elif sys.platform.startswith("linux"):
        subprocess.call(["shutdown", "-h", "now"])
    else:
        print "Platform \`%s' is not supported!"%(sys.platform)

def shutdown_in_minutes(minutes):
    while minutes > 0:
        _hour, _min = divmod(minutes, 60)
        print "Shutdown in %02d hour(s) %02d minute(s)..."%(_hour, _min)

        time.sleep(60)
        minutes -= 1

    shutdown()

def linux_is_root():
    _id = subprocess.check_output(["id", "-u"])
    if _id[:-1] == "0":
        return True
    else:
        return False

def strtime_to_minutes(strtime):
    _time_list = str.split(strtime, ':')
    _hour = int(_time_list[0])
    _min  = int(_time_list[1])

    return _hour * 60 + _min

def main(args):
    if sys.platform.startswith("linux"):
        if not linux_is_root():
            print "You must be root to run this program!"
            return

    parser = OptionParser(usage="shutdown.py [-i n[hm]] [-a hh:mm]")
    parser.add_option("-i", "--in", action="store", type="string", 
            dest="intime", help="Shutdown in n hours/minutes")
    parser.add_option("-a", "--at", action="store", type="string",
            dest="attime", help="Shutdown at hh:mm")
    (options, args) = parser.parse_args()

    _argc = 0
    if options.intime is not None:
        _argc += 1
    if options.attime is not None:
        _argc += 1
    if _argc != 1:
        parser.error("incorrect number of arguments(must be 1)")

    if options.intime is not None:
        _times = 1
        if options.intime[-1].lower() == 'h':
            _times *= 60
        elif options.intime[-1].lower() == 'm':
            pass
        else:
            parser.error("argument of in must end with 'h' or 'm'")
        _min = int(options.intime[:-1]) * _times
        shutdown_in_minutes(_min)

    if options.attime is not None:
        _min = strtime_to_minutes(options.attime)
        _now = time.localtime()
        _cur_min = _now.tm_hour * 60 + _now.tm_min
        if (_min < _cur_min):
            _min += 24 * 60
        shutdown_in_minutes(_min - _cur_min)

if __name__ == "__main__":
    main(sys.argv)

