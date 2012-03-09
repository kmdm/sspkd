from conf import SspkdConfig
from push import SspkdPush
from util import SspkdUtil

class SspkdReceive:
    def __init__(self):
        self.cf = SspkdConfig()
        self.util = SspkdUtil()

    def receive(self, signed_keys):
        sshkeys = self.util.verify_keys(signed_keys)
        
        if self.cf.server.enabled:
            f = open(self.cf.server.database, "w")
            f.write(signed_keys)
            f.close()
            
            SspkdPush().push(signed_keys, sign=False, relay=True)
            
            if self.cf.server.onlystore:
                return
        
        self.util.install_keys(sshkeys)
