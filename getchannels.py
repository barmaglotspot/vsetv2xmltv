#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import vsetv_parser

parser = vsetv_parser.parser_vsetv('http://www.vsetv.com/', '/tmp/vsetv', 'windows-1251')
if len(sys.argv) > 1:
    parser.channelsfiledata = sys.argv[1]
else:
    parser.channelsfiledata = 'channels.cfg'
parser.getcontent('channels.html')
parser.parsecontent_channels()
parser.save_channeldata()
