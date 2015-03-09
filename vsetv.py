#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import vsetv_parser

count_day = 3
fulldesc = True

parser = vsetv_parser.parser_vsetv('http://www.vsetv.com/', '/tmp/vsetv', 'windows-1251')

if len(sys.argv) > 1:
    parser.channelsfiledata = sys.argv[1]
if len(sys.argv) > 2:
    parser.outxml = sys.argv[2]
if len(sys.argv) > 3:
    count_day = int(sys.argv[3])
if len(sys.argv) > 4:
    fulldesc = False
    sfulldesc = sys.argv[4]
    if sfulldesc == '1':
	fulldesc = True 

parser.load_channeldata()
parser.isfulldesc = fulldesc
parser.parsecontent_programme_all(count_day)
parser.set_programmestop()
parser.save_xmltv()