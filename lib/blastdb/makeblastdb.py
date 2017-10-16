#  makeblastdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import subprocess
from . import database

class Makeblastdb(database.BlastDatabase):

  def __init__(self, path, typ):
    super().__init__(path=path, cmd='makeblastdb', typ=typ)

  def make_db(self, src, title=None):
    cmd = [self.cmd, '-dbtype', self.typ, '-in', src, '-out', self.path]
    if title != None:
      cmd += ['-title', title]
    subprocess.run(cmd)
    # Would love to pipe the sequences into makeblastdb but need to figure out
    # how to pass a stream into a method
    #subprocess.Popen([self.cmd, '-dbtype', self.typ,
                              #'-in', filepath,
                              #'-out', self.path],
                                       #stdout=subprocess.PIPE,
                                       #bufsize=1)
    subprocess.run([self.cmd, '-dbtype', self.typ,
                              '-in', src,
                              '-out', self.path])
