#  blastdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

from . import blastdbcmd

class BlastDatabase:

  def __init__(self, cmd=None, name=None, path=None, typ=None):
    self.cmd = cmd
    self.name = name
    self.typ = typ
    self.path = path
    self.dbtool = blastdbcmd.Blastdbcmd()

  def make_db(self, src=None, title=None):
    pass

  def setup(self, src, path, title):
    if os.path_exists(path):
      if not self.dbtool.exists(title):
        self.make_db(src, path, title)
    else:
      self.make_db(src, path, title)
