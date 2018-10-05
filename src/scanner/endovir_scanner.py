#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import status.endovir_status
import utils.fasta_formatter
import toolbox.endovir_toolbox
import toolbox.vdb_tool
import biodb.blastdb
import biodb.biodb_manager
import contig.virus_contig
import bud.flank_extender

class EndovirScanner:

  status_codes = status.endovir_status.EndovirStatusManager.set_status_codes(['RUNERR'])

  def __init__(self, screen):
    self.screen = screen
    self.virus_contigs = {}
    self.flankdb = biodb.blastdb.BlastDatabase(name='endovir_flankdb',
                                               dbdir=os.path.join(screen.wd, 'endovir_dbs'),
                                               dbformat='blast',
                                               dbtype='nucl',
                                               client='blastdbcmd',
                                               tool='makeblastdb')
    self.flankdb.initialize(screen.wd)
    self.status = status.endovir_status.EndovirStatusManager(EndovirScanner.status_codes)

  def initial_scan(self, sra_mapper, assembler, contig_screener):
    sramap = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(sra_mapper)
    sramap.configure({'sra':self.screen.srr, 'db':self.screen.virus_db.dbpath})
    #status checkpoint
    asm = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(assembler)
    asm.configure({'out-dir':self.screen.asm_dir,
                   'out-prefix':self.screen.srr,
                   'read':toolbox.vdb_tool.EndovirVdbTool(overwrite=False).fetch_reads(self.screen.srr,
                                                                  sramap.run(sramap.assemble_process()).get_result())})
    evctgs = self.make_endovir_contigs(asm.run(asm.assemble_process()).get_result())
    #status checkpoint
    ctg_screener = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(contig_screener)
    ctg_screener.configure({'db':self.screen.prot_db.dbpath, 'query':evctgs.path})
    fdb_tool = self.flankdb.get_basic_tool(useStdin=True)
    fdb_proc = fdb_tool.assemble_process()
    for i in ctg_screener.run(ctg_screener.assemble_process()).get_result().get_queries():
      if evctgs.contains(i.id):
        self.virus_contigs[i.id] = contig.virus_contig.VirusContig(evctgs.get_sequence(i.id), self.screen)
        fdb_proc.stdin.write(utils.fasta_formatter.FastaFormatter.format(self.virus_contigs[i.id].lhs_flank.sequence))
        fdb_proc.stdin.write(utils.fasta_formatter.FastaFormatter.format(self.virus_contigs[i.id].rhs_flank.sequence))
      else:
        evctgs.remove_sequence(i.id)
    fdb_proc.stdin.close()
    fdb_tool.run(fdb_proc)
    #status checkpoint
    for i in self.virus_contigs:
      print(i, self.virus_contigs[i].length)
      print("LHS: len: {0}\tstart: {1}\tstop: {2}".format(self.virus_contigs[i].lhs_flank.get_length(),
                                                          self.virus_contigs[i].lhs_flank.get_start_pos(),
                                                          self.virus_contigs[i].lhs_flank.get_end_pos()))
      print("RHS: len: {0}\tstart: {1}\tstop: {2}".format(self.virus_contigs[i].rhs_flank.get_length(),
                                                          self.virus_contigs[i].rhs_flank.get_start_pos(),
                                                          self.virus_contigs[i].rhs_flank.get_end_pos()))

  def make_endovir_contigs(self, contigs):
    ctg_num = 0
    fh = open(contigs.set_path(os.path.join(self.screen.asm_dir, self.screen.srr+".ev_ctgs")), 'w')
    for i in contigs.get_sequences():
      contigs.rename_sequence(i, "{0}-ctg{1:03d}".format(self.screen.srr, ctg_num))
      fh.write(utils.fasta_formatter.FastaFormatter.format(i))
      ctg_num += 1
    fh.close()
    return contigs

  def bud(self, sra_mapper):
    mapper = toolbox.endovir_toolbox.EndovirToolbox.get_by_name(sra_mapper)
    mapper.configure({'sra':self.screen.srr, 'db':self.flankdb.dbpath})
    fle = bud.flank_extender.FlankExtender()
    fle.extend(mapper.run(mapper.assemble_process()).get_result())
