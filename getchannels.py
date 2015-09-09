#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import ufunctions

vChannelFile = os.path.join(os.path.dirname(__file__), 'channels.cfg')
if len(sys.argv) > 1:
    vChannelFile = sys.argv[1]

ufunctions.get_channels(vChannelFile, 'ru')