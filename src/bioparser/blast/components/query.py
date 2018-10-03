#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Implementation of a BLAST query
#-------------------------------------------------------------------------------

import hashlib

class BlastQuery:

  def __init__(self, qid=None, title=None, length=0):
    self.id = qid
    self.title = title
    self.length = length
    self.uid = hashlib.sha256(qid.encode())

  def get_uid(self):
    return self.uid.hexdigest()

  def dump(self):
    print("Id: {0}\nTitle: {1}\nLength: {2}".format(self.id, self.title, self.length))
