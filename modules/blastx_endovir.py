#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os

import biodb.biodb_manager
import toolbox.endovir_tool
import bioparser.blast.blast_json
import result.blast_result

class BlastxInvestigator:

  def __init__(self, fmt='tabular'):
    self.fmt = fmt

  def __init__(self, fmt):
    self.blast_result = result.blast_result.BlastResult()
    self.fmt_map = {15 : 'json'}
    self.fmt = self.fmt_map[fmt]

  def investigate_stdout(self, proc):
    if self.fmt == 'json':
      p = bioparser.blast.blast_json.BlastParser()
      p.parse(proc.stdout)
      self.analyze_result(p)
    else:
      raise NotImplementedError("Parsing {} not implemented".format(self.fmt))

  def investigate(self, src):
    if self.fmt == 'json':
      fh = open(src, 'r')
      p = bioparser.blast.blast_json.BlastParser()
      p.parse(fh)
      fh.close()
      self.analyze_result(p)
    else:
      raise NotImplementedError("Parsing {} not implemented".format(self.fmt))

  def analyze_result(self, parser):
    self.blast_result = result.blast_result.BlastResult(parser.querymap, parser.hitmap, parser.hspmap)

  def get_result(self):
    return self.blast_result

class EndovirModuleTool(toolbox.endovir_tool.EndovirTool):

  def __init__(self, name, path, role):
    super().__init__(name, path, role, useStdout=True)
    self.num_threads = 4
    self.outfmt = 15
    self.default_options = [{'-outfmt' : self.outfmt},
                            {'-parse_deflines' : None},
                            {'-num_threads' : self.num_threads}]
    self.add_options(self.default_options)
    self.investigator = BlastxInvestigator(fmt=self.outfmt)

  def configure(self, settings):
    db  = biodb.biodb_manager.BiodbManager.get_database(settings['proteindb'])
    self.add_options([{'-db' : db.dbpath}])

  def add_input_file(self, fname):
    self.add_options([{'-query' : fname}])
