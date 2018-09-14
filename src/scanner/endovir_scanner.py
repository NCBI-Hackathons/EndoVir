#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys

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
    self.status = status.endovir_status.EndovirStatusManager(EndovirScanner.status_codes)

  def initial_scan(self, mapper='magicblast', assembler='megahit'):
    #srr_mapper = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(mapper)
    #srr_mapper.configure(self.get_settings())
    #proc = srr_mapper.assemble_process()
    ##staus checkpoint
    #investigator = srr_mapper.run(proc)
    ##staus checkpoint
    #vdbtool = toolbox.vdb_tool.EndovirVdbTool()
    #reads = vdbtool.fetch_reads(self.srr, investigator.mapping_result)
    ##staus checkpoint
    asm = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(assembler)
    asm.configure(self.get_settings())
    #asm.add_reads(reads)
    proc = asm.assemble_process()
    investigator = asm.run(proc)
    investigator.parse_contigs()
    #staus checkpoint

  def get_settings(self):
    return {
            'wd' : self.wd,
            'srr' : self.srr,
            'asmdir' : self.asm_dir,
            'virusdb' : self.virus_db
           }
