# -*- coding: utf-8 -*-
import json

#from helper_kakou import Kakou
from helper_kakou2 import Kakou as Kakou2
from helper_hbc import Hbc
#from helper_sms import SMS
from ini_conf import MyIni


class KakouTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        self.kakou = Kakou(**self.my_ini.get_kakou())

    def get_maxid(self):
        print self.kakou.get_maxid()

    def get_cltxs(self):
        print self.kakou.get_cltxs(377804199, 377804204)

    def get_bkcp_by_hphm(self):
        print self.kakou.get_bkcp_by_hphm(u'粤LXX266')


class SMSTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        self.sms = SMS(**self.my_ini.get_sms())

    def get_sms(self):
        content = u'广东实现'
        mobiles = ['15819851862']
        print self.sms.sms_send(content, mobiles)


class KakouTest2(object):
    def __init__(self):
        self.my_ini = MyIni()
        print self.my_ini.get_kakou()
        self.kakou = Kakou2(**self.my_ini.get_kakou())

    def get_maxid(self):
        print self.kakou.get_maxid()

    def get_cltxs(self):
        print self.kakou.get_kakou(278668962, 278668963)

    def get_bkcp_by_hphm(self):
	#print self.kakou.get_bkcp()
        print self.kakou.get_bkcp(u'粤LXX266')

class HbcTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        print self.my_ini.get_hbc()
        self.hbc = Hbc(**self.my_ini.get_hbc())

    def get_que(self):
        print self.hbc.que_get()

if __name__ == '__main__':
    #kt = KakouTest()
    #kt.get_maxid()
    #kt.get_cltxs()
    #kt.get_bkcp_by_hphm()
    #st = SMSTest()
    #st.get_sms()
    kt2 = KakouTest2()
    kt2.get_maxid()
    kt2.get_cltxs()
    #kt2.get_bkcp_by_hphm()
    #ht = HbcTest()
    #ht.get_que()
    
