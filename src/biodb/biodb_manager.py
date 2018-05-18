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

from . import blastdb
from . import smpdb

class BiodbManager:

  def __init__(self, toolbox):
    self.dbdir = None
    self.dbs = {}
    self.toolbox = toolbox

  def configure(self, dbdir, config):
    self.dbdir = dbdir
    self.initialize_databases(config)

  def initialize_databases(self, dbs):
    for i in dbs:
      if i == 'blast_databases':
        self.initialize_blast_databases(dbs[i])
    self.list_databases()

  def list_databases(self):
    for i in self.dbs:
      print(i, self.dbs[i].name, self.dbs[i].tool)

  def initialize_blast_databases(self, dbs):
    for i in dbs:
      print(i, dbs[i]['dbtype'])
      if dbs[i]['dbtype'] == 'smp':
        self.dbs[i] = smpdb.SmpDatabase(self.dbdir, dbs[i]['name'],
                                        dbs[i]['dbtype'], dbs[i]['client'],
                                        dbs[i]['tool'])
      else:
        self.dbs[i] = blastdb.BlastDatabase(self.dbdir, dbs[i]['name'],
                                            dbs[i]['dbtype'], dbs[i]['client'],
                                            dbs[i]['tool'])
  def test_databases(self):
    for i in self.dbs:
      if not self.dbs[i].isValidDatabase(self.toolbox):
        print("Not a valid database: ", i, self.dbs[i].name)
