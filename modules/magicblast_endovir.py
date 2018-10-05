#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os

import biodb.biodb_manager
import toolbox.endovir_tool
import result.mapping_result

class MagicblastInvestigator:

  def __init__(self, fmt='tabular'):
    self.mapping_result = result.mapping_result.MappingResult()
    self.fmt = fmt

  def analyze_stdout(self, proc):
    if self.fmt == 'tabular':
      self.parse_tabular(proc.stdout)
    else:
      raise NotImplementedError("Parsing {} not implemented".format(self.fmt))

  def parse_tabular(self, mb_result):
    for i in mb_result:
      if i[0] != '#':
        cols = i.strip().split('\t')
        read = self.mapping_result.Read(cols[0],
                                        cols[0].split('.')[1],
                                        cols[6],
                                        cols[7],
                                        cols[13],
                                        cols[15])
        ref = self.mapping_result.Reference(cols[1], cols[8], cols[9], cols[14])
        self.mapping_result.add_mapping(read, ref)

  def get_result(self):
    return self.mapping_result

class EndovirModuleTool(toolbox.endovir_tool.EndovirTool):

  def __init__(self, name, path, role):
    super().__init__(name, path, role, useStdout=True)
    self.num_threads = 4
    self.outfmt = 'tabular'
    self.default_options = [{'-no_unaligned' : None},
                            {'-num_threads' : self.num_threads},
                            {'-outfmt' : self.outfmt},
                            {'-splice': 'F'},
                            {'-parse_deflines' : 'true'}]
    self.analyzer = MagicblastInvestigator(fmt=self.outfmt)

  def add_sra(self, sra):
    if os.path.isfile(sra):
      self.add_options([{'-query' : sra}])
    else:
      self.add_options([{'-sra' : sra}, {'-sra_cache' : None}])

  def configure(self, options):
    if 'sra' in options:
      self.add_sra(options['sra'])
    if 'db' in options:
      self.add_options([{'-db' : options['db']}])
    if 'subject' in options:
      self.add_options([{'-subject' : options['subject']}])
