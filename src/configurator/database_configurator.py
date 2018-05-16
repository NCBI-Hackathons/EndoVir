#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  -------------------------------------------------------------------------------
#  \file database_config.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------

import io
import os
import sys

import blast_wrapper.blastdb

class DatabaseConfigurator:

  def __init__(self):
    self.databases = {}

  def config(self, dbs, dbdir, toolshed):
    self.find_missing_databases(dbs, dbdir, toolshed)

  def find_missing_databases(self, dbs, dbdir):
    pass
    #for i in dbs:
      #db = blast_wrapper.blastdb.BlastDatabase(executable=dbs[i]['tool'], dbdir=dbdir,
                                               #title=dbs[i]['name'], dbtype=dbs[i]['dbtype'])

      #if db.isDatabase():
        #self.databases[db.title] = db
      #else:
        #self.databases[db.title] = None
    #print(self.databases)
