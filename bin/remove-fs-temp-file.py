#!/usr/bin/python

############################################################
# Name      : Remove filesystem temp files
# Created   : Apr 19, 2015
# Usage     : remove-fs-temp-file.py dir...
# Example   : remove-fs-temp-file.py dir1 dir2 dir3
############################################################

import os, os.path
import sys
import shutil
import logging
from optparse import OptionParser

g_files = [ "._.DS_Store", ".DS_Store" ]
g_dirs  = [ ".AppleDouble" ]

g_log    = "empty-dir.log"
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

def remove_fs_temp_file(dir_path):
    dir_path = unicode(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for file in g_files:
            if file in files:
                path = os.path.join(root, file)
                print "Remove file %s" % path
                os.remove(path)
        for dir in g_dirs:
            if dir in dirs:
                path = os.path.join(root, dir)
                print "Remove directory %s" % path
                shutil.rmtree(path)

def main(args):
    parser = OptionParser(usage="%s [dir...]"%(args[0]))
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("Please specify at least one directory!")

    init_logger()

    for dir_path in args:
        if os.path.isdir(dir_path):
            remove_fs_temp_file(dir_path)
        else:
            parser.error("Directory `%s' does not exist!"%(dir_path))

if __name__ == "__main__":
    main(sys.argv)

