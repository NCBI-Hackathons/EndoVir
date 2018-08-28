#-------------------------------------------------------------------------------
#  \file basic_biodb.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Basic database class handling biological databases. Since \
#               databases can differ in type (sequences, motifs, etc) and format
#               (e.g. NCBI is different than DIAMOND), it constitutes a
#               general template. It used virtual methods to allow calling
#               common operations without the need to know what data base it
#               actually is.
#               If the directory of the databse is not absolute, it assumes a
#               relative path in relation to the working directory.
#-------------------------------------------------------------------------------

class BasicBioDatabase:

  ## Constructor
  # @input name, str, database name
  # @input dbdir, str, database directory
  # @input dbformat, str, database format
  def __init__(self, name=None, dbdir=None, dbformat=None, source=None):
    self.name = name
    self.dbdir = dbdir
    self.dbformat = dbformat
    self.source = source
    self.dbpath = None

  ## Initialize database
  # Virtual method
  #@input wd, str, working directory.
  def initialize(self, wd):
    raise NotImplementedError("Help! Need implementation")

  ## Install database
  # Virtual method
  def install(self):
    raise NotImplementedError("Help! Need implementation")


  ## Test database
  # Virtual method
  #@input wd, str, working directory.
  #@return status, bool
  def test(self):
    raise NotImplementedError("Help! Need implementation")
