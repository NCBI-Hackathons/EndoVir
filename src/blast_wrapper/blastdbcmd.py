#-------------------------------------------------------------------------------
#  \file blastdbcmd.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------

from process import basic_process

class BlastDatabaseClient(basic_process.BasicProcess):

  def __init__(self, executable, dbtype):
    super().__init__(name='blastdbcmd', path=executable, role='blastdb_client')
    self.dbtype = dbtype
