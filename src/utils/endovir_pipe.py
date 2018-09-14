#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys

from . import endovir_utils

class EndovirPipe:

  def __init__(self, name):
    self.name = name + '.evpipe'
    self.path = os.path.join('/tmp/', self.name)
    self.check()
    #os.mkfifo(self.path)

  def open(self):
    self.fh = open(self.path, 'w')
    return self.fh

  def close(self):
    self.fh.close()

  def check(self):
    if endovir_utils.pathExists(self.path):
      print("Endovir pipe {} already exists. Recreating".format(self.path))
      os.unlink(self.path)
