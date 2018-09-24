#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import status.endovir_status
import utils.endovir_utils
import toolbox.endovir_toolbox
import toolbox.vdb_tool
import biodb.biodb_manager

class EndovirScanner:

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['RUNERR'])

  def __init__(self, screen):
    self.wd = screen.wd
    self.srr = screen.srr
    self.asm_dir = screen.asm_dir
    self.virus_db = screen.virus_db
    self.motif_db = screen.motif_db
    self.contigs = {}
    self.ctg_num = 0
    self.status = status.endovir_status.EndovirStatusManager(EndovirScanner.status_codes)

  def initial_scan(self, mapper='magicblast', assembler='megahit'):
    srr_mapper = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(mapper)
    srr_mapper.configure(self.get_settings())
    #status checkpoint
    investigator = srr_mapper.run(srr_mapper.assemble_process())
    #status checkpoint
    vdbtool = toolbox.vdb_tool.EndovirVdbTool(overwrite=False)
    reads = vdbtool.fetch_reads(self.srr, investigator.get_result())
    #status checkpoint
    asm = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(assembler)
    asm.configure(self.get_settings())
    asm.add_reads(reads)
    investigator = asm.run(asm.assemble_process())
    #status checkpoint
    rpsblast = toolbox.endovir_toolbox.EndovirToolbox.get_by_name('rpsblast')
    rpsblast.add_input_file(investigator.contigs)
    investigator = rpsblast.run(rpsblast.assemble_process())
    #for i in investigator.get_result():
      #self.contigs[i].metadata = {}
      #self.contigs[i].metadata['asm_name'] = self.contigs[i].name
      #self.contigs[i].name = "{0}-ctg-{1}".format(self.srr, self.ctg_num)
      #self.ctg_num += 1

    #status checkpoint
    print(self.contigs)

  def get_settings(self):
    return {
            'wd' : self.wd,
            'srr' : self.srr,
            'asmdir' : self.asm_dir,
            'virusdb' : self.virus_db,
            'motifdb' : self.motif_db
           }
