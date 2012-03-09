import getpass
import os

import pyme.core
import pyme.pygpgme

from conf import SspkdConfig
from errors import *

class SspkdUtil(object):
    def __init__(self):
        self.cf = SspkdConfig()
    
    def _passphrase_cb(self, hint, desc, prev_bad):
        return getpass.getpass("[%s] passphrase: " % hint)

    def sign_keys(self, sshkeys):
        c = pyme.core.Data()
        p = pyme.core.Data(sshkeys)

        ctx = pyme.core.Context()
        ctx.set_passphrase_cb(self._passphrase_cb)
        ctx.set_armor(1)
        ctx.op_keylist_start(self.cf.client.signkey, 0)
        key = ctx.op_keylist_next()

        ctx.op_sign(p, c, pyme.pygpgme.GPGME_SIG_MODE_CLEAR)

        c.seek(0, 0)
        return c.read()

    def verify_keys(self, signed_keys):
        p = pyme.core.Data()
        c = pyme.core.Data(signed_keys)
        
        ctx = pyme.core.Context()
        ctx.op_verify(c, None, p)
        
        # FIXME: We're only expect one signature, is this sufficient? 
        sig = ctx.op_verify_result().signatures[0]
        
        if sig.summary & pyme.pygpgme.GPGME_SIGSUM_GREEN == 0:
            raise SspkdInvalidSignature(
                'Signature is not valid (result=%d)!' % sig.summary
            )

        if sig.summary & pyme.pygpgme.GPGME_SIGSUM_VALID == 0:
            raise SspkdInvalidSignature(
                'Signature is not valid (result=%d)!' % sig.summary
            )
        
        if sig.fpr not in self.cf.client.verifykeys:
            raise SspkdInvalidSignature(
                'Signature key fingerprint does not match verifiy keys: %s' %\
                sig.fpr
            )

        p.seek(0, 0)
        return p.read()
    
    def get_pubkey(self):
        pubkey = ""

        if self.cf.client.recvkey:
            pubkey = 'command="%s $SSH_ORIGINAL_COMMAND" ' % (
                os.path.join(self.cf.client.installpath, 'sspkd-shell'),
            )

            with open(self.cf.client.recvkey, "r") as f:
                pubkey += f.read()
        
        return pubkey

    def install_keys(self, sshkeys):
        with open(self.cf.client.keysfile, "w") as f:
            f.write(self.get_pubkey())
            f.write(sshkeys)
