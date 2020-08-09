#!/usr/bin/python3

from os import path

from bcc import BPF


def print_line(ts, task, pid, msg):
  print('{:18} {:16} {:6} {}'.format(ts, task, pid, msg))


code = path.dirname(path.abspath(__file__)) + '/code.c'

b = BPF(src_file=code)
b.attach_kprobe(event=b.get_syscall_fnname('clone'), fn_name='hello')

print_line('TIME(s)', 'COMM', 'PID', 'MESSAGE')

# format output
while 1:
  try:
    (task, pid, cpu, flags, ts, msg) = b.trace_fields()
  except ValueError:
    continue
  print_line(ts, task.decode(), pid, msg.decode())
