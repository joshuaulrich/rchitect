from __future__ import unicode_literals
from ctypes import c_void_p, c_double, c_int, c_int32, c_int64, c_uint
from ctypes import Structure
from ctypes import sizeof


class SEXP(c_void_p):

    pass


SEXPTYPE = c_uint


class Rcomplex(Structure):
    _fields_ = [
        ('r', c_double),
        ('i', c_double),
    ]


if sizeof(c_void_p) == 4:
    ptrdiff_t = c_int32
elif sizeof(c_void_p) == 8:
    ptrdiff_t = c_int64

R_len_t = c_int

R_xlen_t = ptrdiff_t
