#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------


import io
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../src/toolbox'))
import endovir_tool

class EndovirModuleTool(endovir_tool.EndovirTool):

  def __init__(self, name, path, role):
    super().__init__(name, path, role)
    self.num_threads = 4
    self.outfmt = 'tabular'
    self.default_options = [{'-no_unaligned' : None},
                            {'-num_threads' : self.num_threads},
                            {'-outfmt' : self.outfmt},
                            {'-splice': 'F'}]
    self.add_options(self.default_options)

  def add_srr(self, srr):
    if os.path.isfile(srr):
      self.add_options([{'-query' : srr}])
    else:
      self.add_options([{'-sra' : srr}])

  def add_database(self, db):
    self.add_options([{'-db' : db.dbpath}])


  def parse(self):
    pass
