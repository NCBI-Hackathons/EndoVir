#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys

#sys.path.insert(1, os.path.join(sys.path[0], '../src/'))
import toolbox.endovir_tool
import result.mapping_result

class MagicblastInvestigator:

  def __init__(self, fmt='tabular'):
    self.mappings = []
    self.fmt = fmt

  def investigate_stdout(self, proc):
    if self.fmt == 'tabular':
      self.parse_tabular(proc.stdout)
    else:
      raise NotImplementedError("Parsing {} not implemented".format(self.fmt))

  def parse_tabular(self, mb_result):
    for i in mb_result:
      if i[0] != '#':
        cols = i.strip().split('\t')
        read = result.mapping_result.MappingResult.Read(cols[0],
                                                        cols[0].split('.')[1],
                                                        cols[6],
                                                        cols[7],
                                                        cols[13],
                                                        cols[15])
        ref =  result.mapping_result.MappingResult.Reference(cols[1],
                                                             cols[8],
                                                             cols[9],
                                                             cols[14])
        self.mappings.append(result.mapping_result.MappingResult(read, ref))


class EndovirModuleTool(toolbox.endovir_tool.EndovirTool):

  def __init__(self, name, path, role):
    super().__init__(name, path, role)
    self.num_threads = 4
    self.outfmt = 'tabular'
    self.default_options = [{'-no_unaligned' : None},
                            {'-num_threads' : self.num_threads},
                            {'-outfmt' : self.outfmt},
                            {'-splice': 'F'},
                            {'-parse_deflines' : 'true'}]
    self.add_options(self.default_options)
    self.investigator = MagicblastInvestigator(fmt=self.outfmt)
    self.useStdout = True

  def add_srr(self, srr):
    if os.path.isfile(srr):
      self.add_options([{'-query' : srr}])
    else:
      self.add_options([{'-sra' : srr}, {'-sra_cache' : None}])


  def add_database(self, db):
    self.add_options([{'-db' : db.dbpath}])
