#!/usr/bin/python

############################################################
# Name      : Remove empty directory
# Created   : Apr 18, 2015
# Usage     : remove-empty-dir.py dir...
# Example   : remove-empty-dir.py dir1 dir2 dir3
############################################################

import os, os.path
import sys
import logging
from optparse import OptionParser

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

def remove_empty_dir(dir_path):
    dir_path = unicode(dir_path)
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in dirs:
            sub_dir_path = os.path.join(root, name)
            if len(os.listdir(sub_dir_path)) == 0:
                g_logger.info("Remove empty directory: %s"%(sub_dir_path))
                os.rmdir(sub_dir_path)

def main(args):
    parser = OptionParser(usage="%s [dir...]"%(args[0]))
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("Please specify at least one directory!")

    init_logger()

    for dir_path in args:
        if os.path.isdir(dir_path):
            remove_empty_dir(dir_path)
        else:
            parser.error("Directory `%s' does not exist!"%(dir_path))

if __name__ == "__main__":
    main(sys.argv)

