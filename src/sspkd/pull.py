import os
import subprocess

from conf import SspkdConfig
from errors import *
from util import SspkdUtil

class SspkdPull(object):
    def __init__(self):
        self.cf = SspkdConfig()
        self.util = SspkdUtil()

    def _pull(self):
        if self.cf.server.enabled:
            with open(self.cf.server.database, "r") as f:
                return f.read()

        cmdline = [ 
            'ssh', '-o IdentityFile=%s' % self.cf.client.pushkey, 
            '-o IdentitiesOnly=yes',
            self.cf.client.keyserver, 'fetch'
        ]
        
        ssh = subprocess.Popen(cmdline, stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        out, err = ssh.communicate()
        return out
    
    def pull(self, install=False, verify=True):
        signed_keys = self._pull()

        if verify:
            sshkeys = self.util.verify_keys(signed_keys)

            if install:
                self.util.install_keys(sshkeys)
        else:
            sshkeys = signed_keys

        return sshkeys
