#!/usr/bin/python
# -*- coding: utf-8 -*-

# et.py
# Convert XML produced by mt2en.py to Evernote XML
#
# 2011,2012 Saburo Higuchi <hig at math.ryukoku.ac.jp>
# with lxml-py27 2.3.2-1

from lxml import etree
import sys
import lxml.html
import re

def replamp(url):
    return url.group().replace('&','&amp;').replace('#','&#35;')

myParser=etree.XMLParser(encoding='UTF-8')

xmlstring=''

for line in sys.stdin:
    xmlstring += line

elem=etree.fromstring(xmlstring,parser=myParser)

for e in elem.getiterator("content"):
    t2=re.sub(r'href="[^"].*"',replamp,e.text)

    root=lxml.html.fromstring(t2.encode('utf_8'))
    
    divclass = root.xpath('//*[@class]')
    for d in divclass:
        del d.attrib['class']

    imgs = root.xpath('//img')
    for im in imgs:
        im.tail="Image:"+im.attrib['alt']+" "+im.attrib['src']
        im.drop_tree()

    str='<?xml version="1.0" encoding="UTF-8" standalone="no"?>'+'<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'+lxml.html.tostring(root,encoding="us-ascii")
    e.text=str.replace('&lt;br&gt;','&lt;br/&gt;')

print '<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export.dtd">'
print(elem.docinfo.doctype)
print(etree.tostring(elem,encoding="us-ascii",method="xml",xml_declaration=True).encode('utf_8'))



