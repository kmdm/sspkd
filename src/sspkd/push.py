import os
import subprocess

from conf import SspkdConfig
from errors import *
from util import SspkdUtil

class SspkdPush(object):
    def __init__(self):
        self.cf = SspkdConfig()
        self.util = SspkdUtil()

    def _push(self, server, sshkeys, relay=False):
        print "pushing updated ssh public keys to %s%s..." % (
            server, " (relay)" if relay else ""
        )
        
        # FIXME: Assume server installpath == client installpath
        cmdline = [ 
            'ssh', '-o IdentityFile=%s' % self.cf.client.pushkey,
            '-o IdentitiesOnly=yes',
            server, 'receive'
        ]
        
        ssh = subprocess.Popen(cmdline, stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        out, err = ssh.communicate(input=sshkeys)
        print out

    def push(self, sshkeys, sign=True, relay=False):
        if sign:
            sshkeys = self.util.sign_keys(sshkeys)
    
        if relay:
            servers = self.cf.server.pushto
        else:
            servers = [ self.cf.client.keyserver ]

        for server in servers:
            if server:
                self._push(server, sshkeys, relay=relay)
