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

        self.time_flag = arrow.get(self.kakou_conf['time_flag'])
        self.time_step = self.kakou_conf['time_step']

        self.kakou_status = False
        self.hbc_status = False

    def __del__(self):
        del self.myini

    def kakou_post(self, carinfo):
        """上传卡口数据"""
        #print 'kakou_post'
        headers = {'content-type': 'application/json'}
        url = 'http://{0[host]}:{0[port]}/hbc'.format(self.hbc_ini)
        data = {'carinfo': carinfo}
        #print data
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

    def get_cltxs(self, t1, time_step=60):
        url = 'http://{0[host]}:{0[port]}/rest_hz_kakou/index.php/jjlm/kakou/jgcl/{1}/{2}'.format(
            self.kakou_ini, t1.format('YYYY-MM-DD HH:mm:ss'),
            t1.replace(seconds=time_step).format('YYYY-MM-DD HH:mm:ss'))
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

##    def get_cltxmaxid(self):
##        """获取最大cltx表id值"""
##        url = 'http://{0[host]}:{0[port]}/rest_hz_kakou/index.php/{1}/kakou/cltxmaxid'.format(
##            self.kakou_ini, self.city)
##        try:
##            r = requests.get(url)
##            if r.status_code == 200:
##                return json.loads(r.text)
##            else:
##                self.kakou_status = False
##                raise Exception('url: {url}, status: {code}, {text}'.format(
##                    url=url, code=r.status_code, text=r.text))
##        except Exception as e:
##            self.kakou_status = False
##            raise

    def fetch_data(self):
        """获取卡口车辆信息"""
        #print 'fetch_data'
        now = arrow.now()
        if now.replace(minutes=-30) < self.time_flag:
            return
        info = self.get_cltxs(self.time_flag, self.time_step)
        #print info
        if info['total_count'] == 0:
            self.time_flag = self.time_flag.replace(seconds=self.time_step)
            self.myini.set_time(str(self.time_flag))
            return
        #print info
        # 过滤无效车牌
        def data_valid(i):
            if i['kkdd_id'] and i['hphm'] != '' and i['hphm'] != '-' and i['fxbh_code'] == 'IN':
                return i
        d = filter(data_valid, info['items'])
        if d:
            r = self.kakou_post(d)
        else:
            self.time_flag = self.time_flag.replace(seconds=self.time_step)
            self.myini.set_time(str(self.time_flag))
            return
        if r.status_code == 202:
            self.time_flag = self.time_flag.replace(seconds=self.time_step)
            self.myini.set_time(str(self.time_flag))
            if info['total_count'] >= 0:
                print '{0}: {1}_{2}'.format(arrow.now(), self.city,
                                            str(self.time_flag))
        elif r.status_code == 429: #服务繁忙
            time.sleep(2)

##        if r.status_code == 422:
##            print r.text

    def main_loop(self):
        while 1:
            if self.kakou_status and self.hbc_status:
                try:
                    self.fetch_data()
                    time.sleep(3)
                except Exception as e:
                    print e
                    time.sleep(2)
            else:
                try:
                    if not self.kakou_status:
                        self.get_cltxs(self.time_flag, self.time_step)
                        self.kakou_status = True
                    if not self.hbc_status:
                        self.que_get()
                        self.hbc_status = True
                except Exception as e:
                    time.sleep(2)

if __name__ == '__main__':  # pragma nocover
    fd = FetchData()
    fd.main_loop()
