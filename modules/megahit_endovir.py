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

class MegahitInvestigator:

  def __init__(self):
    self.contigs = None

  def parse_contigs(self):
    pass
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
    self.num_threads = 4
    self.min_contig_len_nt = 300
    self.tmp_dir = '/tmp'
    self.default_options = [{'--num-cpu-threads' : self.num_threads},
                            {'--min-contig-len' : self.min_contig_len_nt},
                            {'--tmp-dir' : self.tmp_dir},
                            {'--keep-tmp-files' : None}]
    self.add_options(self.default_options)
    self.suffix = '.contigs.fa'
    self.investigator = MegahitInvestigator()

  def configure(self, settings):
    self.add_options([{'--out-dir' : os.path.join(settings['asmdir'], settings['srr'])}])
    self.add_options([{'--out-prefix' : settings['srr']}])
    self.investigator.contigs = os.path.join(settings['asmdir'], settings['srr']) + self.suffix

  def add_reads(self, reads):
    self.add_options([{'--read' : reads}])
