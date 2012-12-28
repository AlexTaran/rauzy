#!/usr/bin/python

import sys

def main():
  if len(sys.argv) != 2:
    sys.stderr.write('Wrong number of args. Need <mask_filename>')
  with open(sys.argv[1]) as mask_file:
    for line in sys.stdin:
      mask_value = int(mask_file.readline().strip())
      if mask_value != 0:
        sys.stdout.write(line)

if __name__ == "__main__":
  main()
