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
import logging
from optparse import OptionParser

g_dict_md5  = {}
g_dict_name = {}
g_dups = set()
g_dst  = "dst"
g_log  = "df_finder.log"
g_size_threshold = 64

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

def gen_file_md5sum(file_path):
	m = md5()

	file_obj = open(file_path, "rb")
	m.update(file_obj.read())
	file_obj.close()

	return m.hexdigest()

def is_jpeg(file_path):
	file_name = os.path.basename(file_path)
	words = file_name.rsplit('.', 1)
	if len(words) == 2:
		file_ext = words[1].lower()
		if file_ext in [ "jpg", "jpeg" ]:
			return True

	return False

def is_same_jpeg(file_l, file_r):
	file_l_obj = open(file_l, "r")
	file_l_content = file_l_obj.read()
	file_l_obj.close()

	file_r_obj = open(file_r, "r")
	file_r_content = file_r_obj.read()
	file_r_obj.close()

	file_l_size = os.path.getsize(file_l)
	file_r_size = os.path.getsize(file_r)

	# Assume data after EOI no larger than g_size_threshold bytes
	if abs(file_l_size - file_r_size) > g_size_threshold:
		g_logger.debug("Size difference between %s and %s is larger than %d"%(
					file_l, file_r, g_size_threshold))
		return False

	# http://en.wikipedia.org/wiki/JPEG
	# JPEG EOI (End Of Image): 0xFF 0xD9
	if file_l_size > file_r_size:
		eoi_1 = file_l_content[file_r_size - 2]
		eoi_2 = file_l_content[file_r_size - 1]
		cmp_size = file_r_size
	else:
		eoi_1 = file_r_content[file_l_size - 2]
		eoi_2 = file_r_content[file_l_size - 1]
		cmp_size = file_l_size
	if eoi_1 != '\xFF' or eoi_2 != '\xD9':
		g_logger.debug("Seems both %s and %s have data after EOI"%(file_l, file_r))
		return False

	for i in range(cmp_size):
		if file_l_content[i] != file_r_content[i]:
			g_logger.debug("File content at 0x%x (0x%02X vs 0x%02X) is not the same"%(
						i, file_l_content[i], file_r_content[i]))
			return False

	return True

def gen_dict(dir_path):
	for root, dirs, files in os.walk(dir_path):
		for name in files:
			val = os.path.join(root, name)

			# For MD5
			key = gen_file_md5sum(val)
			g_logger.debug("MD5 %s: %s"%(key, val))
			if key in g_dict_md5:
				g_logger.info("Duplicate file: %s vs %s"%(g_dict_md5[key], val))
				g_dups.add(val)
			else:
				g_dict_md5[key] = val

			# For file name and content
			if name in g_dict_name:
				g_logger.debug("File %s already exist"%(name))
				path_list = g_dict_name[name]
				for file_path in path_list:
					if is_jpeg(val) and is_same_jpeg(file_path, val):
						g_logger.info("Duplicate file: %s vs %s"%(file_path, val))
						g_dups.add(val)
						break
				else:
					path_list.append(val)
				g_dict_name[name] = path_list
			else:
				g_dict_name[name] = [(val)]

def get_file_name(file_name, index):
	words = file_name.rsplit('.', 1)
	if len(words) == 1:
		return "%s-%d"%(file_name, index)
	else:
		return "%s-%02d.%s"%(words[0], index, words[1])

def main(args):
	parser = OptionParser(usage="%s [dir...]"%(args[0]))
	(options, args) = parser.parse_args()

	if len(args) == 0:
		parser.error("Please specify at least one directory!")

	init_logger()

	for dir_path in args:
		if os.path.isdir(dir_path):
			gen_dict(dir_path)
		else:
			parser.error("Directory `%s' does not exist!"%(dir_path))

	if not os.path.exists(g_dst):
		os.mkdir(g_dst)
	for file_src in g_dups:
		file_name = os.path.basename(file_src)
		file_dst  = os.path.join(g_dst, file_name)
		if os.path.exists(file_dst):
			for i in range(64):
				file_tmp = get_file_name(file_name, i)
				file_dst = os.path.join(g_dst, file_tmp)
				if not os.path.exists(file_dst):
					g_logger.info("Rename %s to %s"%(file_name, file_tmp))
					break
		g_logger.info("Move %s to %s"%(file_src, file_dst))
		shutil.move(file_src, file_dst)

if __name__ == "__main__":
	main(sys.argv)

