#!/usr/bin/python

############################################################
# Name		: Duplicate File Finder
# Created	: Nov 11, 2014
# Usage		: df_finder.py dir...
# Example	: df_finder.py dir1 dir2 dir3
# Note		: If there is a duplicate file found, then it
# 			  would be moved to directory 'dst'. It creats
#			  'dst' if it does not exist.
############################################################

from hashlib import md5
import os, os.path
import shutil
import string, sys
from optparse import OptionParser

g_dict = {}
g_dups = []
g_dst  = "dst"

def gen_file_md5sum(file_path):
	m = md5()

	file_obj = open(file_path, "rb")
	m.update(file_obj.read())
	file_obj.close()

	return m.hexdigest()

def gen_dict(dir_path):
	for root, dirs, files in os.walk(dir_path):
		for name in files:
			val = os.path.join(root, name)
			key = gen_file_md5sum(val)
			print "[MD5] %s: %s"%(key, val)
			if key in g_dict:
				print "[DUP] %s vs %s"%(g_dict[key], val)
				g_dups.append(val)
			else:
				g_dict[key] = val

def main(args):
	parser = OptionParser(usage="%s [dir...]"%(args[0]))
	(options, args) = parser.parse_args()

	if len(args) == 0:
		parser.error("Please specify at least one directory!")
		
	for dir_path in args:
		if os.path.isdir(dir_path):
			gen_dict(dir_path)
		else:
			parser.error("Directory `%s' does not exist!"%(dir_path))

	if not os.path.isdir(g_dst):
		os.mkdir(g_dst)
	for file_path in g_dups:
		print "Move %s to %s"%(file_path, g_dst)
		shutil.move(file_path, g_dst)

if __name__ == "__main__":
	main(sys.argv)

