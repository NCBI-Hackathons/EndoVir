#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------


import io
import os
import sys


class BlastResult:

  def __init__(self, queries=None, hits=None, hsps=None):
    self.queries = queries
    self.hits = hits
    self.hsps = hsps

  def get_queries(self):
    return [self.queries[x] for x in self.queries]
