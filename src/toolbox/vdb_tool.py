#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Implementation to use NCBI's NGS vdb toolkit for SRA retrieval
#-------------------------------------------------------------------------------
# Duration to fetch(map) reads using 4 threads: 1135.957700252533 s
#             fetch(map) reads using 8 threads: 904.6983740329742 s
#             fetch(map) reads using 16 threads: 588.7242548465729 s
#             fetch(map_async) reads using 12 threads: 588.5161285400391 s
#             fetch(map_async) reads using 16 threads: 354.78742814064026 s
#             fetch(map_async) reads using 16 threads: 440.67980575561523 s
#             fetch(map_async) reads using 16 threads: 400.13484954833984 sec


import os
import sys
import time
import multiprocessing.dummy
import threading

sys.path.insert(1, os.path.join(sys.path[0], '../include/ncbi/ngs/ngs-python/'))
from ngs import NGS
from ngs.ErrorMsg import ErrorMsg

from utils import fasta_formatter
from utils import endovir_utils

class EndovirVdbTool:

  class ReadFetcher:

    def __init__(self, srr, output):
      self.srr = srr
      self.output = output

    def fetch(self, groups):
      srr = NGS.openReadCollection(self.srr)
      reads = srr.getReadRange(groups[0], groups[1]+1)
      while reads.nextRead():
        self.output.write(fasta_formatter.FastaFormatter.format_string(reads.getReadId(),
                                                                   reads.getReadBases()))

  def __init__(self, overwrite=True):
    self.num_threads = 16
    self.read_location = '/tmp'
    self.suffix = '.reads'
    self.overwrite = overwrite

  def fetch_reads(self, acc, mapping_result):
    contig_file = self.get_output_filename(acc)
    if not self.overwrite and endovir_utils.isNotEmptyFile(contig_file):
      print("Found and using previously fetched reads in {}".format(contig_file), file=sys.stderr)
      return contig_file
    print("Fetching {} reads in {} groups".format(mapping_result.count,
                                                  len(mapping_result.groups)),
                                                  file=sys.stderr)
    # Quick solution, but tricky to show ongoing progess. Could use an inherited
    # thread class as worker
    start_time = time.time()
    fh_output = open(contig_file, 'w')
    rf = self.ReadFetcher(acc, fh_output)
    pool = multiprocessing.dummy.Pool(self.num_threads)
    pool.map_async(rf.fetch, mapping_result.groups)
    pool.close()
    pool.join()
    fh_output.close()
    print("Duration to fetch {0} reads using {1} threads: {2} sec".format(mapping_result.count,
                                                                          self.num_threads,
                                                                          time.time()-start_time),
                                                                          file=sys.stderr)
    return contig_file

  def get_output_filename(self, acc):
    return os.path.join(self.read_location, acc+self.suffix)
