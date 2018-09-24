#-------------------------------------------------------------------------------
#  \file blast_query.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description Implementation of a BLAST query
#-------------------------------------------------------------------------------

import hashlib
#from ..interval import itree
#from ..interval import interval

class BlastQuery:

  def __init__(self, qid=None, title=None, length=0):
    self.id = qid
    self.title = title
    self.length = length
    self.uid = hashlib.sha256(title.encode())

  def get_uid(self):
    return self.uid.hexdigest()

  def dump(self):
    print("Qid: {0}\nId: {1}\nTitle: {2}\nLength: {3}".format(self.qid,
                                                              self.id,
                                                              self.title,
                                                              self.length))
