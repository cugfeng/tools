#!/usr/bin/env python

import sys
import bs4
import requests

def main(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    for div in soup.select("div div[name='tvlist']"):
        #print "####################"
        #print div
        a = div.find("a")
        print "http:" + a["href"]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Usage: {} URL".format(sys.argv[0])
