#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import ufunctions

vChannelFile = os.path.join(os.path.dirname(__file__), 'channels.cfg')
vXMLOut = os.path.join(os.path.dirname(__file__), 'xmltv.xml')
vCountDay = 1
vFullDesc = 'true'

if len(sys.argv) > 1:
    vChannelFile = sys.argv[1]
if len(sys.argv) > 2:
    vXMLOut = sys.argv[2]
if len(sys.argv) > 3:
    vCountDay = int(sys.argv[3])
if len(sys.argv) > 4:
    vFullDesc = sys.argv[4]

ufunctions.save_xmltv(vXMLOut, vCountDay, vFullDesc, vChannelFile)