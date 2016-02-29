# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests

from ini_conf import MyIni


class FetchData(object):

    def __init__(self):
        self.myini = MyIni()
        self.kakou_conf = self.myini.get_kakou()
        self.hbc_conf = self.myini.get_hbc()
        self.kakou_ini = {
            'host': self.kakou_conf['host'],
            'port': self.kakou_conf['port']
        }
        self.hbc_ini = {
            'host': self.hbc_conf['host'],
            'port': self.hbc_conf['port']
        }
        
        self.id_flag = self.kakou_conf['id_flag']
        self.step = self.kakou_conf['id_step']
        self.kkdd = self.kakou_conf['kkdd']
        self.city = self.kakou_conf['city']

        self.kakou_status = False
        self.hbc_status = False

    def __del__(self):
        del self.myini

    def kakou_post(self, carinfo):
        """上传卡口数据"""
        headers = {'content-type': 'application/json'}
        url = 'http://{0[host]}:{0[port]}/hbc'.format(self.hbc_ini)
        data = {'carinfo': carinfo}
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 202 or r.status_code == 429:
                return r
            else:
                self.hbc_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def que_get(self):
        """查看队列情况"""
        url = 'http://{0[host]}:{0[port]}/que'.format(self.hbc_ini)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r
            else:
                self.hbc_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def get_cltxs(self, id_flag, step=500):
        url = 'http://{0[host]}:{0[port]}/rest_hz_kakou/index.php/{1}/kakou/cltxs/{2}/{3}'.format(
            self.kakou_ini, self.city, id_flag, id_flag+step)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            print e
            self.kakou_status = False
            raise

    def get_cltxmaxid(self):
        """获取最大cltx表id值"""
        url = 'http://{0[host]}:{0[port]}/rest_hz_kakou/index.php/{1}/kakou/cltxmaxid'.format(
            self.kakou_ini, self.city)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def fetch_data(self):
        """获取卡口车辆信息"""
        maxid = self.get_cltxmaxid()['maxid']
        if maxid <= self.id_flag:  # 没有新的数据 返回1
            return

        info = self.get_cltxs(self.id_flag, self.step)
        if info['total_count'] == 0:
            if self.id_flag + self.step < maxid:
                self.id_flag += self.step
            else:
                self.id_flag = maxid
            self.myini.set_id(self.id_flag)
            return

        # 过滤无效车牌
        def data_valid(i):
            if i['kkdd_id'] and i['hphm'] != '' and i['hphm'] != '-':
                return i
        d = filter(data_valid, info['items'])
        if d:
            r = self.kakou_post(d)
        else:
            self.id_flag = info['items'][-1]['id']
            self.myini.set_id(self.id_flag)
            return

        if r.status_code == 202:
            self.id_flag = info['items'][-1]['id']
            self.myini.set_id(self.id_flag)
            if info['total_count'] > 5:
                print '{0}: {1}_{2}'.format(arrow.now(), self.city, self.id_flag)
        elif r.status_code == 429: #服务繁忙
            time.sleep(2)

    def main_loop(self):
        while 1:
            if self.kakou_status and self.hbc_status:
                try:
                    self.fetch_data()
                    time.sleep(2)
                except Exception as e:
                    time.sleep(1)
            else:
                try:
                    if not self.kakou_status:
                        self.get_cltxmaxid()
                        self.kakou_status = True
                    if not self.hbc_status:
                        self.que_get()
                        self.hbc_status = True
                except Exception as e:
                    time.sleep(1)


