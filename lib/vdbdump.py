# -*- coding: utf-8 -*-
#
#  vdbdump.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import json
import subprocess

class VdbDump:

  def __init__(self):
    self.cmd = 'vdb-dump'
    self.format = 'json'

  def run(self, srr):
    vd = subprocess.Popen([self.cmd, '--format', self.format, srr],
                                  stdout=subprocess.PIPE, bufsize=1)
    row = ''
    status = 0
    while True:
      char = vd.stdout.read(1).decode()
      print(char, status)
      if len(char) == 0:
        break
      while status == 0:
        char = vd.stdout.read(1).decode()
        if char == '{':
          row = char
          status = 1

      while status == 1:
        char = vd.stdout.read(1).decode()
        if char == '}':
          row += char
          print(row)
          rowobj = json.loads(row)
          status = 2
          continue
        row += char

      while status == 2:
        char = vd.stdout.read(1).decode()
        if char == ',':
          continue
        if char == '\n':
          continue
        if char == '}':
          status = 0
