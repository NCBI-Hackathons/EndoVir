#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Semi-abstract base class for endovir tools. Assuming line based
#               standard I/O.
#               Thanks to Eli Bendersky [0]
#
# [0]: https://eli.thegreenplace.net/2017/interacting-with-a-long-running-child-process-in-python/
#-------------------------------------------------------------------------------

import sys
import time
import json
import threading
import subprocess

class EndovirTool:

  class StdoutInvestigator:

    def __init__(self):
      pass

    def investigate_stdout(self, proc):
      for i in proc.stdout:
        print(i)

  @staticmethod
  def observe(proc, wait=0.3):
    anim = ['\\\\O', ' O ', 'O//', ' O ']
    print(proc.args)
    while proc.poll() == None:
      for i in range(len(anim)):
        print("\rPID: {}, {}".format(proc.pid, anim[i]), end="", file=sys.stderr)
        time.sleep(wait)
    print(file=sys.stderr)
    return 0

  def __init__(self, name, path, role):
    self.name = name
    self.path = path
    self.role = role
    self.option_map = {}
    self.option_list = []
    self.investigator = None
    self.useStdin = False
    self.useStdout = False

  def get_configuration(self):
    return {self.role: {self.name : self.path}}

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

  def assemble_process(self):
    cmd = [self.path]
    for i in self.option_list:
      if self.option_map[i] == None:
        cmd.append(i)
      else:
        cmd += [i, str(self.option_map[i])]
    return subprocess.Popen(cmd,
                            stdin=subprocess.PIPE if self.useStdin else None,
                            stdout=subprocess.PIPE if self.useStdout else None,
                            bufsize=1,
                            universal_newlines=True)

  def run(self, process):
    t = None
    if self.useStdout:
      t = threading.Thread(target=self.investigator.investigate_stdout, args=(process, ))
    s = threading.Thread(target=EndovirTool.observe, args=(process, ))
    if t != None:
      t.start()
    s.start()
    if t != None:
      t.join()
    s.join()
    return self.investigator
