from __future__ import unicode_literals
from ctypes import c_void_p
import sys

if sys.platform.startswith('win'):
    if sys.version_info[0] >= 3:
        from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ
    else:
        from _winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ


def cfunction(fname, lib, restype, argtypes):
    f = getattr(lib, fname)
    f.restype = restype
    f.argtypes = argtypes
    return f


def cglobal(vname, lib, vtype=c_void_p):
    return vtype.in_dll(lib, vname)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def read_registry(key, valueex):
    reg_key = OpenKey(HKEY_LOCAL_MACHINE, key, 0, KEY_READ)
    return QueryValueEx(reg_key, valueex)
