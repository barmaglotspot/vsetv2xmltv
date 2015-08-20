# -*- coding: utf-8 -*-

from grab import Grab
import sys
import os
import logging
import datetime
import re
from lxml import etree

class channel_data(object):
    __slots__ = ('Name', 'Index', 'IconURL', 'UserName', 'UserIconURL', 'Correction')

    def __init__(self, vName, vIndex='0', vIconURL='None', vUserName='None', vUserIconURL='None', vCorrection=120):        
        self.Name = vName
        self.Index = vIndex
        self.IconURL = vIconURL
        self.UserName = vUserName
        self.UserIconURL = vUserIconURL
        self.Correction = vCorrection

    def getxml(self, vroot):        
        echannel = etree.SubElement(vroot, 'channel')
        echannel.set('id', self.Index)
        edisplayname = etree.SubElement(echannel, 'display-name')
        edisplayname.set('lang', 'ru')
        if self.UserName == 'None':
            edisplayname.text = self.Name.decode('utf-8')            
        else:
            edisplayname.text = self.UserName.decode('utf-8')            
        eiconlink = etree.SubElement(echannel, 'icon')       
        if self.UserIconURL == 'None':
            eiconlink.set('src', self.IconURL.decode('utf-8'))            
        else:
            eiconlink.set('src', self.UserIconURL.decode('utf-8'))            
        return 0


class programme_data(object):
    __slots__ = ('ChannelIdx', 'Start', 'Stop', 'Title', 'Desc', 'FullDesc', 'CategoryLang1', 'CategoryLang2', 'Directors', 'Actors', 'Date', 'Starrating')

    def __init__(self, vChannelIdx, vStart, vTitle, vStop='', vDesc='', vFullDesc='', vCategoryLang1='', vCategoryLang2='', vDirectors='', vActors='', vDate='', vStarrating=''):        
        self.ChannelIdx = vChannelIdx
        self.Start = vStart
        self.Stop = vStop
        self.Title = vTitle
        self.Desc = vDesc
        self.FullDesc = vFullDesc
        self.CategoryLang1 = vCategoryLang1
        self.CategoryLang2 = vCategoryLang2
        self.Directors = vDirectors
        self.Actors = vActors
        self.Date = vDate
        self.Starrating = vStarrating

    def getxml(self, vroot, visfulldesc):        
        astr = ''
        eprogramme = etree.SubElement(vroot, 'programme')
        eprogramme.set('start', self.Start)
        eprogramme.set('stop', self.Stop)
        eprogramme.set('channel', self.ChannelIdx)
        etittle = etree.SubElement(eprogramme, 'title')
        etittle.set('lang', 'ru')
        etittle.text = self.Title.decode('utf-8')        
        if visfulldesc == True:            
            if self.FullDesc != '':
                edesc = etree.SubElement(eprogramme, 'desc')
                edesc.set('lang', 'ru')
                edesc.text = self.FullDesc.decode('utf-8')
        else:            
            if self.Desc != '':
                edesc = etree.SubElement(eprogramme, 'desc')
                edesc.set('lang', 'ru')
                edesc.text = self.Desc.decode('utf-8')
        if (self.Directors != '') or (self.Actors != ''):
            ecredits = etree.SubElement(eprogramme, 'credits')            
            if self.Directors != '':
                strlist = self.Directors.split(',')                
                for astr in strlist:
                    edirector = etree.SubElement(ecredits, 'director')
                    edirector.text = astr.strip().decode('utf-8')                    
            if self.Actors != '':
                strlist = self.Actors.split(',')                
                for astr in strlist:
                    eactor = etree.SubElement(ecredits, 'actor')
                    eactor.text = astr.strip().decode('utf-8')
        if self.Date != '':
            edate = etree.SubElement(eprogramme, 'date')
            edate.text = self.Date                
        if self.CategoryLang2 != '':
            ecategoryen = etree.SubElement(eprogramme, 'category')
            ecategoryen.set('lang', 'en')
            ecategoryen.text = self.CategoryLang2.decode('utf-8')            
        if self.CategoryLang1 != '':
            strlist = self.CategoryLang1.split(',')
            for astr in strlist:
                astr = astr[0].upper()+astr[1:]
                ecategory = etree.SubElement(eprogramme, 'category')
                ecategory.set('lang', 'ru')
                ecategory.text = astr.decode('utf-8')           
        if self.Starrating != '':
            erating = etree.SubElement(eprogramme, 'star-rating')
            evalue = etree.SubElement(erating, 'value')
            evalue.text = self.Starrating            
        return 0

class parser_vsetv(object):
    __slots__ = ('ahost', 'alogdir', 'acharset', 'flogger', 'fgrab', 'fgrabdesc', 'fchanneldata', 'fprogrammedata', 'channelsfiledata', 'currentdata', 'isfulldesc', 'outxml')

    def __init__(self, vhost, vlogdir, vcharset):        
        self.ahost = vhost
        self.flogger = logging.getLogger('grab')
        self.flogger.addHandler(logging.StreamHandler())
        self.flogger.setLevel(logging.DEBUG)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.alogdir = vlogdir
        self.acharset = vcharset
        self.fgrab = Grab()
        self.fgrab.setup(log_dir=self.alogdir, charset=self.acharset)
        self.fgrabdesc = Grab()
        self.fgrabdesc.setup(log_dir=self.alogdir, charset=self.acharset)
        self.fchanneldata = []
        self.fprogrammedata = []
        self.channelsfiledata = os.path.join(os.path.dirname(__file__), 'channels.cfg')
        self.outxml = os.path.join(os.path.dirname(__file__), 'xmltv.xml')
        self.currentdata = datetime.datetime.now()
        self.isfulldesc = True

    def getcontent(self, vdirection, desc=0):        
        if desc == 0:
            self.fgrab = Grab()
            self.fgrab.setup(log_dir=self.alogdir, charset=self.acharset)
            self.fgrab.go(self.ahost + vdirection)            
        else:
            self.fgrabdesc = Grab()
            self.fgrabdesc.setup(log_dir=self.alogdir, charset=self.acharset)
            self.fgrabdesc.go(self.ahost + vdirection)            
        return 0

    def parsecontent_channels(self):        
        i = 0
        cname = ''
        clink = ''
        cicon = ''        
        for node in self.fgrab.doc.select('//td[@valign="top"]'):
            try:
                cname = node.select('.//span[@class="name"]').text()
                clink = node.select('.//a').attr('href')
                clink = clink.split('_')[2]
                cicon = self.ahost + 'pic/channel_logos/' + clink + '.gif'
                dc = channel_data(cname, clink, cicon)
                self.fchanneldata.append(dc)
                i += 1               
            except Exception:
                pass           
        return i

    def save_channeldata(self):        
        i = 0
        outputfile = open(self.channelsfiledata, 'w')        
        for dc in self.fchanneldata:
            line = dc.Index + ';' + dc.Name + ';' + dc.IconURL + ';' + dc.UserName + ';' + dc.UserIconURL + ';' + str(dc.Correction)
            # print line
            outputfile.write(line + '\n')
            i += 1            
        outputfile.close()        
        return i

    def load_channeldata(self):        
        self.fchanneldata = []
        i = 0        
        if os.path.exists(self.channelsfiledata):
            inputfile = open(self.channelsfiledata, 'r')            
            for line in inputfile:
                if line != '':                    
                    listStr = line.strip().split(';')                    
                    try:
                        dc = channel_data(listStr[1], listStr[0], listStr[2], listStr[3], listStr[4], int(listStr[5]))
                        self.fchanneldata.append(dc)                        
                    except Exception, e:
                        print 'ERROR: (%s)' % repr(e)
                    i += 1
            inputfile.close()            
        else:
            print 'Not found file ' + self.channelsfiledata            
        return i

    def addzero(self, vvalue):        
        if vvalue < 10:
            avalue = '0' + str(vvalue)            
        else:
            avalue = str(vvalue)            
        return avalue

    def removetags(self, vstr):        
        rstr = re.sub('<([^!>]([^>]|\n)*)>', '', vstr)
        re.sub(r'[^\x00-\x7F]',' ', rstr)
        return rstr

    def parse_strings(self, vstr, vbegin, vend):        
        idx_beg = vstr.find(vbegin)
        idx_end = vstr.find(vend)
        tstr = vstr[idx_beg:idx_end]
        rstr = self.removetags(tstr)
        return rstr.strip(' \t\n\r')

    def get_datetime_str(self, vdate, vtype):        
        ayear = vdate.year
        amonthstr = self.addzero(vdate.month)
        adaystr = self.addzero(vdate.day)        
        if vtype == 0:
            adate = str(ayear) + '-' + amonthstr + '-' + adaystr            
        else:
            adate = str(ayear) + amonthstr + adaystr            
        return adate

    def get_datetime_fmt(self, vdate, vtimestr, correction):       
        # Даты начала передачи (start) и окончания передачи (stop) описываются в формате "YmdHis P",
        # где Y — год (4-значный), m — месяц (от 01 до 12), d — день (от 01 до 31), H — час (от 00 до 23), i — минута (от 00 до 59), s — секунда (от 00 до 59),
        # P — смещение по часовому поясу (+0400 — соответствует Московскому времени).
        # 2013 11 25 14 40 00 +0200
        vdatestr = self.get_datetime_str(vdate, 1)
        ahourstr = vtimestr.strip().split(':')[0]
        aminstr = vtimestr.strip().split(':')[1]
        asecstr = vtimestr.strip().split(':')[2]
        vdatestr = vdatestr + ahourstr + aminstr + asecstr
        crh = correction // 60
        crm = correction - crh * 60        
        if crh >= 0:
            dstr = '+' + self.addzero(crh) + self.addzero(crm)            
        else:
            dstr = '-' + self.addzero(crh) + self.addzero(crm)            
        vdatestr = vdatestr + ' ' + dstr        
        return vdatestr

    def get_parsefulldescription(self, vurlfdesc, vprogrammedata):        
        if vurlfdesc != '':            
            self.getcontent(vurlfdesc, 1)
            # get date and genre
            cdate = ''
            ccountry = ''
            ctmp = ''            
            try:
                node = self.fgrabdesc.doc.select('//td[@class="showname"]')                
                if node.html().find('<strong>') != -1:
                    ctmp = self.parse_strings(node.html(), '<br>', '<strong>').strip(',')                    
                else:
                    ctmp = self.parse_strings(node.html(), '<br>', '<!--').strip(',')
                if len(ctmp.split(','))==2:                     
                    ccountry = ctmp.split(',')[0].strip()
                    cdate = ctmp.split(',')[1].strip()
                    if cdate[-1] == '-':
                        cdate = cdate[:-1]           
                    if cdate != '':
                        ctmp = ccountry + ', ' + cdate
                        vprogrammedata.Date = cdate
            except:
                ctmp = ''
                cgenre = ''
                cdate = ''                
            try:                                
                cgenre = node.select('.//strong').text().replace(' / ', ',')                
                if cgenre != '':
                    if vprogrammedata.CategoryLang1 != '':
                        vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',' + cgenre
                    else:
                        vprogrammedata.CategoryLang1 = cgenre                        
            except Exception:           
                cgenre = ''                
            cdirectors = ''
            cactors = ''
            cdesc = ''            
            try:
                node = self.fgrabdesc.doc.select('//td[@class="showmain"]')
                cdirectors = self.parse_strings(node.html(), 'Режиссер(ы):', '<br>')                
                if cdirectors != '':
                    vprogrammedata.Directors = cdirectors[12:]
                cactors = self.parse_strings(node.html(), 'Актеры:', '<div>')                
                if cactors != '':
                    vprogrammedata.Actors = cactors[7:] 
                cdesc = self.removetags(node.select('.//span[@class="big"]').text()).strip()                
                if cdesc != '':
                    if ctmp != '':
                        vprogrammedata.FullDesc = ctmp.strip() + '. ' + cdesc                        
                    else:
                        vprogrammedata.FullDesc = cdesc                        
            except Exception:
                cdirectors = ''
                cactors = ''
                cdesc = ''                
            crat = ''            
            try:                
                node = self.fgrabdesc.doc.select('//span[@class="name"]')
                crat = node.text().split(':')[1].strip()                
                if crat != '':
                    vprogrammedata.Starrating = crat
            except Exception:
                crat = ''                
        return 0

    def get_parsecategory(self, vprogrammedata):       
        vtitle = vprogrammedata.Title.lower()
        if (vtitle.find('х/ф') != -1) or (vtitle.find('д/ф') != -1) or (vtitle.find('Х/ф') != -1) or (vtitle.find('Д/ф') != -1):
            if vprogrammedata.CategoryLang1 != '':
                vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',Фильм'
            else:
                vprogrammedata.CategoryLang1 = 'Фильм'
            vprogrammedata.CategoryLang2 = 'Movie / Drama'            
        elif (vtitle.find('т/с') != -1) or (vtitle.find('х/с') != -1) or (vtitle.find('д/с') != -1) or \
        (vtitle.find('Т/с') != -1) or (vtitle.find('Х/с') != -1) or (vtitle.find('Д/с') != -1):
            if vprogrammedata.CategoryLang1 != '':
                vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',Cериал'
            else:
                vprogrammedata.CategoryLang1 = 'Cериал'
            vprogrammedata.CategoryLang2 = 'Movie / Drama'            
        elif (vtitle.find('м/ф') != -1) or (vtitle.find('м/с') != -1) or (vtitle.find('М/ф') != -1) or (vtitle.find('М/с') != -1) or (vtitle.find('мульт') != -1):
            if vprogrammedata.CategoryLang1 != '':
                vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',Детский'
            else:
                vprogrammedata.CategoryLang1 = 'Детский'
            vprogrammedata.CategoryLang2 = 'Cartoons / Puppets'            
        elif (vtitle.find('спорт') != -1) or (vtitle.find('футбол') != -1) or (vtitle.find('хоккей') != -1) or (vtitle.find('uefa') != -1):
            if vprogrammedata.CategoryLang1 != '':
                vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',Спорт'
            else:
                vprogrammedata.CategoryLang1 = 'Спорт'
            vprogrammedata.CategoryLang2 = 'Sports'            
        elif (vtitle.find('новост') != -1) or (vtitle.find('Новост') != -1) or (vtitle.find('факты') != -1) or (vtitle.find('тсн') != -1) or \
        (vtitle.find('новини') != -1) or (vtitle.find('время') != -1) or (vtitle.find('известия') != -1):
            if vprogrammedata.CategoryLang1 != '':
                vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',Новости'
            else:
                vprogrammedata.CategoryLang1 = 'Новости'
            vprogrammedata.CategoryLang2 = 'News / Current affairs'            
        elif (vtitle.find('истори') != -1) or (vtitle.find('планет') != -1) or (vtitle.find('разрушители') != -1) or (vtitle.find('знаки') != -1) or (vtitle.find('катастроф') != -1):
            if vprogrammedata.CategoryLang1 != '':
                vprogrammedata.CategoryLang1 = vprogrammedata.CategoryLang1 + ',Досуг'
            else:
                vprogrammedata.CategoryLang1 = 'Досуг'
            vprogrammedata.CategoryLang2 = 'Leisure hobbies'            
        else:
            vprogrammedata.CategoryLang2 = ''
        return 0

    def parsecontent_programme_all(self, vcntday):
        try:
        
            for dc in self.fchanneldata:
                nowdt = datetime.datetime.now()
                curdt = nowdt           
                while curdt != nowdt + datetime.timedelta(days=vcntday):
                    self.parsecontent_programme(dc, curdt)
                    curdt = curdt + datetime.timedelta(days=1)                
            return 0 
        except Exception, e:
            print 'ERROR: (%s)' % repr(e)


    def parsecontent_programme(self, vchanneldata, vdate):        
        vdirection = 'schedule_channel_%s_day_%s.html' % (vchanneldata.Index, self.get_datetime_str(vdate, 0))
        self.getcontent(vdirection)        
        i = 0
        ltime = '00:00'
        ctimeb = '00:00'
        ctimee = '00:00'
        ctitle = ''
        cdesc = ''
        curlfdesc = ''        
        for node in self.fgrab.doc.select('//div[@class="pasttime" or @class="onair" or @class="time"]'):            
            try:
                ctimeb = node.text()
                if ctimeb < ltime:
                    vdate = vdate + datetime.timedelta(days=1)                    
                ltime = ctimeb
                ctimeb = self.get_datetime_fmt(vdate, ctimeb + ':00', vchanneldata.Correction)
                ctimee = self.get_datetime_fmt(vdate, '23:59:59', vchanneldata.Correction)
                nodetitle = node.select('.//following-sibling::div[@class="pastprname2" or @class="prname2"]')
                ctitle = self.removetags(nodetitle.text()).replace('&amp;', '&').strip()
                dp = programme_data(vchanneldata.Index, ctimeb, ctitle, ctimee)
                self.get_parsecategory(dp)
                i += 1                
                try:                                        
                    if self.isfulldesc == True :
                        # get link for full description
                        curlfdesc = nodetitle.select('.//a').attr('href') 
                        # get full description  
                        self.get_parsefulldescription(curlfdesc, dp)
                    else:                                         
                        # get short description
                        cdesc = node.select('.//following-sibling::div[@class="prdesc" and position()=2]').html().replace('<br>', ' ')
                        cdesc = self.removetags(cdesc).strip()
                        dp.Desc = cdesc                                            
                except Exception:
                    curlfdesc = ''
                    cdesc = ''                    
                self.fprogrammedata.append(dp)                
            except Exception:
                ctimeb = '00:00'
                ctimee = '00:00'
                ctitle = ''                
        return i

    def save_xmltv(self):        
        root = etree.Element('tv')
        root.set('generator-info-name', 'vsetv_grab')        
        for channel in self.fchanneldata:
            channel.getxml(root)            
        for programme in self.fprogrammedata:
            programme.getxml(root, self.isfulldesc)            
        handle = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        ftvxml = open(self.outxml, 'w')
        ftvxml.writelines(handle)
        ftvxml.close()        
        return 0

    def set_programmestop(self):        
        i = 0        
        while i != len(self.fprogrammedata):            
            dp1 = self.fprogrammedata[i]            
            if i + 1 != len(self.fprogrammedata):
                dp2 = self.fprogrammedata[i + 1]                
                if dp1.ChannelIdx == dp2.ChannelIdx:
                    dp1.Stop = dp2.Start                   
            i += 1
        return 0
