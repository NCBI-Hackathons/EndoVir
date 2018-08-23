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
                                                      databases[i]['dbtype'],
                                                      databases[i]['client'],
                                                      databases[i]['tool'])
      BiodbManager.dbs[i].initialize(self.wd)


  def test_databases(self):
    for i in BiodbManager.dbs:
      if BiodbManager.dbs[i].test():
        print("Good databases {}".format(i))
      else:
        print("Error in testing databases {}".format(i))

  def fetch_databases(self, databases, toolbox):
    for i in databases:
      db = None
      if i['format'] == 'blast':
        db = blastdb.BlastDatabase(databases[i]['directory'],
                                   databases[i]['name'],
                                   databases[i]['format'],
                                   databases[i]['client'],
                                   databases[i]['tool'])
