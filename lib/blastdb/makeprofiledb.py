#  makeprofiledb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import sys
import subprocess
from . import BlastDatabase

class Makeprofiledb(BlastDatabase):

  def __init__(self, typ):
    super().__init__(cmd='makeprofiledb', typ=typ)

  def make_db(self, src, title=None):
    cmd = [self.cmd, '-dbtype', self.typ, '-in', src, '-out', self.path]
    if title != None:
      cmd += ['-title', title]
    subprocess.run(cmd)
