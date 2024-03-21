import sys
import os
import io
import argparse
import time

def __to_int(string):
  return int(string, 0)

def __vcp_set(dsp: io.FileIO, idx: int, val: int, dsc: str):
  buf = bytes([0x01, idx])
  dsp.write(buf)
  buf = dsp.read(8)
  if val != buf[7] and val <= buf[5]:
    print('{}: {} -> {} [{}]'.format(dsc, buf[7], val, buf[5]))
    dsp.write(bytes([0x03, idx, 0x00, val]))

parser = argparse.ArgumentParser()
parser.add_argument('-b', metavar='brightness', dest='bval', type=__to_int, default=argparse.SUPPRESS)
parser.add_argument('-c', metavar='contrast',   dest='cval', type=__to_int, default=argparse.SUPPRESS)
a = parser.parse_args()

if not hasattr(a, 'bval') and not hasattr(a, 'cval'):
  print('One of options [-b | -c] is required', file=sys.stderr)
  exit(1)

for subdir, dirs, files in os.walk('/dev/bus/ddcci'):
  for file in files:
    path = os.path.join(subdir, file)
    with open(path, 'r+b', buffering = 0) as f:
    # brightness
      if hasattr(a, 'bval'):
        __vcp_set(f, 0x10, a.bval, '[{}] brightness'.format(path))
    # contrast
      if hasattr(a, 'cval'):
        __vcp_set(f, 0x12, a.cval, '[{}] contrast  '.format(path))