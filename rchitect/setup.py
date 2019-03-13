from __future__ import unicode_literals
import sys
import signal

from rchitect._libR import ffi, lib
from .utils import Rhome, libRpath, ensure_path
from .callbacks import def_callback, setup_unix_callbacks, setup_rstart


def init(args=["rchitect", "--quiet"]):
    rhome = Rhome()
    ensure_path(rhome)
    if not lib._libR_load(libRpath(rhome).encode()):
        raise Exception("cannot load R library")
    if not lib._libR_load_symbols():
        raise Exception(ffi.string(lib._libR_dl_error_message()).decode())

    _argv = [ffi.new("char[]", a.encode()) for a in args]
    argv = ffi.new("char *[]", _argv)

    lib.Rf_initialize_R(len(argv), argv)
    if sys.platform.startswith("win"):
        setup_rstart(args)
    else:
        setup_unix_callbacks()
    lib.setup_Rmainloop()
    if not lib._libR_load_constants():
        raise Exception(ffi.string(lib._libR_dl_error_message()).decode())
    lib._libR_init_xptr_callback()


def loop():
    lib.run_Rmainloop()


def sigint_handler(signum, frame):
    raise KeyboardInterrupt()


if sys.version >= "3":
    def ask_input(s):
        return input(s)
else:
    def ask_input(s):
        return raw_input(s).decode("utf-8", "backslashreplace")


@def_callback()
def show_message(buf):
    sys.stdout.write(buf)
    sys.stdout.flush()


@def_callback()
def read_console(p, add_history):
    orig_handler = signal.getsignal(signal.SIGINT)
    # allow Ctrl+C to throw KeyboardInterrupt in callback
    signal.signal(signal.SIGINT, sigint_handler)
    try:
        return ask_input(p)
    finally:
        signal.signal(signal.SIGINT, orig_handler)


@def_callback()
def write_console_ex(buf, otype):
    if otype == 0:
        sys.stdout.write(buf)
        sys.stdout.flush()
    else:
        sys.stderr.write(buf)
        sys.stderr.flush()


@def_callback()
def busy(which):
    pass


@def_callback()
def polled_events():
    pass


# @def_callback()
# def clean_up(saveact, status, run_last):
#     lib.Rstd_CleanUp(saveact, status, run_last)


@def_callback()
def yes_no_cancel(p):
    while True:
        try:
            result = ask_input("{} [y/n/c]: ".format(p))
            if result in ["Y", "y"]:
                return 1
            elif result in ["N", "n"]:
                return 2
            else:
                return 0
        except EOFError:
            return 0
        except KeyboardInterrupt:
            return 0
        except Exception:
            pass