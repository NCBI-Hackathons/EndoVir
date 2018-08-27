"""
-------------------------------------------------------------------------------
\file database_manager.py
\author Jan P Buchmann <jan.buchmann@sydney.edu.au>
\copyright 2018 The University of Sydney
\version 0.0.0
\description
-------------------------------------------------------------------------------
"""
import io
import os
import sys

import utils.endovir_utils
from . import blastdb
from . import smpdb

class BiodbManager:

  dbs = {}

  def __init__(self, wd):
    self.wd = wd

  def initialize_databases(self, databases):
    for i in databases:
      if databases[i]['format'] == 'blast':
        if i not in BiodbManager.dbs:
          BiodbManager.dbs[i] = blastdb.BlastDatabase(databases[i]['directory'],
                                                      databases[i]['name'],
                                                      databases[i]['format'],
                                                      databases[i]['src'],
                                                      databases[i]['dbtype'],
                                                      databases[i]['client'],
                                                      databases[i]['tool'])
      BiodbManager.dbs[i].initialize(self.wd)


  def test_databases(self):
    for i in BiodbManager.dbs:
      status = BiodbManager.dbs[i].test()
      if not status.get_status('OK'):
        status.list_triggers()
        sys.exit("Error in database {} ({}):".format(BiodbManager.dbs[i].name,
                                                     BiodbManager.dbs[i].dbpath))
      print("Good databases {}".format(BiodbManager.dbs[i].name))


  def install_databases(self, databases):
    self.initialize_databases(databases)
    if len(self.wd) == 0:
      sys.exit("No initialized databases. Abort.")
    for i in BiodbManager.dbs:
      status = BiodbManager.dbs[i].test()
      if not status.get_status(status_name='OK'):
        self.make_database_directory(BiodbManager.dbs[i])
        BiodbManager.dbs[i].install()


  def make_database_directory(self, database):
    if not utils.endovir_utils.make_dir(database.dbdir):
      sys.exit("Cannot create database directory: {}.Abort.".format(database.dbdir))
