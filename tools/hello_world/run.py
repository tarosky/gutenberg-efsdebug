#!/usr/bin/python3

from os import path

from bcc import BPF

code = path.dirname(path.abspath(__file__)) + '/code.c'

BPF(src_file=code).trace_print(fmt="pid {1}, msg = {5}")
