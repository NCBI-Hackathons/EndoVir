#-------------------------------------------------------------------------------
#  \file blastdb_installer.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Blast database donwload and install.
#-------------------------------------------------------------------------------

import os
import sys
import gzip
import urllib
import tarfile

sys.path.insert(1, os.path.join(sys.path[0], '../include/ncbipy_eutils/src'))
import edbase.edanalyzer
import callimachus.ncbi_callimachus

class BlastSequenceDatabaseInstaller:

  def __init__(self):
    self.tmp_dbfile = '/tmp/endovirdb'
    self.tmp_dbfile_comp = '/tmp/endovirdb.gz'

  def download(self, sourcelist):
    db = open(self.tmp_dbfile, 'w')
    for i in sourcelist:
      print("Downloading: {} -> {}".format(i, self.tmp_dbfile_comp), file=sys.stderr)
      fh_tmp_dbfile_comp = open(self.tmp_dbfile_comp, 'wb')
      response = urllib.request.urlopen(i)
      fh_tmp_dbfile_comp.write(response.read())
      fh_tmp_dbfile_comp.close()
      print("Decompressing {} -> {}".format(self.tmp_dbfile_comp, self.tmp_dbfile), file=sys.stderr)
      fh_tmp_dbfile = gzip.open(self.tmp_dbfile_comp, 'rb')
      db.write(fh_tmp_dbfile.read().decode())
    db.close()
    if os.path.getsize(self.tmp_dbfile) > 0:
      return self.tmp_dbfile
    return None

  def install(self, db):
    db.tool.clear_options()
    db.tool.add_options([{'-dbtype' : db.dbtype},
                         {'-out' : db.dbpath},
                         {'-title' : db.name},
                         {'-parse_seqids' : None},
                         {'-hash_index' : None},
                         {'-in' : self.tmp_dbfile}])
    proc = db.tool.assemble_process()
    db.tool.run(proc)
    if proc.returncode == 0:
      self.clean_up()
      return True
    return False

  def clean_up(self):
    print("Cleaning up:", file=sys.stderr)
    for i in [self.tmp_dbfile, self.tmp_dbfile_comp]:
      print("Deleting: {}".format(i), file=sys.stderr)
      os.unlink(i)

class BlastMotifDatabaseInstaller:

  class DocsumAnalyzer(edbase.edanalyzer.EdAnalyzer):

    def __init__(self):
      super().__init__()
      self.accessions = {}

    def analyze_result(self, response, request):
      for i in response['result']['uids']:
        self.accessions[response['result'][i]['accession']+'.smp'] = 0

  def __init__(self, email):
    self.tmp_dir = '/tmp'
    self.tmp_dbfile_comp = os.path.join(self.tmp_dir, 'endovircdddb.gz')
    self.tmp_pssm_file = os.path.join(self.tmp_dir, 'endovircdddb.pssm')
    self.email = email

  def download(self, sourcelist):
    accessions = self.get_virus_pssm()
    fh_pssm = open(self.tmp_pssm_file, 'w')
    for i in sourcelist:
      print("Downloading: {} -> {}".format(i, self.tmp_dbfile_comp), file=sys.stderr)
      print("Extracting PSSM's", file=sys.stderr)
      tar = tarfile.open(self.tmp_dbfile_comp, "r:*")
      for j in tar:
        if j.name in accessions:
          fh_pssm.write(os.path.join(self.tmp_dir, j.name)+'\n')
          tar.extract(j, self.tmp_dir)
    fh_pssm.close()
    return self.tmp_pssm_file

  def install(self, db):
    db.tool.clear_options()
    db.tool.add_options([{'-title' : db.name},
                         {'-in' : self.tmp_pssm_file},
                         {'-out' :  db.dbpath},
                         {'-threshold' : 9.82},
                         {'-scale' : 100},
                         {'-dbtype' : db.dbtype},
                         {'-index' : 'true'}])
    pfh = db.tool.run()
    if db.tool.hasFinished(pfh):
      if pfh.returncode == 0:
        #os.unlink(self.tmp_dbfile)
        return True
    return False

  def get_virus_pssm(self):
    print("Fetching virus PSSM accessions", file=sys.stderr)
    nc = callimachus.ncbi_callimachus.NcbiCallimachus(self.email)
    qry = nc.new_query()
    qid = qry.add_query(qry.new_search(parameters={'db' : 'cdd',
                                                   'term': 'txid10239[Organism:exp] NOT (predicted OR putative OR hypothetical)'}))
    qid = qry.add_query(qry.new_fetch(dependency=qid,
                                      parameters={'rettype':'docsum',
                                                  'retmode':'json'},
                                      analyzer=self.DocsumAnalyzer()))
    dsa = nc.run_query(qry)
    return dsa.accessions
