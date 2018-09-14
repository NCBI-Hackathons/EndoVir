#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os

import biodb.biodb_manager
import toolbox.endovir_tool
import result.mapping_result

class RpsblastInvestigator:

  def __init__(self, fmt='json'):
    pass
    #self.mapping_result = result.mapping_result.MappingResult()
    #self.fmt = fmt

  #def investigate_stdout(self, proc):
    #if self.fmt == 'tabular':
      #self.parse_tabular(proc.stdout)
    #else:
      #raise NotImplementedError("Parsing {} not implemented".format(self.fmt))

  #def parse_tabular(self, mb_result):
    #for i in mb_result:
      #if i[0] != '#':
        #cols = i.strip().split('\t')
        #read = self.mapping_result.Read(cols[0],
                                        #cols[0].split('.')[1],
                                        #cols[6],
                                        #cols[7],
                                        #cols[13],
                                        #cols[15])
        #ref = self.mapping_result.Reference(cols[1], cols[8], cols[9], cols[14])
        #self.mapping_result.add_mapping(read, ref)

class EndovirModuleTool(toolbox.endovir_tool.EndovirTool):

  def __init__(self, name, path, role):
    super().__init__(name, path, role)
    self.max_eval = 0.001
    self.num_threads = 4
    self.outfmt = 15
    self.default_options = [{'-num_threads' : self.num_threads},
                            {'-outfmt' : self.outfmt},
                            {'-splice': 'F'},
                            {'-evalue' : self.max_eval = 0.001}]
    self.add_options(self.default_options)
    self.investigator = MagicblastInvestigator(fmt=self.outfmt)
    self.useStdout = True

  def configure(self, settings):
    if os.path.isfile(settings['srr']):
      self.add_options([{'-query' : settings['srr']}])
    else:
      self.add_options([{'-sra' : settings['srr']}, {'-sra_cache' : None}])
    db  = biodb.biodb_manager.BiodbManager.get_database(settings['virusdb'])
    self.add_options([{'-db' : db.dbpath}])
