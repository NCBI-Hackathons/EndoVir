#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
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

  def __init__(self, name, dbdir, dbformat, dbtype, client, tool, source=None):
    super().__init__(name=name, dbdir=dbdir, dbformat=dbformat, source=source)
    self.dbtype = dbtype
    self.tool = toolbox.endovir_toolbox.EndovirToolbox().get_by_name(tool)
    self.status = status.endovir_status.EndovirStatusManager(BlastDatabase.status_codes)
    BlastDatabase.client = toolbox.endovir_toolbox.EndovirToolbox().get_by_name(client)

  def get_basic_tool(self):
    self.tool.clear_options()
    self.tool.add_options([{'-dbtype' : self.dbtype},
                           {'-out' : self.dbpath},
                           {'-title' : self.name},
                           {'-parse_seqids' : None},
                           {'-hash_index' : None}])
    return self.tool

  def get_configuration(self):
    return {
            self.name :
            {
              'directory' : os.path.abspath(self.dbdir),
              'format' : self.dbformat,
              'dbtype' : self.dbtype,
              'client' : BlastDatabase.client.name,
              'tool' : self.tool.name
             }
           }

  def initialize(self, wd):
    if not utils.endovir_utils.isAbsolutePath(self.dbdir):
      self.dbdir = os.path.join(wd, self.dbdir)
    self.dbpath = os.path.join(self.dbdir, self.name)

  def test(self):
    if not utils.endovir_utils.isDirectory(self.dbdir):
      self.status.set_status('PATHERR', self.dbdir)
      return self.status
    if not self.isValidDatabase():
      self.status.set_status('DBERR', 'nonvalid')
      return self.status
    return self.status

  def isValidDatabase(self):
    BlastDatabase.client.clear_options()
    BlastDatabase.client.add_options([{'-db':self.dbpath}, {'-info':None,
                                                            '-out':'/dev/null'}])
    if BlastDatabase.client.run(BlastDatabase.client.assemble_process()) == None:
      return False
    return True

  def install(self, email=None):
    dbi = blastdb_installer.BlastSequenceDatabaseInstaller()
    if self.dbtype == 'rps':
      dbi = blastdb_installer.BlastMotifDatabaseInstaller(email)
    if dbi.download(self.source) == None:
      self.status.set_status('FETCHERR', 'download_fail')
      return self.status
    if not dbi.install(self):
      self.status.set_status('DBERR', 'install')
      return self.status
    return self.status
