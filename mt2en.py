#!/usr/bin/python
# mt2en.py
# Convert MovableType format to almost Evernote XML 
# 2011,2012 Saburo Higuchi <hig at math.ryukoku.ac.jp>

import datetime
import sys
import re
import time

EN_APP_VERSION="Evernote Mac 3.0.7 Beta 2 (224219)"

d=datetime.datetime.today()

body=""
last=""
mode=0
property={}
category=[]

pattern=re.compile('^(?P<property>TITLE|CATEGORY|DATE): (?P<value>.*)$')

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export.dtd">'
print '<en-export export-date="' + time.strftime("%Y%m%dT%H%M%SZ") +'" application="Evernote" version="' + EN_APP_VERSION +'">' # or anything

for line in sys.stdin:
    if mode==1 :
        if re.findall("^EXTENDED BODY:$",line):
            mode=0

            print "<note>"
            print "<title>" + property['TITLE'] + "</title>"
            print '<content><![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
            print '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            print '<en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">' + body + "</en-note>"
            print "]]></content>"
            ds=re.sub(r'00(:[0-9][0-9]:[0-9][0-9] .M)',r'12\1',property['DATE'])
            d=time.strptime(ds,"%m/%d/%Y %I:%M:%S %p") #,"%m/%d/%Y %I:%M:%S %p")
            t=time.mktime(d)
            d=time.gmtime(t)
            print "<created>" + time.strftime("%Y%m%dT%H%M%SZ",d) + "</created>"
            print "<updated>" + time.strftime("%Y%m%dT%H%M%SZ",d) + "</updated>"
            for c in category :
                print "<tag>" + c + "</tag>"
#            print "<note-attributes><subject-date>19700101T000000Z</subject-date><source>web.clip</source><source-url>"+"http://d.hatena.ne.jp/hig33/"+ time.strftime("%Y%m%d",d)+"</source-url></note-attributes>"    
            print "<note-attributes><source>web.clip</source><source-url>"+"http://d.hatena.ne.jp/hig33/"+ time.strftime("%Y%m%d",d)+"</source-url></note-attributes>"    
            print "</note>"
            propety={}
            category=[]
            continue
        else:
            body+=last
            last=line
    if( len(re.findall("^BODY:$",line))>0 ):
        mode=1
        body=""
        last=""
        continue
    else:    
        result=pattern.search(line)
        if result:
            if result.group('property')=='CATEGORY':
                category.append(result.group('value'))
            else:                                
                property.update({ result.group('property') :result.group('value') })

print '</en-export>'
