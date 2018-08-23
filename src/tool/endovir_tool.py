#-------------------------------------------------------------------------------
#  \file tool.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.1
#  \description Semi-abstract base class for assemblers.
#-------------------------------------------------------------------------------
import time
import json
import subprocess

class EndovirTool:

  def __init__(self, name, path, role):
    self.name = name
    self.path = path
    self.role = role
    self.option_map = {}
    self.option_list = []

  def update_options(self, options):
    for i in options:
      if i in self.option_map:
        self.option_map[i] = options[i]

  def clear_options(self):
    self.option_map = {}
    self.option_list = []

  def add_options(self, option_list):
    for i in option_list:
      for j in i:
        self.option_list.append(j)
        self.option_map[j] = i[j]

  def run(self):
    cmd = [self.path]
    for i in self.option_list:
      if self.option_map[i] == None:
        cmd.append(i)
      else:
        cmd += [i, self.option_map[i]]
    print(cmd)
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            bufsize=1, universal_newlines=True)

  def hasFinished(self, pfh, wait=0.5):
    while pfh.poll() == None:
      print("\r PID: {}\tRole: {}\t{}".format(pfh.pid, self.role, pfh.args), end='')
      time.sleep(wait)
    return True
