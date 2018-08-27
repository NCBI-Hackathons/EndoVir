#-------------------------------------------------------------------------------
#  \file blastdb_installer.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import urllib
import gzip
#import tarfile

class BlastSequenceDatabaseInstaller:

  def __init__(self):
    self.tmp_dbfile = '/tmp/endovirdb'
    self.tmp_dbfile_comp = '/tmp/endovirdb.gz'

  def download(self, sourcelist):
    db = open(self.tmp_dbfile, 'w')
    for i in sourcelist:
      print("Downloading: {} -> {}".format(i, self.tmp_dbfile_comp))
      fh_tmp_dbfile_comp = open(self.tmp_dbfile_comp, 'wb')
      response = urllib.request.urlopen(i)
      fh_tmp_dbfile_comp.write(response.read())
      fh_tmp_dbfile_comp.close()
      print("Decompressing {} -> {}".format(self.tmp_dbfile_comp, self.tmp_dbfile))
      fh_tmp_dbfile = gzip.open(self.tmp_dbfile_comp, 'rb')
      db.write(fh_tmp_dbfile.read().decode())
      os.unlink(self.tmp_dbfile_comp)
    db.seek(0)
    db.close()
    if os.path.getsize(self.tmp_dbfile) > 0:
      return self.tmp_dbfile
    return None

  def install(self, db):
    db.tool.clear_options()
    db.tool.add_options([{'-dbtype' : db.dbtype},
                         {'-out' : db.dbpath},
                         {'-title' : db.name},
                         {'-in' : self.tmp_dbfile}])
    pfh = db.tool.run()
    if db.tool.hasFinished(pfh):
      if pfh.returncode == 0:
        os.unlink(self.tmp_dbfile)
        return True
    return False
