#!/usr/bin/python

############################################################
# Name		: Sync files between two directories
# Created	: Nov 30, 2014
# Usage		: sync-file.py src dst
# Note		: For file in $src but not in $dst, this program
# 			  copies it to $dst.
############################################################

import os, os.path
import shutil
import string, sys
import logging
from optparse import OptionParser

g_log    = "sync-file.log"
g_logger = logging.getLogger()

def init_logger():
	formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

	file_handler = logging.FileHandler(g_log)
	file_handler.setFormatter(formatter)
	file_handler.setLevel(logging.DEBUG)

	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(formatter)
	stream_handler.setLevel(logging.INFO)

	g_logger.addHandler(file_handler)
	g_logger.addHandler(stream_handler)
	g_logger.setLevel(logging.DEBUG)

def main(args):
	program = os.path.basename(args[0])
	parser  = OptionParser(usage="%s src dst"%(program))
	(options, args) = parser.parse_args()

	if len(args) != 2:
		parser.error("Please specify both source and destination directories!")
	for dir_path in args:
		if not os.path.isdir(dir_path):
			parser.error("%s is not a directory!"%(dir_path))

	init_logger()

	dir_src = args[0]
	dir_dst = args[1]
	for root, dirs, files in os.walk(dir_src):
		for name in dirs:
			path_src = os.path.join(root, name)
			path_dst = string.replace(path_src, dir_src, dir_dst, 1)
			if not os.path.exists(path_dst):
				g_logger.info("Create directory %s"%(path_dst))
				os.mkdir(path_dst)
		for name in files:
			path_src = os.path.join(root, name)
			path_dst = string.replace(path_src, dir_src, dir_dst, 1)
			if not os.path.exists(path_dst):
				g_logger.info("Copy %s to %s"%(path_src, path_dst))
				shutil.copy2(path_src, path_dst)

if __name__ == "__main__":
	main(sys.argv)

