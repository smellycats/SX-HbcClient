# -*- coding: utf-8 -*-
import os
import time
import json
#import shutil

import requests
import grequests

import helper
from ini_conf import MyIni
from my_logger import debug_logging

debug_logging(u'logs/error.log')

logger = logging.getLogger('root')

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

        self.hpys5 = {'WT':u'白底黑字','YL':u'黄底黑字',
                      'BU':u'蓝底白字','BK':u'黑底白字','QT':u'其他'}
        self.floder2 = {
            '441302101': u'462',
            '441302102': u'461',
            '441302103': u'458',
            '441302104': u'460',
            '441302105': u'459',
            '441302106': u'457'
        }
        self.fxbh3 = {
            'NS': u'北向南',
            'SN': u'南向北',
            'EW': u'东向西',
            'WE': u'西向东',
            'IN': u'东向西',
            'OT': u'西向东'
        }
        self.city = {
            '441302': 'hcq',
            '441303': 'hy',
            '441322': 'bl'
            '441323': 'hd',
            '441324': 'lm',
            '441333': 'dyw'
        }
        self.img_file = 'd://videoandimage'

    def cgs_token(self):
        url = 'http://%s:%s/token' % (self.cgs_ini['host'],
                                      self.cgs_ini['port'])
        headers = {'content-type': 'application/json'}
        data = {'username': self.cgs_ini['username'],
                'password': self.cgs_ini['password']}
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 200:
                self.cgs_ini['token'] = json.loads(r.text)['access_token']
                #print json.loads(r.text)['access_token']
            else:
                self.cgs_status = False
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def hbc_token(self):
        url = 'http://%s:%s/token' % (self.hbc_ini['host'],
                                      self.hbc_ini['port'])
        headers = {'content-type': 'application/json'}
        data = {'username': self.hbc_ini['username'],
                'password': self.hbc_ini['password']}
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                self.hbc_ini['token'] = json.loads(r.text)['access_token']
            else:
                self.hbc_status = False
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def get_hzhbc_all(self):
        headers = {'content-type': 'application/json',
                   'access_token': self.cgs_ini['token']}
        url = 'http://%s:%s/hzhbc' % (self.cgs_ini['host'],
                                      self.cgs_ini['port'])
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                items = json.loads(r.text)['items']
                print 'hbc_num:%s' % len(items)
                for i in items:
                    self.hzhbc_set.add((i['hphm'], i['hpzl']))
            else:
                self.cgs_status = False
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def get_cltxs(self):
        last_id = self.id_flag + self.step
        url = 'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/cltxs/%s/%s'
              %(self.kakou_ini['host'], self.kakou_ini['port'],
                self.city.get(self.kkdd, 'hz'), self.id_flag, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_cltxmaxid(self):
        url = 'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/cltxmaxid'
              % (self.kakou_ini['host'], self.kakou_ini['port'],
                 self.city.get(self.kkdd, 'hz'))
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
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
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
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
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    #根据URL地址获取图片到本地
    def get_img_by_url(self,url,path,name):
        try:
            imgpath = u'%s/%s.jpg' % (path, name)
            helper.get_url_img(url, imgpath)
        except IOError,e:
            print e
            if e[0]== 2 or e[0]==22:
                name = name.replace('*','_').replace('?','_').replace('|','_').replace('<','_').replace('>','_').replace('/','_').replace('\\','_')
                self.makedirs(path)
                imgpath = u'%s/%s.jpg' % (path, name)
                #urllib.urlretrieve(url,local)
                helper.get_url_img(url, imgpath)
            else:
                imgpath = ''
                raise
        except Exception as e:
            print (e)
            raise
        finally:
            return imgpath

    #创建文件夹
    def makedirs(self, path):
        try:
            if os.path.isdir(path):
                pass
            else:
                os.makedirs(path)
        except IOError,e:
            logging.exception(e)
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
                    jgsj = arrow.get(i['jgsj'])
                    #print u'黄表车: %s, 号牌颜色: %s' % (i['hphm'], i['hpys'])
                    hbc_img = self.check_hbc_img_by_hphm(jgsj.format('YYYY-MM-DD'), i['hphm'])
                    imgpath = ''
                    if hbc_img['total_count'] == 0:
                        try:
                            #path = u'd://videoandimage/'+u'%s年%s月%s日'%(i['jgsj'][:4], i['jgsj'][5:7], i['jgsj'][8:10])+u'/'+u'违章图片目录'
                            path = u'%s/%s/违章图片目录' % (self.img_file, jgsj.format('YYYY年MM月DD日'))
                            #name = u'机号'+self.floder2[i['kkdd_id']]+u'车道A'+str(i['cdbh'])+jgsj.format('YYYY年MM月DD日HH时mm分ss秒')+u'R454DOK3'+u'T'+f_hphm['cpzl']+u'C'+self.hpys5[i['hpys_code']]+u'P'+i['hphm']+u'驶向'+self.fxbh3.get(i['fxbh_code'],u'无')+u'违章黄标车违反禁令标志'
                            name = u'机号%s车道A%s%sR454DOK3T%sC%sP%s驶向%s违章黄标车违反禁令标志'
                                    % (self.floder2[i['kkdd_id']], i['cdbh'],
                                       jgsj.format('YYYY年MM月DD日HH时mm分ss秒'),
                                       f_hphm['cpzl'], self.hpys5[i['hpys_code']],
                                       i['hphm'], self.fxbh3.get(i['fxbh_code'], u'无'))
                            imgpath = self.get_img_by_url(i['imgurl'], path, name)
                        except Exception as e:
                            logger.error('url: %s' % i['imgurl'])
                            logger.error(e)
                            imgpath = ''
                        
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
        #hbc.get_hzhbc_all()
        # 加载初始化数据
        init_flag = False
        while 1:
            if not init_flag:
                try:
                    hbc.get_hzhbc_all()
                    init_flag = True
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            elif self.kakou_status and self.cgs_status and self.hbc_status:
                try:
                    hbc.cmpare_hbc()
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            else:
                try:
                    if not self.kakou_status:
                        self.get_cltxmaxid()
                        self.kakou_status = True
                    if not self.cgs_status:
                        self.get_hzhbc_all()
                        self.cgs_status = True
                    if not self.hbc_status:
                        self.check_hbc_img_by_hphm('2015-09-26', u'粤L12345')
                        self.hbc_status = True
                except Exception as e:
                    print (e)
                    time.sleep(1)
        del hbc
        

if __name__ == "__main__":
    hbc = HbcCompare()
    hbc.main_loop()
    del hbc

