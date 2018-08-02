# -*- coding: utf-8 -*-
import time
import json
import socket

import arrow

from helper_consul import ConsulAPI
from helper_kafka_consumer import KafkaConsumer
from helper_hbc import Hbc
from my_yaml import MyYAML
from my_logger import *


debug_logging('/home/logs/error.log')
logger = logging.getLogger('root')


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyYAML('/home/my.yaml').get_ini()

        # request方法类
        self.kc = None
        self.hbc = None
        self.con = ConsulAPI()

        self.item = None
        self.part_list = list(range(60))


    def get_service(self, service):
        """获取服务信息"""
        s = self.con.get_service(service)
        if len(s) == 0:
            return None
        h = self.con.get_health(service)
        if len(h) == 0:
            return None
        service_status = {}
        for i in h:
            service_status[i['ServiceID']] = i['Status']
        for i in s:
            if service_status[i['ServiceID']] == 'passing':
                return {'host': i['ServiceAddress'], 'port': i['ServicePort']}
        return None

    # 过滤无效车牌
    def data_valid(self, i):
        if i['kkdd_id'] is None:
            return False
        if len(i['kkdd_id']) < 9:
            return False
        if i['hphm'] == '' or i['hphm'] == '-':
            return False
        if i['kkdd_id'][:6] in set(['441303']) and i['fxbh_code'] != 'IN':
            return False
        return True

    def upload_data(self):
        items = []
        offsets = {}
        for i in range(200):
            msg = self.kc.c.poll(0.005)

            if msg is None:
                continue
            if msg.error():
                continue
            else:
                m = json.loads(msg.value().decode('utf-8'))['message']
                if self.data_valid(m):
                    items.append(m)
            par = msg.partition()
            off = msg.offset()
            offsets[par] = off
        if offsets == {}:
            return
        else:
            print('items={0}'.format(len(items)))
            logger.info('items={0}'.format(len(items)))
            if len(items) > 0:
                self.hbc.kakou_post(items)                 # 上传数据
            self.kc.c.commit(async=False)
            print(offsets)
            logger.info(offsets)
            return

    def main_loop(self):
        while 1:
            try:
                if self.kc is None:
                    self.kc = KafkaConsumer(**dict(self.my_ini['kafka']))
                    self.kc.assign(self.part_list)
                if self.hbc is not None and self.hbc.status:
                    self.upload_data()
                    time.sleep(0.25)
                else:
                    s = self.get_service('kong')
                    if s is None:
                        time.sleep(5)
                        continue
                    self.hbc = Hbc(**{'host': s['host'], 'port': s['port']})
                    self.hbc.status = True
            except Exception as e:
                logger.exception(e)
                time.sleep(15)

        
