#-------------------------------------------------------------------------------
#  \file blast_database.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Blast database base class.
#-------------------------------------------------------------------------------

import os
import sys
import time
import enum
import tarfile
import urllib.request

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import utils.endovir_utils
import toolbox.endovir_toolbox
import status.endovir_status
from . import basic_biodb
from . import blastdb_installer

class BlastDatabase(basic_biodb.BasicBioDatabase):

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['PATHERR', 'DBERR', 'FETCHERR'])
  client = None

  def __init__(self, dbdir, title, dbformat, source, dbtype, client, tool):
    super().__init__(name=title, dbdir=dbdir, dbformat=dbformat, source=source)
    self.dbtype = dbtype
    self.tool = toolbox.endovir_toolbox.EndovirToolbox().get_by_name(tool)
    BlastDatabase.client = toolbox.endovir_toolbox.EndovirToolbox().get_by_name(client)

  def initialize(self, wd):
    if not utils.endovir_utils.isAbsolutePath(self.dbdir):
      self.dbdir = os.path.join(wd, self.dbdir)
    self.dbpath = os.path.join(self.dbdir, self.name)

  def test(self):
    dbstatus = status.endovir_status.EndovirStatusManager(BlastDatabase.status_codes)
    if not utils.endovir_utils.isDirectory(self.dbdir):
      dbstatus.set_status('PATHERR', self.dbdir)
      return dbstatus
    if not self.isValidDatabase():
      dbstatus.set_status('DBERR', 'nonvalid')
      return dbstatus
    return dbstatus

  def isValidDatabase(self):
    BlastDatabase.client.clear_options()
    BlastDatabase.client.add_options([{'-db': self.name}, {'-info':None}])
    pfh = BlastDatabase.client.run()
    if BlastDatabase.client.hasFinished(pfh):
      if pfh.returncode == 0:
        return True
    return False

  def install(self):
    dbstatus = status.endovir_status.EndovirStatusManager(BlastDatabase.status_codes)
    if self.dbtype == 'smp':
      return 0
    dbi = blastdb_installer.BlastSequenceDatabaseInstaller()
    if dbi.download(self.source) == None:
      return dbstatus.set_status('FETCH', 'download_fail')
    if not dbi.install(self):
      return dbstatus.set_status('DBERR', 'install')
    return dbstatus
