#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import status.endovir_status
import utils.endovir_utils
import utils.fasta_formatter
import utils.sequence_container
import toolbox.endovir_toolbox
import toolbox.vdb_tool
import biodb.blastdb
import contig.virus_contig
import contig.contigdb

class EndovirScanner:

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['RUNERR'])

  def __init__(self, screen):
    self.screen = screen
    self.virus_contigs = contig.contigdb.ContigDatabase(screen)
    self.flankdb = biodb.blastdb.BlastDatabase(name='endovir_flankdb',
                                               dbdir=os.path.join(screen.wd, 'endovir_dbs'),
                                               dbformat='blast',
                                               dbtype='nucl',
                                               client='blastdbcmd',
                                               tool='makeblastdb')
    self.flankdb.initialize(screen.wd)
    self.flankdb.tool.useStdin = True
    self.status = status.endovir_status.EndovirStatusManager(EndovirScanner.status_codes)

  def initial_scan(self, mapper, assembler, contig_screener):
    srr_mapper = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(mapper)
    srr_mapper.configure(self.get_settings())
    #status checkpoint
    investigator = srr_mapper.run(srr_mapper.assemble_process())
    #status checkpoint
    vdbtool = toolbox.vdb_tool.EndovirVdbTool(overwrite=False)
    reads = vdbtool.fetch_reads(self.screen.srr, investigator.get_result())
    #status checkpoint
    asm = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(assembler)
    asm.configure(self.get_settings())
    asm.add_reads(reads)
    investigator = asm.run(asm.assemble_process())
    evctgs = self.make_endovir_contigs(investigator.get_result())
    #status checkpoint
    ctg_screener = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(contig_screener)
    ctg_screener.configure(self.get_settings())
    ctg_screener.add_input_file(evctgs.path)
    investigator = ctg_screener.run(ctg_screener.assemble_process())
    ctg_screen_results = investigator.get_result()
    fdb_tool = self.flankdb.get_basic_tool()
    fdb_proc = fdb_tool.assemble_process()
    for i in ctg_screen_results.get_queries():
      if evctgs.contains(i.id):
        c = self.virus_contigs.add_contig(contig.virus_contig.VirusContig(evctgs.get_sequence(i.id), self.screen))
        fdb_proc.stdin.write(utils.fasta_formatter.FastaFormatter.format(c.lhs_flank.sequence))
        fdb_proc.stdin.write(utils.fasta_formatter.FastaFormatter.format(c.rhs_flank.sequence))
      else:
        evctgs.remove_sequence(i.id)
    fdb_proc.stdin.close()
    fdb_tool.run(fdb_proc)

    for i in self.virus_contigs.contigs_map:
      print(i, self.virus_contigs.contigs_map[i].length)
      print("LHS: len: {0}\tstart: {1}\tstop: {2}".format(self.virus_contigs.contigs_map[i].lhs_flank.get_length(),
                                                          self.virus_contigs.contigs_map[i].lhs_flank.get_start_pos(),
                                                          self.virus_contigs.contigs_map[i].lhs_flank.get_end_pos()))
      print("RHS: len: {0}\tstart: {1}\tstop: {2}".format(self.virus_contigs.contigs_map[i].rhs_flank.get_length(),
                                                          self.virus_contigs.contigs_map[i].rhs_flank.get_start_pos(),
                                                          self.virus_contigs.contigs_map[i].rhs_flank.get_end_pos()))
    #status checkpoint

  def get_settings(self):
    return {
            'wd' : self.screen.wd,
            'srr' : self.screen.srr,
            'asmdir' : self.screen.asm_dir,
            'virusdb' : self.screen.virus_db,
            'proteindb' : self.screen.prot_db
           }

  def make_endovir_contigs(self, contigs):
    ctg_num = 0
    fh = open(contigs.set_path(os.path.join(self.screen.asm_dir, self.screen.srr+".ev_ctgs")), 'w')
    for i in contigs.get_sequences():
      contigs.rename_sequence(i, "{0}-ctg{1:03d}".format(self.screen.srr, ctg_num))
      fh.write(utils.fasta_formatter.FastaFormatter.format(i))
      ctg_num += 1
    fh.close()
    return contigs

  def bud(self, mapper='magicblast'):
    for i in self.virus_contigs.get_contigs():
      mapper = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(mapper)
      mapper.configure(self.get_settings())
