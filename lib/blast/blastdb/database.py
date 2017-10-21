#  blastdb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import gzip
import subprocess
#import ftplib

from . import blastdbcmd

class BlastDatabase:

  def __init__(self, cmd=None, dbdir=None, name=None, typ=None):
    self.cmd  = cmd
    self.title = name
    self.dbdir = dbdir
    self.typ  = typ
    self.dbtool = blastdbcmd.Blastdbcmd()
    self.path = os.path.join(self.dbdir, self.title)

  def make_db(self, fil=None):
    if fil == None:
      cmd = [self.cmd, '-dbtype', self.typ, '-out', os.path.join(self.dbdir, self.title), '-title', self.title]
      p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
      return p
    cmd = [self.cmd, '-dbtype', self.typ, '-in', fil, '-out', os.path.join(self.dbdir, self.title), '-title', self.title]
    subprocess.run(cmd)

  def make_db_from_stdin(self):
    cmd = [self.cmd, '-dbtype', self.typ, '-out', os.path.join(self.dbdir, self.title), '-title', self.title]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    return p

  def setup(self, src):
    if os.path.exists(self.dbdir):
      if not self.dbtool.exists(os.path.join(self.dbdir, self.title)):
        print("No Blast DB {0}".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
        if not os.path.exists(os.path.join(os.path.join(self.dbdir, self.title))):
          self.fetch_db(src, self.title)
        print("\tfound local data at {0}. Creating database".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
        self.make_db(data=os.path.join(self.dbdir, self.title))
      else:
        print("\tfound local Blast DB {0}".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
    else:
      os.makedir(self.dbdir)
      self.fetch_db(src)
      self.make_db(src, self.title)

  def fetch_db(self, src, title):
    print("DB fetch placeholder for {0} to make db {1}".format(src, title))
