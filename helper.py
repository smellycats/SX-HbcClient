# -*- coding: utf-8 -*-
import os
import shutil
from random import Random

import requests
from itsdangerous import Signer


def fix_hphm(hphm, hpys):
    if hphm != None and hphm != '-':
        header = hphm[:2] # 车牌头
        tail = hphm[-1] #车牌尾
        if header == u'粤L':
            if tail == u'学':
                return {'hphm': hphm[1:-1], 'hpzl': '16', 'cpzl': u'标准车牌'}
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
    
def get_img(url, f):
    """根据URL地址抓图到本地文件"""
    r = requests.get(url, stream=True)
    #buf = StringIO.StringIO()
    if r.status_code == 200:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    # 非200响应,抛出异常
    r.raise_for_status()

def random_str(randomlength=8):
    """生成随机字符串"""
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def get_sign():
    """生成防伪码"""
    return Signer('hzhbc').sign(random_str(6))

def makedirs(path):
    """创建文件夹"""
    try:
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
    except IOError,e:
        raise

def hbc_img():
    img_dict = {
        (u'441302017', u'OT'): u'\u6885\u6e56\u8def\u6885\u6e56\u5361\u53e3_\u5f80\u6885\u6e56.jpg',
        (u'441302018', u'OT'): u'\u91d1\u9f99\u5927\u9053\u56db\u89d2\u697c\u5361\u53e3_\u5f80\u6cf0\u7f8e.jpg',
        (u'441302103', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u5357\u65cb\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u9a6c\u6c34\u8def.jpg',
        (u'441302017', u'IN'): u'\u6885\u6e56\u8def\u6885\u6e56\u5361\u53e3_\u5f80\u4e0b\u89d2.jpg',
        (u'441302102', u'OT'): u'\u60e0\u57ce\u533a\u91d1\u949f\u8def\u7ba1\u59d4\u4f1a\u8def\u53e3_\u5f80\u6cf0\u8c6a\u8def.jpg',
        (u'441302006', u'IN'): u'\u4ef2\u607a\u533a\u56fd\u9053205\u7ebf\u9648\u6c5f\u4e0e\u9547\u9686\u4ea4\u754c\u5904\u5361\u53e3_\u5f80\u5e02\u533a.jpg',
        (u'441302026', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u67cf\u7530\u6865\u5361\u53e3_\u5f80\u67cf\u7530\u6865.jpg',
        (u'441302004', u'OT'): u'\u60e0\u535a\u8def\u4e0e\u4e09\u73af\u8def\u653e\u53e3\u5904\u5361\u53e3_\u5f80\u91d1\u5c71\u6c7d\u8f66\u57ce.jpg',
        (u'441302021', u'IN'): u'\u60e0\u57ce\u533aYG90\u7ebf\u5362\u6d32\u82a6\u6751\u5361\u53e3_\u5f80\u82a6\u5c9a.jpg',
        (u'441302022', u'IN'): u'\u60e0\u57ce\u533aX199\u5e7f\u4ecd\u516c\u8def\u4ecd\u56fe\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302025', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u9f99\u5858\u6865\u5361\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302004', u'IN'): u'\u60e0\u535a\u8def\u4e0e\u4e09\u73af\u8def\u653e\u53e3\u5904\u5361\u53e3_\u535a\u7f57\u5f80\u4e09\u73af.jpg',
        (u'441302102', u'IN'): u'\u60e0\u57ce\u533a\u91d1\u949f\u8def\u7ba1\u59d4\u4f1a\u8def\u53e3_\u5f80\u4e09\u680b.jpg',
        (u'441302020', u'OT'): u'\u60e0\u57ce\u533a\u89c2\u5c9a\u5927\u6865\u82a6\u5c9a\u5361\u53e3_\u5f80\u89c2\u97f3\u9601.jpg',
        (u'441302006', u'OT'): u'\u4ef2\u607a\u533a\u56fd\u9053205\u7ebf\u9648\u6c5f\u4e0e\u9547\u9686\u4ea4\u754c\u5904\u5361\u53e3_\u5f80\u4ef2\u607a.jpg',
        (u'441302027', u'IN'): u'\u4e09\u73af\u897f\u8def\u4e30\u5c71\u5361\u53e3_\u5f80\u4e0b\u89d2.jpg',
        (u'441302106', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u534e\u9633\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u4e09\u73af.jpg',
        (u'441302019', u'IN'): u'\u6c38\u8054\u8def\u706b\u8f66\u897f\u7ad9\u5361\u53e3_\u897f\u7ad9.jpg',
        (u'441302027', u'OT'): u'\u4e09\u73af\u897f\u8def\u4e30\u5c71\u5361\u53e3_\u5f80\u897f\u7ad9.jpg',
        (u'441302024', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053208\u7ebf\u6a2a\u6ca5\u5361\u53e3_\u5f80\u6881\u5316.jpg',
        (u'441302021', u'OT'): u'\u60e0\u57ce\u533aYG90\u7ebf\u5362\u6d32\u82a6\u6751\u5361\u53e3_\u5f80\u82a6\u6751.jpg',
        (u'441302015', u'OT'): u'\u60e0\u6c11\u5927\u9053\u5174\u6e56\u4e00\u8def\u5361\u53e3_\u5f80\u6c5d\u6e56.jpg',
        (u'441302105', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5357\u53e3_\u5f80\u6c34\u53e3.jpg',
        (u'441302007', u'OT'): u'\u5c0f\u91d1\u53e3\u5361\u53e3_\u5f80\u6c64\u6cc9.jpg',
        (u'441302104', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5361\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302105', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5357\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302010', u'OT'): u'\u60e0\u57ce\u533a\u9a6c\u5b89\u6cf0\u5b89\u8def\u9a6c\u5b89\u5361\u53e3_\u5f80\u60e0\u4e1c.jpg',
        (u'441302018', u'IN'): u'\u91d1\u9f99\u5927\u9053\u56db\u89d2\u697c\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302008', u'IN'): u'\u4ef2\u607a\u533a\u4ef2\u607a\u5927\u9053\u5bcc\u5ddd\u745e\u56ed\u5361\u53e3_\u5f80\u5e02\u533a.JPG',
        (u'441302023', u'IN'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u5927\u5c9a\u8001\u6536\u8d39\u7ad9\u524d\u5361\u53e3_\u5f80\u6a2a\u6ca5.jpg',
        (u'441302011', u'OT'): u'\u4ef2\u607a\u533a\u7701\u9053357\u7ebf\u9648\u6c5f\u68a7\u6751\u5361\u53e3_\u5f80\u4ef2\u607a.JPG',
        (u'441302015', u'IN'): u'\u60e0\u6c11\u5927\u9053\u5174\u6e56\u4e00\u8def\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302014', u'OT'): u'\u4ef2\u607a\u533a\u7701\u9053120\u7ebf\u672a\u6f7c\u6865\u5361\u53e3_\u5f80\u4ef2\u607a.JPG',
        (u'441302008', u'OT'): u'\u4ef2\u607a\u533a\u4ef2\u607a\u5927\u9053\u5bcc\u5ddd\u745e\u56ed\u5361\u53e3_\u5f80\u4ef2\u607a.JPG',
        (u'441302009', u'IN'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u6c34\u53e3\u5361\u53e3_\u5f80\u8001\u6c34\u53e3.jpg',
        (u'441302011', u'IN'): u'\u4ef2\u607a\u533a\u7701\u9053357\u7ebf\u9648\u6c5f\u68a7\u6751\u5361\u53e3_\u5f80\u5e02\u533a.JPG',
        (u'441302025', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u9f99\u5858\u6865\u5361\u53e3_\u5f80\u826f\u4e95.jpg',
        (u'441302020', u'IN'): u'\u60e0\u57ce\u533a\u89c2\u5c9a\u5927\u6865\u82a6\u5c9a\u5361\u53e3_\u5f80\u82a6\u5c9a.jpg',
        (u'441302014', u'IN'): u'\u4ef2\u607a\u533a\u7701\u9053120\u7ebf\u672a\u6f7c\u6865\u5361\u53e3_\u5f80\u5e02\u533a.JPG',
        (u'441302009', u'OT'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u6c34\u53e3\u5361\u53e3_\u5f80\u5357\u65cb.jpg',
        (u'441302010', u'IN'): u'\u60e0\u57ce\u533a\u9a6c\u5b89\u6cf0\u5b89\u8def\u9a6c\u5b89\u5361\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302019', u'OT'): u'\u6c38\u8054\u8def\u706b\u8f66\u897f\u7ad9\u5361\u53e3_\u5f80\u9ad8\u901f\u516c\u8def.jpg',
        (u'441302023', u'OT'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u5927\u5c9a\u8001\u6536\u8d39\u7ad9\u524d\u5361\u53e3_\u5f80\u7d2b\u91d1.jpg',
        (u'441302022', u'OT'): u'\u60e0\u57ce\u533aX199\u5e7f\u4ecd\u516c\u8def\u4ecd\u56fe\u5361\u53e3_\u5f80\u4ecd\u56fe.jpg',
        (u'441302007', u'IN'): u'\u5c0f\u91d1\u53e3\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302103', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u5357\u65cb\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u5357\u65cb.jpg',
        (u'441302013', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u5357\u5927\u9053\u60e0\u6de1\u8def\u5361\u53e3_\u5f80\u5e02\u533a.jpg',
        (u'441302024', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053208\u7ebf\u6a2a\u6ca5\u5361\u53e3_\u5f80\u6a2a\u6ca5.jpg',
        (u'441302013', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u5357\u5927\u9053\u60e0\u6de1\u8def\u5361\u53e3_\u5f80\u6de1\u6c34.jpg',
        (u'441302104', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5361\u53e3_\u5f80\u6c34\u53e3.jpg',
        (u'441302026', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u67cf\u7530\u6865\u5361\u53e3_\u5f80\u60e0\u5dde\u5927\u9053.jpg',
        (u'441302106', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u534e\u9633\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u5357\u65cb.jpg',
        (u'441302001', u'OT'): u'\u4e1c\u6e56\u897f\u8def_\u5f80\u65b0\u5f00\u6cb3\u6865.jpg',
        (u'441302001', u'IN'): u'\u4e1c\u6e56\u897f\u8def_\u5f80\u897f\u679d\u6c5f.jpg',
        (u'441302002', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u957f\u6e56\u5317\u8def\u8def\u6bb5_\u5f80\u6c5f\u5317.jpg',
        (u'441302002', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u957f\u6e56\u5317\u8def\u8def\u6bb5_\u5f80\u9a6c\u5b89.jpg',
        (u'441302003', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u4e1c\u6c5f\u5927\u6865\u5361\u53e3_\u5f80\u4e1c\u5e73.jpg',
        (u'441302003', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u4e1c\u6c5f\u5927\u6865\u5361\u53e3_\u5f80\u6c5f\u5317.jpg',
        (u'441302005', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u6c99\u5824\u4e8c\u8def\u4e09\u73af\u8def\u5361\u53e3_\u5f80\u6cb3\u5357\u5cb8.jpg',
        (u'441302005', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u6c99\u5824\u4e8c\u8def\u4e09\u73af\u8def\u5361\u53e3_\u5f80\u4e09\u73af.jpg',
        (u'441302016', u'OT'): u'\u60e0\u57ce\u533a\u9cc4\u6e56\u8def\u5361\u53e3_\u5f80\u7ea2\u82b1\u6e56.jpg',
        (u'441302016', u'IN'): u'\u60e0\u57ce\u533a\u9cc4\u6e56\u8def\u5361\u53e3_\u5f80\u6c5f\u5317.jpg'
    }
    return img_dict
        

