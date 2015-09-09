# -*- coding: utf-8 -*-

import common
import channel
import parservsetv

def get_channels(vChannelFile, vLang):
    try:
        common.dbg_log('functions::get_channels', 'enter_function')
        chnlst = channel.channel_list(vChannelFile, vLang)
        chnlst.load_channels_from_net()
        chnlst.save_channels_to_file()
        common.dbg_log('functions::get_channels', 'exit_function')
    except Exception, e:
        common.dbg_log('functions::get_channels', 'ERROR: (' + repr(e) + ')', 1) 
        
def save_xmltv(vXMLOut, vCountDay=3, vFullDesc='false', vCfgFile='channels.cfg'):
    try:
        common.dbg_log('functions::save_xmltv', 'enter_function')
        prs = parservsetv.parser(vXMLOut, vCountDay, vFullDesc, vCfgFile)
        prs.get_content()
        prs.save_xml()
        common.dbg_log('functions::save_xmltv', 'exit_function')
    except Exception, e:
        common.dbg_log('functions::save_xmltv', 'ERROR: (' + repr(e) + ')', 1)