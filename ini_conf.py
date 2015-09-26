
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
        return conf

    def set_hbc(self, id_flag):
        self.cf.set('HBC', 'id_flag', id_flag)
        self.cf.write(open(self.conf_path, 'w'))

if __name__ == '__main__':
    ini = MyIni()
    hbc = ini.get_hbc()
    #ini.set_hbc(2)
    print hbc
