"""
threefive/srt.py
implementing Secure Reliable Transport protocol via ctypes and  libsrt.so

this is not fully functioning yet.


"""

import ctypes
import sys
import socket

SRTO_SENDER = 21
PORT = 8080
ADDR = "127.0.0.1"


class sockaddr(ctypes.Structure):
    _fields_ = [
        ("sa_family", ctypes.c_ushort),
        ("sa_data", ctypes.c_char * 14),  # 14 bytes for address data
    ]


class in_addr(ctypes.Structure):
    _fields_ = [("s_addr", ctypes.c_uint)]  # IPv4 address


class sockaddr_in(ctypes.Structure):
    _fields_ = [
        ("sin_family", ctypes.c_ushort),
        ("sin_port", ctypes.c_ushort),
        ("sin_addr", in_addr),
        ("sin_zero", ctypes.c_char * 8),  # Padding
    ]


# Create an instance of sockaddr_in
sa_in = sockaddr_in()
sa_in.sin_family = socket.AF_INET
sa_in.sin_port = socket.htons(PORT)
sa_in.sin_addr.s_addr = int.from_bytes(socket.inet_aton(ADDR))  # IPv4 address

# Get a pointer to sa_in
sa_in_ptr = ctypes.pointer(sa_in)

# This is the ctypes equivalent of (struct sockaddr*)&sa
sa_ptr = ctypes.cast(sa_in_ptr, ctypes.POINTER(sockaddr))

libsrt = ctypes.CDLL("libsrt.so")
libsrt.srt_startup()
ss = libsrt.srt_create_socket()
libsrt.srt_setsockflag(ss, SRTO_SENDER, 1, 8)
st = libsrt.srt_connect(
    ss, sa_ptr, 64
)  # How big is a pointer? 32? I went 64 just in case.

st = libsrt.srt_close(ss)

srt_cleanup()
