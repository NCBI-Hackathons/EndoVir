#-------------------------------------------------------------------------------
#  \file blast_database.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Blast database base class.
#-------------------------------------------------------------------------------

import os
import sys
import tarfile
import urllib.request
import time

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import utils.endovir_utils
import toolbox.endovir_toolbox
from . import basic_biodb

class BlastDatabase(basic_biodb.BasicBioDatabase):

  tool = None
  client = None

  def __init__(self, dbdir, title, dbformat, dbtype, client, tool):
    super().__init__(name=title, dbdir=dbdir, dbformat=dbformat)
    self.dbtype = dbtype
    BlastDatabase.client = toolbox.endovir_toolbox.Toolbox().get_by_name(client)
    BlastDatabase.tool = toolbox.endovir_toolbox.Toolbox().get_by_name(tool)

  def initialize(self, wd):
    if not endovir_utils.isAbsolutePath(self.dbdir):
      self.dbdir = os.path.join(wd, self.dbdir)
    self.dbname = os.path.join(self.dbdir, self.dbname)

  def test(self):
    testOK = True
    if not endovir_utils.isDirectory(self.dbdir):
      print("Error: Not a database directory: {}".format(self.dbdir))
    if not self.isValidDatabase():
      print("Error: Not a valid {}::{} database: {}".format(self.dbformat,
                                                           self.dbtype,
                                                           self.dbname))
      testOK = False
    return testOK

  def make_db(self, fil=None):
    cmd = self.cmd + ['-dbtype', self.dbtyp, '-in', fil, '-out', os.path.join(self.dbdir, self.title), '-title', self.title]
    print(cmd)
    p = subprocess.Popen(cmd)
    while p.poll() == None:
      print("\rCreating db {}".format(self.title), end='')
      time.sleep(2)

    if p.returncode != 0:
      print("Creating db {} failed. Aborting.".format(self.title))
      raise RuntimeError()

  def make_db_stdin(self, stdout):
    cmd = self.cmd + ['-dbtype', self.dbtyp, '-out', os.path.join(self.dbdir, self.title), '-title', self.title]
    print(cmd)
    p = subprocess.Popen(cmd, stdin=stdout)

  def isValidDatabase(self):
    BlastDatabase.tool.clear_options()
    BlastDatabase.tool.add_options([{'-db': self.name}, {'-info':None}])
    pfh = BlastDatabase.tool.run()
    if BlastDatabase.tool.hasFinished(pfh):
      if pfh.returncode == 0:
        return True
    return False
  #def check(self):
    #if os.path.exists(self.dbdir):
      #if not self.dbtool.exists(os.path.join(self.dbdir, self.title)):
        #print("No Blast DB {0}. Did you run setup.sh?".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
        #sys.exit()
      #else:
        #print("\tfound local Blast DB {0}".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
    #else:
      #print("No Blast DB {0}. Did you run setup.sh?".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
      #sys.exit()
      #os.makedir(self.dbdir)
      #self.fetch_db(src)
      #self.make_db(src, self.title)

  def fetch_db(self, src, title):
    if src == 'Cdd':
      return
    print("Fetching database {} from {}".format(title, src))
    db = open(self.path, 'w')
    for i in src:
      dbgz = open('dbgz', 'wb')
      response = urllib.request.urlopen(i)
      dbgz.write(response.read())
      dbgz.close()
      f = gzip.open('dbgz', 'rb')
      db.write(f.read().decode())
      os.unlink('dbgz')
    db.close()
    #print("DB fetch placeholder for {0} to make db {1}".format(src, title))
