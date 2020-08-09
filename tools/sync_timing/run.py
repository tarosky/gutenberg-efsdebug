#!/usr/bin/python3

import sys
from os import path

from bcc import BPF

code = path.dirname(path.abspath(__file__)) + '/code.c'

b = BPF(src_file=code)
b.attach_kprobe(event=b.get_syscall_fnname('sync'), fn_name='do_trace')
print("Tracing for quick sync's... Ctrl-C to end")

# format output
start = 0
while 1:
  try:
    (task, pid, cpu, flags, ts, ms) = b.trace_fields()
    if start == 0:
      start = ts
    ts = ts - start
    print(
        'At time {:.2f} s: multiple syncs detected, last {} ms ago'.format(
            ts, ms.decode()))
    sys.stdout.flush()
  except KeyboardInterrupt:
    exit()
