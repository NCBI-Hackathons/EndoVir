#  -------------------------------------------------------------------------------
#  \file smpdb.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------

import os
import sys

class SmpDatabase(basic_biodb.BasicBioDatabase):

  def __init__(self, dbdir=None, title=None, dbtype=None, dbstyle=None):
    super().__init__(name=title, dbdirpath=executable, role='blastdb')

  def add_client(self, client):
    pass
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

  def isDatabase(self):
    self.clear_options()
    self.add_options([{'-db' : self.path},{'-info': None}])
    pfh = self.run()
    if self.hasFinished(pfh):
      if pfh.returncode == 0:
        return True
      return False

  def check(self):
    if os.path.exists(self.dbdir):
      if not self.dbtool.exists(os.path.join(self.dbdir, self.title)):
        print("No Blast DB {0}. Did you run setup.sh?".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
        sys.exit()
      else:
        print("\tfound local Blast DB {0}".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
    else:
      print("No Blast DB {0}. Did you run setup.sh?".format(os.path.join(self.dbdir, self.title), file=sys.stderr))
      sys.exit()
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
