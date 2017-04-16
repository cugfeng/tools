#!/usr/bin/env python

import sys
import bs4
import requests

def main(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    li_list = soup.find_all("li")
    for li in li_list:
        if li.has_attr("id") and li.has_attr("title"):
            #print "####################"
            #print li
            a = li.find("a")
            print "http:" + a["href"]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Usage: {} URL".format(sys.argv[0])
