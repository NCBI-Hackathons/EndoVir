#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Implementation to use NCBI's NGS vdb toolkit for SRA retrieval
#-------------------------------------------------------------------------------

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../include/ncbi/ngs/ngs-python/'))
from ngs import NGS
from ngs.ErrorMsg import ErrorMsg

class EndovirVdbTool:

  def __init__(self):
    pass

  def fetch_reads(self, acc, mapping_results):
    self.get_read_groups(mapping_results)
    #with NGS.openReadCollection(acc) as run:
      #with run.getReadRange(205412, 2) as ref:
        #while ref.nextRead():
          #print(ref.getReadName())
          #print(ref.getNumFragments())
          #print(ref.getReadCategory())
          #print(ref.getReadBases())
          #print(ref.getReadGroup())
          #print(ref.getReadQualities())
          #print(ref.getReadId())

  def get_read_groups(self, mapping_result):
    start_entry = reads[0]
    for i in reads:
