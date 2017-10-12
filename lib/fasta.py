#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  fasta.py
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys


class Sequence:

  def __init__(self, header='', seq=''):
    self.header = header
    self.sequence = seq
    self.length = len(seq)

  def shrink(self, newlen):
    self.sequence = self.seq.substr[:newlen]
    self.length = len(self.seq)

  def subseq(self, start, length, header=None):
    if header == None:
      return Sequence(self.header, self.sequence[start:start+length])
    return Sequence(header, self.sequence[start:start+length])

  def save_fasta(self, fname):
    fh = open(fname, 'w')
    fh.write('>'+self.header+'\n')
    fh.write(self.seq+'\n')
    fh.close()


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
          self.add_sequence(Sequence(header, seq))
          seq = ''
        header = i[1:].strip()
      else:
        seq += i.strip()
    self.add_sequence(Sequence(header, seq))

    if self.doFhClose == True:
      src.close()

  def write_fasta(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write('>'+i.header+'\n')
      fh.write(i.seq+'\n')
    fh.close()

  def stream_fasta(self):
    for i in self.sequences:
      print(">{0}\n{1}\n".format(i.header, i.sequence))

  def add_sequence(self, seq):
    self.sequences.append(seq)
