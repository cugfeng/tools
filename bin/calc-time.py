#!/usr/bin/python

from optparse import OptionParser

def to_kb(string):
	if string[-1] in ["g", "G"]:
		scale = 1024 * 1024
	elif string[-1] in ["m", "M"]:
		scale = 1024
	elif string[-1] in ["k", "K"]:
		scale = 1
	else:
		print "Warning: wrong scale %s, set as K" % string[-1]
		scale = 1

	return (int)(scale * float(string[:-1]))

def calculate(total_size, speed):
	minutes  = total_size / (60 * speed)
	hours    = minutes / 60
	minutes %= 60
	print "Speed %d KB/sec: need %d hours %d minutes" % (speed, hours, minutes)
	 
def calculate_range(total_size, speed_min, speed_max, speed_step):
	for speed in range(speed_min, speed_max, speed_step):
		calculate(total_size, speed)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-i", "--min",
			action="store", type="string", dest="speed_min",
			help="minimum transfer speed")
	parser.add_option("-a", "--max",
			action="store", type="string", dest="speed_max",
			help="maximum transfer speed")
	parser.add_option("-t", "--step",
			action="store", type="string", dest="speed_step",
			help="transfer speed step")
	parser.add_option("-p", "--speed",
			action="store", type="string", dest="speed",
			help="transfer speed")
	parser.add_option("-s", "--size",
			action="store", type="string", dest="size",
			help="total size")
	(options, args) = parser.parse_args()

	total_size = to_kb(options.size)
	if options.speed is not None:
		speed = to_kb(options.speed)
		calculate(total_size, speed)
	else:
		speed_min  = to_kb(options.speed_min)
		speed_max  = to_kb(options.speed_max)
		speed_step = to_kb(options.speed_step)
		calculate_range(total_size, speed_min, speed_max, speed_step)

