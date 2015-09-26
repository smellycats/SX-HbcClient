# -*- coding: utf-8 -*-
import time
import json
#import shutil

import requests
import grequests

import helper
from ini_conf import MyIni


class HbcCompare(object):

    def __init__(self):
        self.myini = MyIni()
        self.hbc_conf = self.myini.get_hbc()
        self.kakou_ini = {'host': '10.47.187.165', 'port': 80}
        self.cgs_ini = {'host': '10.47.222.45', 'port': 8080,
                        'username':'test1', 'password': 'test12345',
                        'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MzI1NjcyMiwiaWF0IjoxNDQzMjQ5NTIyfQ.eyJzY29wZSI6WyJzY29wZV9nZXQiLCJoemhiY19nZXQiXSwidWlkIjoyM30.Qga6zksBXBu8Aq9zVBb7tsR_vQFI4A7IfzdgMvGEfrw'}
        self.hbc_ini = {'host': '10.47.222.45', 'port': 8081,
                        'username':'test1', 'password': 'test12345',
                        'token': ''}
        self.id_flag = self.hbc_conf['id_flag']
        self.step = self.hbc_conf['step']
        self.kkdd = self.hbc_conf['kkdd']
        
        self.kakou_status = False
        self.cgs_status = False
        self.hbc_status = False
        # 黄标车集合
        self.hzhbc_set = set()

    def cgs_token(self):
        url = 'http://%s:%s/token' % (self.cgs_ini['host'], self.cgs_ini['port'])
        headers = {'content-type': 'application/json'}
        data = {'username': self.cgs_ini['username'],
                'password': self.cgs_ini['password']}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        if r.status_code == 200:
            self.cgs_ini['token'] = json.loads(r.text)['access_token']
            print json.loads(r.text)['access_token']
        else:
            self.cgs_status = False
            raise Exception('Cgs server error,%s,%s' % (r.status_code, r.text))

    def hbc_token(self):
        url = 'http://%s:%s/token' % (self.hbc_ini['host'], self.hbc_ini['port'])
        headers = {'content-type': 'application/json'}
        data = {'username': self.hbc_ini['username'],
                'password': self.hbc_ini['password']}
        r = requests.post(url, headers=headers, data=json.dumps(data))
        if r.status_code == 201:
            self.hbc_ini['token'] = r.text['access_token']
        else:
            self.hbc_status = False
            raise Exception('Hbc server error,%s,%s' % (r.status_code, r.text))

    def get_hzhbc_all(self):
        headers = {'content-type': 'application/json',
                   'access_token': self.cgs_ini['token']}
        url = 'http://%s:%s/hzhbc' % (self.cgs_ini['host'], self.cgs_ini['port'])
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                items = json.loads(r.text)['items']
                print 'hbc_num:%s' % len(items)
                for i in items:
                    self.hzhbc_set.add((i['hphm'], i['hpzl']))
            else:
                self.cgs_status = False
                raise Exception('Cgs server error,%s,%s' % (r.status_code, r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def get_cltxs(self):
        last_id = self.id_flag + self.step
        url = 'http://%s:%s/rest_hz_kakou/index.php/hcq/kakou/cltxs/%s/%s'%(self.kakou_ini['host'], self.kakou_ini['port'], self.id_flag, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('Kakou server error,%s,%s' % (r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_cltxmaxid(self):
        url = 'http://%s:%s/rest_hz_kakou/index.php/hcq/kakou/cltxmaxid'%(self.kakou_ini['host'], self.kakou_ini['port'])
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('Kakou server error,%s,%s' % (r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_hbc(self, hphm, hpzl):
        headers = {'content-type': 'application/json',
                   'access_token': self.cgs_ini['token']}
        url = 'http://%s:%s/hzhbc/%s/%s'%(self.cgs_ini['host'],
                                          self.cgs_ini['port'], hphm, hpzl)
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                return r.text
            else:
                self.cgs_status = False
                raise Exception('Cgs server error,%s,%s' % (r.status_code, r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def check_hbc_img_by_hphm(self, date, hphm):
        headers = {'content-type': 'application/json',
                   'access_token': self.hbc_ini['token']}
        url = 'http://%s:%s/hbc/img/%s/%s/%s' % (self.hbc_ini['host'],
                                             self.hbc_ini['port'],
                                             date, hphm, self.kkdd)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.hbc_status = False
                raise Exception('HbcStore server error,%s,%s' % (r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def add_hbc(self, data):
        url = 'http://%s:%s/hbc' % (self.hbc_ini['host'],
                                             self.hbc_ini['port'])
        headers = {'content-type': 'application/json',
                   'access_token': self.hbc_ini['token']}
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                return json.loads(r.text)
            else:
                self.hbc_status = False
                raise Exception('HbcStore server error,%s,%s' % (r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def cmpare_hbc(self):
        maxid = self.get_cltxmaxid()['maxid']
        if maxid <= self.id_flag:
            # 没有新的数据 返回1
            time.sleep(1)
            return 1
        carinfo = self.get_cltxs()
        if carinfo['total_count'] == 0:
            if self.id_flag + self.step < maxid:
                self.id_flag += self.step
            else:
                self.id_flag = maxid
            self.myini.set_hbc(self.id_flag)
            time.sleep(1)
            #print 'id_flag: %s' % self.id_flag
            return 0
        elif carinfo['total_count'] < self.step:
            time.sleep(1)

        # 黄标车检测 list
        # hbc_list = []
        for i in carinfo['items']:
            # 判断车牌是否需要黄标车查询
            f_hphm = helper.fix_hphm(i['hphm'], i['hpys_code'])
            if f_hphm['hpzl'] != '00':
                # 是否在黄标车集合里面
                if (f_hphm['hphm'], f_hphm['hpzl']) in self.hzhbc_set:
                    #print u'黄表车: %s, 号牌颜色: %s' % (i['hphm'], i['hpys'])
                    hbc_img = self.check_hbc_img_by_hphm(i['jgsj'][:10], i['hphm'])
                    imgpath = ''
                    if hbc_img['total_count'] == 0:
                        imgpath = 'D:\imgs\%s.jpg' % i['id']
                        helper.get_url_img(i['imgurl'], imgpath)
                        
                    data = {
                        'jgsj': i['jgsj'],
                        'hphm': i['hphm'],
                        'kkdd_id': i['kkdd_id'],
                        'hpys_code': i['hpys_code'],
                        'fxbh_code': i['fxbh_code'],
                        'cdbh': i['cdbh'],
                        'imgurl': i['imgurl'],
                        'imgpath': imgpath
                    }
                    self.add_hbc(data)
        self.id_flag = carinfo['items'][-1]['id']
        self.myini.set_hbc(self.id_flag)
        print 'id_flag: %s' % self.id_flag
        return -1

    def main_loop(self):
        hbc = HbcCompare()
        hbc.get_hzhbc_all()
        while 1:
            hbc.cmpare_hbc()
            #time.sleep(0.5)
        del hbc
        

if __name__ == "__main__":
    hbc = HbcCompare()
    hbc.main_loop()
    del hbc

