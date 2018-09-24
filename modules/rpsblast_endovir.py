#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os

import biodb.biodb_manager
import toolbox.endovir_tool
import result.mapping_result
import bioparser.blast.blast_json

class RpsblastInvestigator:

  def __init__(self, fmt='json'):
    #self.blast_result = result.blast.BlastResult()
    self.fmt = fmt

  def investigate_stdout(self, proc):
    if self.fmt == 'json':
      p = bioparser.blast.blast_json.BlastParser()
      p.parse(proc.stdout)
    else:
      raise NotImplementedError("Parsing {} not implemented".format(self.fmt))

  def investigate(self, src):
    if self.fmt == 'json':
      fh = open(src, 'r')
      p = bioparser.blast.blast_json.BlastParser()
      p.parse(fh)
      fh.close()
    else:
      raise NotImplementedError("Parsing {} not implemented".format(self.fmt))


class EndovirModuleTool(toolbox.endovir_tool.EndovirTool):

  def __init__(self, name, path, role, db='endovir_cdd'):
    super().__init__(name, path, role, useStdout=True)
    self.max_eval = 0.001
    self.num_threads = 0
    self.outfmt = 15
    self.default_options = [{'-num_threads' : self.num_threads},
                            {'-outfmt' : self.outfmt},
                            {'-splice': 'F'},
                            {'-evalue' : self.max_eval}]
    self.add_options(self.default_options)
    self.investigator = RpsblastInvestigator(fmt=self.outfmt)

  def configure(self, settings):
    db  = biodb.biodb_manager.BiodbManager.get_database(settings['motifdb'])
    self.add_options([{'-db' : db.dbpath}])

  def add_input_file(self, fname):
    self.add_options([{'-query' : fname}])
