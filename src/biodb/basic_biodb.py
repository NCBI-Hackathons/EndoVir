#  -------------------------------------------------------------------------------
#  \file basic_biodb.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#  -------------------------------------------------------------------------------
import os

class BasicBioDatabase:

  def __init__(self, name=None, dbdir=None, dbtype=None):
    self.name = name
    self.dbdir = dbdir
    self.dbtype = dbtype
    self.dbpath = None
    if name != None and dbdir != None:
      self.dbpath = os.path.join(self.dbdir, self.name)
