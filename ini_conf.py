
import ConfigParser

class MyIni:
    def __init__(self, conf_path='my_ini.conf'):
        self.conf_path = conf_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(conf_path)

    def get_hbc(self):
        conf = {}
        section = 'HBC'
        conf['id_flag'] = self.cf.getint(section, 'id_flag')
        conf['step'] = self.cf.getint(section, 'step')
        conf['kkdd'] = self.cf.get(section, 'kkdd')
        conf['city'] = self.cf.get(section, 'city')
        conf['city_name'] = self.cf.get(section, 'city_name').decode('gbk')
        conf['hbc_img_path'] = self.cf.get(section, 'hbc_img_path').decode('gbk')
        conf['wz_img_path'] = self.cf.get(section, 'wz_img_path').decode('gbk')
        return conf

    def get_bk(self):
        conf = {}
        section = 'BK'
        conf['time_flag'] = self.cf.get(section, 'time_flag')
        conf['step'] = self.cf.getint(section, 'step')
        conf['kkdd'] = self.cf.get(section, 'kkdd')
        return conf

    def set_hbc(self, id_flag):
        self.cf.set('HBC', 'id_flag', id_flag)
        self.cf.write(open(self.conf_path, 'w'))

    def set_bk(self, time_flag):
        self.cf.set('BK', 'time_flag', time_flag)
        self.cf.write(open(self.conf_path, 'w'))

if __name__ == '__main__':
    ini = MyIni()
    hbc = ini.get_bk()
    ini.set_bk('2015-10-01 00:10:00')
    print hbc
