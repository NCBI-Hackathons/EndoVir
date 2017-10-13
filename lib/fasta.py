#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  fasta.py
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import io
import sys
from . import sequence

class FastaSequence(sequence.Sequence):

  def __init__(self, name='', seq=''):
    super().__init__()
    self.header = name

  def get_sequence(self):
    return ">{0}\n{1}".format(self.header, self.name)

  def subseq(self, start, length, header=None):
    if header == None:
      return FastaSequence(self.header, self.sequence[start:start+length])
    return FastaSequence(header, self.sequence[start:start+length])


class Fasta:

  def __init__(self):
    self.sequences = []
    self.doFhClose = False

  def read(self, fil=None):
    src = sys.stdin

    if fil != None:
      src = open(fil, 'r')
      self.doFhClose = True
    seq = ''
    header = ''
    for i in src:
      if i[0] == '>':
        if len(seq) > 0:
          self.add_sequence(FastaSequence(header, seq))
          seq = ''
        header = i[1:].strip()
      else:
        seq += i.strip()
    self.add_sequence(FastaSequence(header, seq))

    if self.doFhClose == True:
      src.close()

  def write_fasta(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write(i.get_sequence())
    fh.close()
    return fname

  def stream_fasta(self):
    stream = io.StringIO()
    for i in self.sequences:
      print(i.get_sequence(), file=stream)
    yield stream.getvalue()

  def add_sequence(self, seq):
    self.sequences.append(seq)
