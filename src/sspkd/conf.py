import ConfigParser as configparser
import os

if os.getuid() > 0:
    DEFAULT_CONFIG_FILE = os.path.join(os.environ['HOME'], '.sspkd.cfg')
else:
    DEFAULT_CONFIG_FILE = "/etc/sspkd.cfg"

class SspkdConfigBundle(object):
    def __setattr__(self, key, val):
        self.__dict__[key] = val
    
    def __str__(self):
        return str(self.__dict__)
    
class SspkdConfig(object):
    __hive = {}

    def __init__(self, config_file=None):
        self.__dict__ = self.__hive
        
        if not self.__dict__.has_key('__cp'):
            self._load_config(config_file)

    def _load_config(self, config_file=None):
        if config_file is None:
            config_file = DEFAULT_CONFIG_FILE

        self.__cp = configparser.SafeConfigParser()
        self.__cp.read(config_file)
        
        self.server = SspkdConfigBundle()
        self.client = SspkdConfigBundle()
        
        # read server configuration 
        self.server.enabled = self.__cp.getboolean('server', 'enabled')
        if self.server.enabled:
            self.server.onlystore = self.__cp.getboolean('server', 'store only')
            self.server.database = self.__cp.get('server', 'db file')
            self.server.pushto = self.__cp.get('server', 'push to').split(' ')
        
        # read client configuration
        self.client.installpath = self.__cp.get('client', 'install path')
        self.client.keysfile = self.__cp.get('client', 'authorized keys file')
        self.client.pushkey = self.__cp.get('client', 'push ssh key')
        self.client.recvkey = self.__cp.get('client', 'receive ssh key')
        self.client.verifykeys = self.__cp.get(
            'client', 'verify keys'
        ).split(' ')
        
        # read optional client configuration
        if self.__cp.has_option('client', 'key server'):
            self.client.keyserver = self.__cp.get('client', 'key server')
            self.client.signkey = self.__cp.get('client', 'sign key')
