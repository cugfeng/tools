#!/usr/bin/python

############################################################
# Name      : Duplicate File Finder
# Created   : Nov 11, 2014
# Usage     : df_finder.py dir...
# Example   : df_finder.py dir1 dir2 dir3
# Note      : If there is a duplicate file found, then it
#             would be moved to directory 'dst'. It creats
#             'dst' if it does not exist.
############################################################

from hashlib import md5
import sqlite3
import os, os.path
import shutil
import string, sys
import logging
from optparse import OptionParser

g_dups = list()
g_dst  = "dst"

g_log    = "df_finder.log"
g_logger = logging.getLogger()

g_db_file   = "sqlite3.db"
g_db_conn   = None
g_db_cursor = None

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

def init_db():
    global g_db_conn
    global g_db_cursor

    g_db_conn   = sqlite3.connect(g_db_file)
    g_db_cursor = g_db_conn.cursor()

    try:
        g_db_cursor.execute("SELECT * FROM md5s")
    except Exception:
        g_logger.info("Initialize database")
        g_db_cursor.execute("CREATE TABLE md5s (md5 text, path text)")
        g_db_conn.commit()

def deinit_db():
    global g_db_conn
    global g_db_cursor

    g_db_conn.close()
    g_db_conn   = None
    g_db_cursor = None

def gen_file_md5sum(file_path):
    m = md5()

    file_obj = open(file_path, "rb")
    m.update(file_obj.read())
    file_obj.close()

    return m.hexdigest()

def find_duplicate(dir_path):
    dir_path = unicode(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for name in files:
            val = os.path.join(root, name)

            # For MD5
            g_db_cursor.execute("SELECT * FROM md5s WHERE path=?", (val,))
            row = g_db_cursor.fetchone()
            if row is None:
                key = gen_file_md5sum(val)
                g_db_cursor.execute("SELECT * FROM md5s WHERE md5=?", (key,))
                row = g_db_cursor.fetchone()
                if row is None:
                    g_logger.info("Add file: %s -- %s"%(key, val))
                    g_db_cursor.execute("INSERT INTO md5s VALUES (?,?)", (key, val))
                    g_db_conn.commit()
                else:
                    g_logger.info("Duplicate file: %s vs %s"%(row[1], val))
                    g_dups.append(val)
            else:
                g_logger.info("File %s is already in database"%(val));

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
    init_db()

    for dir_path in args:
        if os.path.isdir(dir_path):
            find_duplicate(dir_path)
        else:
            parser.error("Directory `%s' does not exist!"%(dir_path))

    if not os.path.exists(g_dst):
        os.mkdir(g_dst)
    for file_src in g_dups:
        file_name = os.path.basename(file_src)
        file_dst  = os.path.join(g_dst, file_name)
        if os.path.exists(file_dst):
            for i in range(1, 65):
                file_tmp = get_file_name(file_name, i)
                file_dst = os.path.join(g_dst, file_tmp)
                if not os.path.exists(file_dst):
                    g_logger.info("Rename %s to %s"%(file_name, file_tmp))
                    break
        g_logger.info("Move %s to %s"%(file_src, file_dst))
        shutil.move(file_src, file_dst)

    deinit_db()

if __name__ == "__main__":
    main(sys.argv)

