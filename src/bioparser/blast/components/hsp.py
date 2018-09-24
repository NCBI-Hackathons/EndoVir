#-------------------------------------------------------------------------------
#  \file hsp.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description Implementation of a BLAST HSP (High socirng pair) linking a
#               query to a hit. Aligned regions should be stored as interval
#               trees, at some point, analogous to NCBI's cpp toolkit [0]
# [0]: https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/doxyhtml/itree_8hpp_source.html#l00288
#-------------------------------------------------------------------------------

#import uuid
import hashlib

class Hsp:

  def __init__(self, blast_hsp, query, hit):
    self.bitscore =  blast_hsp.pop('bit_score', 0)
    self.num = blast_hsp.pop('num', 0)
    self.score = blast_hsp.pop('score', 0)
    self.evalue = blast_hsp.pop('evalue', 100)
    self.identify = blast_hsp.pop('identity', 0)
    self.positive = blast_hsp.pop('positive', 0)
    self.alength = blast_hsp.pop('align_len', 0)
    self.gaps = blast_hsp.pop('gaps', 0)
    self.qbeg = blast_hsp.pop('query_from', 0)
    self.qend = blast_hsp.pop('query_to', 0)
    self.hbeg = blast_hsp.pop('hit_from', 0)
    self.hend = blast_hsp.pop('hit_to', 0)
    #self.uid = str(uuid.uuid4())
    self.uid = hashlib.sha256()
    self.uid.update(query.uid.digest()+hit.uid.digest())
    self.query = query
    self.hit = hit

  def get_uid(self):
    return self.uid.hexdigest()
