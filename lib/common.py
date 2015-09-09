# -*- coding: utf-8 -*-

import sys
import locale
import urllib2
import traceback

host = 'http://www.vsetv.com/'
useragent = 'Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.0'
contenttype = 'application/x-www-form-urlencoded'

debug = 'true'
repspecsym = 'true'
sort_by_index = 'true'

encoding = locale.getpreferredencoding(do_setlocale=True)
reload(sys)
sys.setdefaultencoding(encoding)
    
def dbg_log(vsource, vtext, vlevel=0):
    if debug == 'false':
        return
    if vlevel==0:
        print('NOTIFY:## Vse TV ## ' + vsource + ' ## ' + vtext)
    if vlevel==1:
        print('ERROR:## Vse TV ## ' + vsource + ' ## ' + vtext)
        print(traceback.format_exc())
        
def load_url(vurl):
    try:
        request = urllib2.Request(vurl)
        request.add_header('User-Agent', useragent)
        request.add_header('Content-Type', contenttype)
        response = urllib2.urlopen(request)
        content = response.read()
        return content.strip()
    except Exception, e:
        dbg_log('common::load_url(' + vurl + ')', 'ERROR: (' + repr(e) + ')', 1)
        
def remove_specsym(vstr):
    try: 
        dbg_log('common::remove_specsym', 'enter_function')
        rstr = vstr.strip('&nbsp;')
        rstr = rstr.replace('&amp;', '&')
        rstr = rstr.replace('&quot;','"')
        rstr = rstr.replace('&lt;', '<')
        rstr = rstr.replace('&gt;', '>')
        dbg_log('common::remove_specsym', 'exit_function')
        return rstr        
    except Exception, e:
        dbg_log('common::remove_specsym', 'ERROR: (' + repr(e) + ')', 1)
        return vstr

def save_xmlfile(vfilename, vxmldoc):
    try:
        dbg_log('common::save_xmlfile', 'enter_function')
        outputfile = open(vfilename, 'w')
        data = vxmldoc.toprettyxml(encoding='utf-8')
        if repspecsym == 'true':
            outputfile.write(remove_specsym(data))
        else:
            outputfile.write(data)
        outputfile.close() 
        dbg_log('common::save_xmlfile', 'exit_function')
    except Exception, e:
        dbg_log('common::save_xmlfile', 'ERROR: (' + repr(e) + ')', 1)