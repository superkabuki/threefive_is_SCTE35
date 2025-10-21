"""
threefive/srt.py
implementing Secure Reliable Transport protocol via ctypes and  libsrt.so

this is not fully functioning yet.


"""

import ctypes
import sys
import socket
import time

YES = 1
SRTO_SENDER = 21
PORT = 9000
ADDR = "127.0.0.1"

MSG = ctypes.create_string_buffer(b"bigcorp message", 15)


class sockaddr(ctypes.Structure):
    _fields_ = [
        ("sa_family", ctypes.c_ushort),
        ("sa_data", ctypes.c_char * 14),  # 14 bytes for address data
    ]


class in_addr(ctypes.Structure):
    _fields_ = [("s_addr", ctypes.c_uint32)]  # IPv4


class sockaddr_in(ctypes.Structure):
    _fields_ = [
        ("sin_family", ctypes.c_short),
        ("sin_port", ctypes.c_ushort),
        ("sin_addr", in_addr),
        ("sin_zero", ctypes.c_char * 8),
    ]


def ipv4int(addr):
    """
    take a ipv4 string addr and make it an int
    """
    sa = int.from_bytes(socket.inet_pton(socket.AF_INET, addr), byteorder="little")
    print(f"SA {sa}")
    return sa


def mk_sockaddr_sa(addr, port):
    """
    mk_sockaddr_sa make a c compatible (struct sockaddr*)&sa
    """
    sa_in = sockaddr_in()
    sa_in.sin_family = socket.AF_INET
    sa_in.sin_port = socket.htons(port)
    sa_in.sin_addr.s_addr = ipv4int(addr)
    # socket.inet_pton(socket.AF_INET, addr)
    # Get a pointer to sa_in
    sa_in_ptr = ctypes.pointer(sa_in)
    #  (struct sockaddr*)&sa
    return ctypes.cast(sa_in_ptr, ctypes.POINTER(sockaddr)), ctypes.sizeof(sa_in)


libsrt = ctypes.CDLL("libsrt.so")
libsrt.srt_getlasterror_str.restype = ctypes.c_char_p

libsrt.srt_startup()
sa_ptr, sa_size = mk_sockaddr_sa(ADDR, PORT)
print(f"Make Socket Addr {libsrt.srt_getlasterror_str()}")

ss = libsrt.srt_create_socket()
print(f"Create Socket: {libsrt.srt_getlasterror_str()}")

libsrt.srt_setsockflag(ss, SRTO_SENDER, 1, 32)
print(f"Set Socket: {libsrt.srt_getlasterror_str()}")

st = libsrt.srt_connect(ss, sa_ptr, 64)
if st:
    print(f"Connect: {libsrt.srt_getlasterror_str()}")
loops = 100
while loops:
    loops -= 1
    st = libsrt.srt_sendmsg2(ss, MSG, ctypes.sizeof(MSG), None)
    if st:
        print(f"Sending Message: {libsrt.srt_getlasterror_str()}")
    time.sleep(0.1)

time.sleep(1)

st = libsrt.srt_close(ss)
libsrt.srt_cleanup()
