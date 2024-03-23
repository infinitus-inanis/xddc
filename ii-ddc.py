import os, io, sys
import fcntl, termios, struct
import argparse

def __to_int(string):
  return int(string, 0)

def __vcp_show(dsp: io.FileIO, idx: int, dsc: str):
  buf = bytes([0x01, idx])
  dsp.write(buf)
  buf = dsp.read(8)
  print('{}: {} / {}'.format(dsc, buf[7], buf[5]))
  return

def __vcp_set(dsp: io.FileIO, idx: int, val: int, dsc: str):
  buf = bytes([0x01, idx])
  dsp.write(buf)
  buf = dsp.read(8)
  if val != buf[7] and val <= buf[5]:
    print('{}: ({} -> {}) / {}'.format(dsc, buf[7], val, buf[5]))
    dsp.write(bytes([0x03, idx, 0x00, val]))

def __terminal_props():
  return struct.unpack(
    'HHHH',
    fcntl.ioctl(0, termios.TIOCGWINSZ,
      struct.pack('HHHH', 0, 0, 0, 0)
    )
  )

class HelpFormatter(argparse.HelpFormatter):
  def _format_action_invocation(self, action: argparse.Action) -> str:
    formatted = super()._format_action_invocation(action)
    if action.option_strings and action.nargs != 0:
      formatted = formatted.replace(
        f" {self._format_args(action, self._get_default_metavar_for_optional(action))}",
        "",
        len(action.option_strings) - 1,
      )
    return formatted

parser = argparse.ArgumentParser(
  formatter_class=
    lambda prog: HelpFormatter(
      prog, 
      max_help_position=int(__terminal_props()[0] * 0.5)
    )
  )
parser.add_argument(
  '-s', '--show', 
  dest='show', action="store_true", 
  help="show current values"
)
parser.add_argument(
  '-b', '--brightness',
  dest='bval', type=__to_int, default=argparse.SUPPRESS,
  help="set current brightness value"
)
parser.add_argument(
  '-c', '--contrast',
  dest='cval', type=__to_int, default=argparse.SUPPRESS,
  help="set current contrast value"
)
a = parser.parse_args()

if len(sys.argv) == 1:
  parser.print_help()
  exit(0)

for subdir, dirs, files in os.walk('/dev/bus/ddcci'):
  for file in files:
    path = os.path.join(subdir, file)
    with open(path, 'r+b', buffering = 0) as f:
      if (a.show):
        __vcp_show(f, 0x10, f'[{path}] brightness')
        __vcp_show(f, 0x12, f'[{path}] contrast')
      else:
      # brightness
        if hasattr(a, 'bval'):
          __vcp_set(f, 0x10, a.bval, f'[{path}] brightness')
      # contrast
        if hasattr(a, 'cval'):
          __vcp_set(f, 0x12, a.cval, f'[{path}] contrast')