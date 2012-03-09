from errors import *
from receive import *
from pull import *
from push import *

__sspkd_version__ = '0.1'

def fetch(*args, **kwargs):
    return SspkdPull().pull(*args, **kwargs)

def recv(*args, **kwargs):
    return SspkdReceive().receive(*args, **kwargs)

def sign_and_push(*args, **kwargs):
    return SspkdPush().push(*args, **kwargs)
