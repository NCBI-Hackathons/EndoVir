#-------------------------------------------------------------------------------
#  \file hit.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description Implementation of a BLAST hit.
#-------------------------------------------------------------------------------

import hashlib
#from ..interval import itree
#from ..interval import interval

class BlastHit:

  def __init__(self, hid=None, accession=None, title=None, length=0, hitnum=0):
    self.id = hid
    self.accession = accession
    self.title = title
    self.length = length
    self.num = hitnum
    self.uid = hashlib.sha256(title.encode())

  def get_uid(self):
    return self.uid.hexdigest()

  def dump(self):
    print("Hid: {0}\nId: {1}\nTitle: {2}\Accession: {3}\nLength: {4}\nNumber{5}".format(self.hid,
                                                                           self.id,
                                                                           self.title,
                                                                           self.accession,
                                                                           self.length,
                                                                           self.num))
