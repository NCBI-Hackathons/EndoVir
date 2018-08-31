#-------------------------------------------------------------------------------
# \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2018 The University of Sydney
# \description
#-------------------------------------------------------------------------------

import io
import os
import sys

import utils.endovir_utils
from . import blastdb

class BiodbManager:

  dbs = {}

  @staticmethod
  def get_databases():
    if len (BiodbManager.dbs) == 0:
      return None
    return [BiodbManager.dbs[x] for x in BiodbManager.dbs]

  @staticmethod
  def get_database(dbname):
    return BiodbManager.dbs[dbname]

  @staticmethod
  def get_configurations():
    config = {}
    for i in BiodbManager.dbs:
      config.update(BiodbManager.dbs[i].get_configuration())
    return config

  @staticmethod
  def initialize_databases(wd, databases):
    print("Initializing databases", file=sys.stderr)
    for i in databases:
      if databases[i]['format'] == 'blast':
        if i not in BiodbManager.dbs:
          BiodbManager.dbs[i] = blastdb.BlastDatabase(i,
                                                      databases[i]['directory'],
                                                      databases[i]['format'],
                                                      databases[i]['dbtype'],
                                                      databases[i]['client'],
                                                      databases[i]['tool'],
                                                      databases[i].get('src'))
      BiodbManager.dbs[i].initialize(wd)
      print("\tInitializing {}".format(i), file=sys.stderr)
    print("Initializing databases: OK", file=sys.stderr)

  @staticmethod
  def test_databases():
    for i in BiodbManager.dbs:
      status = BiodbManager.dbs[i].test()
      if not status.get_status('OK'):
        status.list_triggers()
        sys.exit("Error in database {} ({}):".format(BiodbManager.dbs[i].name,
                                                     BiodbManager.dbs[i].dbpath))
      print("Good database {}".format(BiodbManager.dbs[i].name),file=sys.stderr)

  @staticmethod
  def install_databases(databases, email):
    print("Installing databases...", file=sys.stderr)
    BiodbManager.initialize_databases(databases)
    if len(BiodbManager.dbs) == 0:
      sys.exit("No initialized databases. Abort.")
    for i in BiodbManager.dbs:
      print("Installing database {}".format(BiodbManager.dbs[i].name), file=sys.stderr)
      status = BiodbManager.dbs[i].test()
      if status.get_status(status_name='OK'):
        print("Found installed database: {}".format(BiodbManager.dbs[i].name), file=sys.stderr)
      else:
        BiodbManager.make_database_directory(BiodbManager.dbs[i])
        status = BiodbManager.dbs[i].install()
        if not status.get_status(status_name='OK'):
          sys.exit("Error installing database {}".format(BiodbManager.dbs[i].name))
    print("Installing databases OK".format(BiodbManager.dbs[i].name), file=sys.stderr)

  @staticmethod
  def make_database_directory(database):
    if not utils.endovir_utils.make_dir(database.dbdir):
      sys.exit("Cannot create database directory: {}.Abort.".format(database.dbdir))

  def __init__(self):
    pass
