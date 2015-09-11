# -*- coding: utf-8 -*-
import json
import requests

def fix_hphm(hphm, hpys):
    if hphm != None and hphm != '-':
        header = hphm[:2]
        print "header %s"%header
        tail = hphm[-1]
        print "tail %s"%tail
        if header == u'粤L':
            if tail == u'学':
                return {'hphm': hphm[1:-1], 'hpzl': '16', 'cpzl': u'标准车牌'}
            if tail == u'挂':
                return {'hphm': hphm[1:-1], 'hpzl': '15', 'cpzl': u'标准车牌'}
            if hpys == 2 or hpys == u'蓝牌': #蓝牌
                return {'hphm': hphm[1:], 'hpzl': '02', 'cpzl': u'标准车牌'}
            if hpys == 3 or hpys == u'黄牌': #黄牌
                return {'hphm': hphm[1:], 'hpzl': '01', 'cpzl': u'双层车牌'}
            if hpys == 5 or hpys == u'黑牌': #黑牌
                return {'hphm': hphm[1:], 'hpzl': '06', 'cpzl': u'标准车牌'}
        return {'hphm': hphm, 'hpzl': '00', 'cpzl': u'其他'}

def get_img(url):

class HbcCompare(object):

    def __init__(self):
        self.kakou_ip = '127.0.0.1'
        self.kakou_port = 80
        self.cgs_ip = '127.0.0.1'
        self.cgs_port = 8098
        self.id_flag = 201169426
        self.step = 100
        self.kkdd = '441302'
        
        self.kakou_status = False
        self.cgs_status = False
        self.hbc_status = False

    def get_cltxs(self):
        last_id = self.id_flag + self.step
        url = 'http://%s:%s/rest_hz_kakou/index.php/hd/kakou/cltxs/%s/%s'%(self.kakou_ip, self.kakou_port, self.id_flag, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print (e)
        return False

    def get_cltxmaxid(self):
        url = 'http://%s:%s/rest_hz_kakou/index.php/hd/kakou/cltxmaxid'%(self.kakou_ip, self.kakou_port)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.text['maxid']
        except Exception as e:
            print (e)
        return False

    def get_hbc(self, hphm, hpzl):
        url = 'http://%s:%s/hzhbc/%s/%s'%(self.cgs_ip, self.cgs_port, hphm, hpzl)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print (e)
        return False

    def get_exist_hbc_by_hphm(self, date, hphm):
        url = 'http://%s:%s/hbc/%s/%s/%s'%(self.hzhbc_ip, self.hzhbc_port, date, hphm, self.kkdd)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print (e)
        return False

    def add_hbc(self, data):
        url = 'http://%s:%s/hbc/%s/%s/%s'%(self.hzhbc_ip, self.hzhbc_port)
        headers = {'content-type': 'application/json'}
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                return True
        except Exception as e:
            print (e)
        return False

    def cmpare_hbc(self):
        maxid = self.get_cltxmaxid()
        if not maxid:
            self.kakou_status = False
            return False
        if maxid > self.id_flag:
            carinfo = self.get_cltxs()
            if not carinfo:
                self.kakou_status = False
                return False
            if carinfo['total_count'] == 0:
                return 0
            for i in carinfo:
                hbc_hphm = fix_hphm(i.hphm, i.hpys)
                if hbc_hphm['hpzl'] != '00':
                    # 查询黄标车数据库是否黄标车
                    hbc = get_hbc(hbc_hphm['hphm'], hbc_hphm['hpzl'])
                    if not hbc:
                        self.cgs_status = False
                        return False
                    if hbc != {}:
                        e_hbc = get_exist_hbc_by_hphm(date=i.jgsj[:10], i.hphm)
                        if not e_hbc:
                            self.hbc_status = False
                            return False
                        imgpath = ''
                        if e_hbc != {}:
                            try:
                                imgpath = get_img(i.imgurl)
                            except Exception as e:
                                print (e)
                        data = {'jgsj': i.jgsj, 'hphm': i.hphm,
                                'kkdd_id': i.kkdd, 'hpys_id': i.hpys_id,
                                'fxbh_id': i.fxbh_id, 'cdbh': i.cdbh,
                                'imgurl': i.imgurl, 'imgpath': imgpath}
                        add_hbc = self.add_hbc(data)
                        if not add_hbc:
                            self.hbc_status = False
                            return False
                    

    def main_loop(self):
        while 1:
            if self.kakou_status:
                
            

        

if __name__ == "__main__":
    print fix_hphm(u'粤L12345',3)
