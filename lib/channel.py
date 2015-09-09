# -*- coding: utf-8 -*-

import os
import re
import common

class channel:
    __slots__ = ('Index', 'OName', 'UName', 'Icon', 'Correction')

    def __init__(self, vIndex, vOName, vUName='None', vIcon='None', vCorrection=120):
        try:
            self.Index = vIndex
            self.OName = vOName
            self.UName = vUName
            self.Icon = vIcon
            self.Correction = vCorrection
        except Exception, e:
            common.dbg_log('channel::__init__', 'ERROR: (' + repr(e) + ')', 1)

    def get_xml(self, vxmldoc, vnode):
        try:
            common.dbg_log('channel::get_xml', 'enter_function')
            echannel = vxmldoc.createElement("channel")
            echannel.setAttribute("id", self.Index)
            edisplayname = vxmldoc.createElement("display-name")
            edisplayname.setAttribute("lang", 'ru')
            if self.UName == 'None':
                edisplayname_text = vxmldoc.createTextNode(self.OName.decode('utf-8'))            
            else:
                edisplayname_text = vxmldoc.createTextNode(self.UName.decode('utf-8')) 
            edisplayname.appendChild(edisplayname_text) 
            echannel.appendChild(edisplayname)
            if self.Icon != 'None':
                eiconlink = vxmldoc.createElement("icon")       
                eiconlink.setAttribute("src", self.Icon)
                echannel.appendChild(eiconlink)
            vnode.appendChild(echannel)
            common.dbg_log('channel::get_xml', 'exit_function')
        except Exception, e:
            common.dbg_log('channel::get_xml', 'ERROR: (' + repr(e) + ')', 1)

class channel_list:
    __slots__ = ('Data', 'Lang', 'CfgFile')

    def __init__(self, vCfgFile='channels.cfg', vLang='ru'):
        try:
            self.Data = []            
            self.CfgFile = vCfgFile
            self.Lang = vLang
        except Exception, e:
            common.dbg_log('channel_list::__init__', 'ERROR: (' + repr(e) + ')', 1)

    def load_channels_from_net(self):
        try:
            common.dbg_log('channel_list::load_channel_from_net', 'enter_function')
            self.Data = []
            html = common.load_url(common.host+'channels.html')
            html = html.decode('windows-1251').encode('utf-8')
            datalst = re.compile('<option value=channel_(.+?)>(.+?)</option>').findall(html)
            for index,oname in datalst:
                if self.Lang == 'ru':
                    flag = oname.find('(на укр.)') == -1
                else:
                    flag = oname.find('(на укр.)') != -1
                if flag:
                    icon = common.host + 'pic/channel_logos/' + index + '.gif'
                    chn = channel(index, oname.decode('utf-8'), oname.decode('utf-8'), icon)
                    self.Data.append(chn)
                    common.dbg_log('channel_list::load_channel_from_net', oname.decode('utf-8'))
            if common.sort_by_index == 'true':
                self.Data.sort(key = lambda x: int(x.Index))
            common.dbg_log('channel_list::load_channel_from_net', 'exit_function')
        except Exception, e:
            common.dbg_log('channel_list::load_channel_from_net', 'ERROR: (' + repr(e) + ')', 1)
            
    def save_channels_to_file(self):
        try:      
            common.dbg_log('channel_list::save_channels_to_file', 'enter_function')
            outputfile = open(self.CfgFile, 'w')        
            for dc in self.Data:
                line = dc.Index + ';' + dc.OName.encode('utf-8') + ';' + dc.UName.encode('utf-8') + ';' + dc.Icon + ';' + str(dc.Correction)
                outputfile.write(line + '\n')         
            outputfile.close() 
            common.dbg_log('channel_list::save_channels_to_file', 'exit_function')       
        except Exception, e:
            common.dbg_log('channel_list::save_channels_to_file', 'ERROR: (' + repr(e) + ')', 1)
            
    def load_channels_from_file(self):
        try:
            common.dbg_log('channel_list::load_channel_from_file', 'enter_function')
            self.Data = []       
            if os.path.exists(self.CfgFile):
                inputfile = open(self.CfgFile, 'r')            
                for line in inputfile:
                    if line != '':                    
                        listStr = line.strip().split(';')                    
                        try:
                            dc = channel(listStr[0], listStr[1], listStr[2], listStr[3], int(listStr[4]))
                            self.Data.append(dc)                        
                        except Exception, e:
                            common.dbg_log('channel_list::load_channel_from_file', 'ERROR: (' + repr(e) + ')', 1)
                inputfile.close()            
            else:
                common.dbg_log('channel_list::load_channel_from_file', 'File not found', 1) 
            common.dbg_log('channel_list::load_channel_from_file', 'exit_function')       
        except Exception, e:
            common.dbg_log('channel_list::load_channel_from_file', 'ERROR: (' + repr(e) + ')', 1)

    def get_xml(self, vxmldoc, vnode):
        try:
            common.dbg_log('channel_list::get_xml', 'enter_function')
            for chn in self.Data:
                chn.get_xml(vxmldoc, vnode)
            common.dbg_log('channel_list::get_xml', 'exit_function')
        except Exception, e:
            common.dbg_log('channel_list::get_xml', 'ERROR: (' + repr(e) + ')', 1)
