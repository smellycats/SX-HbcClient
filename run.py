# -*- coding: utf-8 -*-
import os
import time
import json
#import shutil
import logging
import cStringIO

import requests
import grequests
from PIL import Image

import helper
import helper_wm
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
                        'username': 'test1', 'password': 'test12345',
                        'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MzI1NjcyMiwiaWF0IjoxNDQzMjQ5NTIyfQ.eyJzY29wZSI6WyJzY29wZV9nZXQiLCJoemhiY19nZXQiXSwidWlkIjoyM30.Qga6zksBXBu8Aq9zVBb7tsR_vQFI4A7IfzdgMvGEfrw'}
        self.hbc_ini = {'host': '10.47.222.45', 'port': 8081,
                        'username': 'test1', 'password': 'test12345',
                        'token': ''}
        self.cgs2_ini = {'host': '10.47.222.45', 'port': 8081}
        self.id_flag = self.hbc_conf['id_flag']
        self.step = self.hbc_conf['step']
        self.kkdd = self.hbc_conf['kkdd']
        self.city = self.hbc_conf['city']

        self.kakou_status = False
        self.cgs_status = False
        self.cgs2_status = False
        self.hbc_status = False
        # 黄标车集合 set
        self.hzhbc_set = set()
        # 号牌颜色字典 dict
        self.hpys_dict = {
            'WT': u'白底黑字',
            'YL': u'黄底黑字',
            'BU': u'蓝底白字',
            'BK': u'黑底白字',
            'QT': u'其他'
        }
        # 机号字典 dict
        self.jh_dict = {}
        # 设备代号 dict
        self.sbdh_dict = {}
        self.fxbh_dict = {
            'NS': u'北向南',
            'SN': u'南向北',
            'EW': u'东向西',
            'WE': u'西向东',
            'IN': u'东向西',
            'OT': u'西向东'
        }
        self.city_dict = {
            '441302': 'hcq',
            '441303': 'hy',
            '441305': 'dyw',
            '441322': 'bl',
            '441323': 'hd',
            '441324': 'lm',
        }
        self.hbc_img_path = self.hbc_conf['hbc_img_path']#u'd://videoandimage'
        self.wz_img_path = self.hbc_conf['wz_img_path']

        self.hbc_img = helper.hbc_img()

    def cgs_token(self):
        url = 'http://%s:%s/token' % (self.cgs_ini['host'], self.cgs_ini['port'])
        headers = {'content-type': 'application/json'}
        data = {
            'username': self.cgs_ini['username'],
            'password': self.cgs_ini['password']
        }
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 200:
                self.cgs_ini['token'] = json.loads(r.text)['access_token']
                # print json.loads(r.text)['access_token']
            else:
                self.cgs_status = False
                raise Exception('url: %s, status: %s, %s' % (url, r.status_code, r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def hbc_token(self):
        url = 'http://%s:%s/token' % (self.hbc_ini['host'], self.hbc_ini['port'])
        headers = {'content-type': 'application/json'}
        data = {
            'username': self.hbc_ini['username'],
            'password': self.hbc_ini['password']
        }
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                self.hbc_ini['token'] = json.loads(r.text)['access_token']
            else:
                self.hbc_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def get_hzhbc_by_hphm(self):
        headers = {
            'content-type': 'application/json',
            'access_token': self.cgs2_ini['token']
        }
        url = u'http://%s:%s/rest_cgs/index.php/v2/hbc/hbc?q=粤L12345+hpzl:02' % (
            self.cgs2_ini['host'], self.cgs2_ini['port'])
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                pass
            else:
                self.cgs2_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.cgs2_status = False
            raise

    def get_hzhbc_all(self):
        headers = {
            'content-type': 'application/json',
            'access_token': self.cgs2_ini['token']
        }
        url = 'http://%s:%s/rest_cgs/index.php/v2/hbc/hbcall' % (
            self.cgs2_ini['host'], self.cgs2_ini['port'])
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                # 清空黄标车信息
                self.hzhbc_set = set()
                #items = json.loads(r.text)['items']
                for i in json.loads(r.text)['items']:
                    self.hzhbc_set.add((i['hphm'], i['hpzl']))
            else:
                self.cgs2_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.cgs2_status = False
            raise

    def get_hzhbc_all2(self):
        headers = {
            'content-type': 'application/json',
            'access_token': self.cgs_ini['token']
        }
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
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def get_cltxs(self):
        last_id = self.id_flag + self.step
        url = 'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/cltxs/%s/%s' % (
            self.kakou_ini['host'], self.kakou_ini['port'], self.city,
            self.id_flag, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_cltxmaxid(self):
        url = 'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/cltxmaxid' % (
            self.kakou_ini['host'], self.kakou_ini['port'], self.city)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_kkdd(self):
        url = 'http://%s:%s/kkdd/%s' % (
            self.hbc_ini['host'], self.hbc_ini['port'], self.kkdd)
        headers = {
            'content-type': 'application/json',
            'access_token': self.hbc_ini['token']
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                items = json.loads(r.text)['items']
                for i in items:
                    self.jh_dict[i['kkdd_id']] = i['cf_id']
                    self.sbdh_dict[i['kkdd_id']] = i['sbdh']
            else:
                self.hbc_status = False
                raise Exception('url: %s, status: %s, %s'
                                % (url, r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def check_hbc_img_by_hphm(self, date, hphm):
        headers = {
            'content-type': 'application/json',
            'access_token': self.hbc_ini['token']
        }
        url = 'http://%s:%s/hbc/img/%s/%s/%s' % (
            self.hbc_ini['host'], self.hbc_ini['port'], date, hphm, self.kkdd)
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
        url = 'http://%s:%s/hbc' % (
            self.hbc_ini['host'], self.hbc_ini['port'])
        headers = {
            'content-type': 'application/json',
            'access_token': self.hbc_ini['token']
        }
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                return json.loads(r.text)
            else:
                self.hbc_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def add_wm(self, url, imgpath, name, text, wz_img):
        buf = cStringIO.StringIO()
        helper.get_img(url, buf)
        im = Image.open(cStringIO.StringIO(buf.getvalue()))
        width, heigh = im.size
        if width > 1200:
            font_size = 30
        else:
            font_size = 25
        # 文字水印
        mark = helper_wm.text2img(text, font_size=font_size)
        # 叠加水印到图片
        image = helper_wm.watermark(im, mark, 'left_top', 0.7)
        if wz_img is not None:
            wz_im = Image.open(wz_img)
            wz_width, wz_heigh = wz_im.size
            if width < wz_width:
                wz_im.thumbnail((width, width))
                wz_width, wz_heigh = wz_im.size
            join_im = Image.new('RGBA', (width, heigh+wz_heigh))
            join_im.paste(image, (0, 0))
            join_im.paste(wz_im, (0, heigh))
            join_im.save(imgpath, 'JPEG')
        else:
            image.save(imgpath, 'JPEG')


    # 根据URL地址获取图片到本地
    def get_img_by_url(self, url, path, name, text, wz_img):
        try:
            imgpath = u'%s/%s.jpg' % (path, name)
            self.add_wm(url, imgpath, name, text, wz_img)
        except IOError as e:
            print (e)
            logger.error(e)
            if e[0] == 2 or e[0] == 22:
                name = name.replace('*', '_').replace('?', '_').replace('|', '_').replace(
                    '<', '_').replace('>', '_').replace('/', '_').replace('\\', '_')
                self.makedirs(path)
                
                self.add_wm(url, imgpath, name, text, wz_img)
            else:
                imgpath = ''
                raise
        except Exception as e:
            print (e)
            logger.error(e)
            raise
        finally:
            return imgpath

    # 创建文件夹
    def makedirs(self, path):
        try:
            if os.path.isdir(path):
                pass
            else:
                os.makedirs(path)
        except IOError, e:
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
            # print 'id_flag: %s' % self.id_flag
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
                    # print u'黄表车: %s, 号牌颜色: %s' % (i['hphm'], i['hpys'])
                    hbc_img = self.check_hbc_img_by_hphm(
                        jgsj.format('YYYY-MM-DD'), i['hphm'])
                    imgpath = ''
                    if hbc_img['total_count'] == 0:
                        try:
                            path = u'%s/%s/违章图片目录' % (
                                self.hbc_img_path, jgsj.format(u'YYYY年MM月DD日'))
                            name = u'机号%s车道A%s%sR454DOK3T%sC%sP%s驶向%s违章黄标车违反禁令标志' % (
                                self.jh_dict[i['kkdd_id']], i['cdbh'],
                                jgsj.format(u'YYYY年MM月DD日HH时mm分ss秒'),
                                f_hphm['cpzl'], self.hpys_dict[i['hpys_code']],
                                i['hphm'], self.fxbh_dict.get(i['fxbh_code'], u'其他'))
                            text = u'违法时间:%s 违法地点:惠州市惠城区%s\n违法代码:13441 违法行为:违章黄标车 设备编号:%s\n防伪码:%s' % (
                                i['jgsj'], i['kkdd'], self.sbdh_dict[i['kkdd_id']], helper.get_sign())
                            wz_img = self.hbc_img.get((i['kkdd_id'], i['fxbh_code']), None)
                            if wz_img is not None:
                                wz_img = u'%s/%s' % (self.wz_img_path, wz_img)
                            imgpath = self.get_img_by_url(
                                i['imgurl'], path, name, text, wz_img)
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
        #hbc = HbcCompare()
        # hbc.get_hzhbc_all()
        # 时间戳标记
        time_flag = time.time()
        # 加载初始化数据
        init_flag = False
        while 1:
            if not init_flag:
                try:
                    # 获取黄标车数据
                    self.get_hzhbc_all()
                    self.cgs2_status = True
                    # 获取卡口地点数据
                    self.get_kkdd()
                    self.cgs_status = True

                    init_flag = True
                    print 'Init Finish'
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            elif self.kakou_status and self.cgs_status and self.cgs2_status and self.hbc_status:
                # 现在时间大于时间戳标记时间2小时则更新黄标车数据
                if time.time() - time_flag > 7200:
                    self.get_hzhbc_all()
                    time_flag = time.time()
                try:
                    self.cmpare_hbc()
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            else:
                try:
                    if not self.kakou_status:
                        self.get_cltxmaxid()
                        self.kakou_status = True
                    if not self.cgs_status:
                        self.get_kkdd()
                        self.cgs_status = True
                    if not self.cgs2_status:
                        self.get_hzhbc_by_hphm()
                        self.cgs2_status = True
                    if not self.hbc_status:
                        self.check_hbc_img_by_hphm('2015-09-26', u'粤L12345')
                        self.hbc_status = True
                except Exception as e:
                    #print (e)
                    time.sleep(1)
        del hbc


if __name__ == "__main__":
    hbc = HbcCompare()
##    hbc = HbcCompare()
##    #hbc.main_loop()
##    url = 'http://localhost/kakou/images/test2.jpg'
##    path = 'imgs'
##    name = 'test2'
##    text = u'Linsir.vi5i0n@hotmail.com'
##    hbc.get_img_by_url(url, path, name, text)
##    del hbc
