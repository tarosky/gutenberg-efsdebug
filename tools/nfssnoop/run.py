#!/usr/bin/python3

import sys
from os import path

from bcc import BPF


def print_line(ts, task, pid, msg):
  print('{:18} {:16} {:6} {:6}'.format(ts, task, pid, msg))
  sys.stdout.flush()


code = path.dirname(path.abspath(__file__)) + '/code.c'

# load BPF program
b = BPF(src_file=code)
b.attach_kprobe(event='rpc_run_task', fn_name='hello')

print_line('TIME(s)', 'COMM', 'PID', 'STATID')

# process event
start = 0


def print_event(cpu, data, size):
  global start
  event = b['events'].event(data)
  if start == 0:
    start = event.ts
  time_s = (float(event.ts - start)) / 1000000000

  print_line(time_s, event.comm.decode(), event.pid, event.statidx)


# loop with callback to print_event
b['events'].open_perf_buffer(print_event)
while 1:
  try:
    b.perf_buffer_poll()
  except KeyboardInterrupt:
    exit()
