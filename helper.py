# -*- coding: utf-8 -*-
import shutil

import requests


def fix_hphm(hphm, hpys):
    if hphm != None and hphm != '-':
        header = hphm[:2] # 车牌头
        tail = hphm[-1] #车牌尾
        if header == u'粤L':
            if tail == u'学':
                return {'hphm': hphm[1:-1], 'hpzl': '16', 'cpzl': u'标准车牌'}
            if tail == u'挂':
                return {'hphm': hphm[1:-1], 'hpzl': '15', 'cpzl': u'标准车牌'}
            if hpys == 2 or hpys == u'BU': #蓝牌
                return {'hphm': hphm[1:], 'hpzl': '02', 'cpzl': u'标准车牌'}
            if hpys == 3 or hpys == u'YL': #黄牌
                return {'hphm': hphm[1:], 'hpzl': '01', 'cpzl': u'双层车牌'}
            if hpys == 5 or hpys == u'BK': #黑牌
                return {'hphm': hphm[1:], 'hpzl': '06', 'cpzl': u'标准车牌'}
    return {'hphm': hphm, 'hpzl': '00', 'cpzl': u'其他'}

def get_url_img(url, path):
    """根据URL地址抓图到本地文件"""
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    # 非200响应,抛出异常
    r.raise_for_status()
