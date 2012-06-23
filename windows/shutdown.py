#!/usr/bin/python3

import os
import sys
import time
import string
from optparse import OptionParser

def shutdown_in_minutes(_min):
	print("Shutdown in {0:.0f} hour(s) {1:.0f} minute(s)...".format(_min / 60, _min % 60))

	while _min > 0:
		_hour_left, _min_left = divmod(_min, 60)
		print("\rTime left: {0:.0f} hour(s) {1:02.0f} minute(s)...".format(_hour_left, _min_left), end='')

		time.sleep(60)
		_min -= 1

	if sys.platform == "win32":
		os.system("shutdown -s")
	else:
		os.system("shutdown -h now")

def time2min(_time):
	_time_list = str.split(_time, ':')
	_hour = int(_time_list[0])
	_min  = int(_time_list[1])

	_min += _hour * 60
	return _min

def main(args):
	parser = OptionParser(usage="shutdown.py [-i n[hm]] [-a hh:mm]")
	parser.add_option("-i", "--in", action="store", type="string", 
			dest="intime", help="Shutdown in n hours/minutes")
	parser.add_option("-a", "--at", action="store", type="string",
			dest="attime", help="Shutdown at hh:mm")
	(options, args) = parser.parse_args()

	#print(options)
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
		_min = time2min(options.attime) 
		_now = time.localtime()
		_cur_min = _now.tm_hour * 60 + _now.tm_min
		if (_min < _cur_min):
			_min += 24 * 60
		shutdown_in_minutes(_min - _cur_min)

if __name__ == "__main__":
	main(sys.argv)

