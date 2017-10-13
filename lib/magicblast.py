# -*- coding: utf-8 -*-
#
#  magicblast.py
#
#  Copyright 2017 USYD
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys
import subprocess

class Samparser:

  class Header:

    def __init__(self):
      self.vn = None
      self.so = 'unknown'
      self.go = 'none'

    def parse(self, cols):
      for i in cols[1:]:
        tag = i.split(':')
        if tag[0] == 'VN':
            self.vn = tag[1]
        if tag[0] == 'GO':
          self.go = tag[1]

  class RefSeqDir:

    def __init__(self):
      self.sn = None
      self.ln = None

    def parse(self, cols):
      for i in cols[1:]:
        tag = i.split(':')
        if tag[0] == 'SN':
            self.sn = tag[1]
        if tag[0] == 'ln':
          self.ln = tag[1]

  class Programm:

    def __init__(self):
      self.id = None
      self.pn = None
      self.cl = None

    def parse(self, cols):
      for i in cols[1:]:
        tag = i.split(':')
        if tag[0] == 'ID':
          self.id = tag[1]
        if tag[0] == 'PN':
          self.pn = tag[1]
        if tag[0] == 'CL':
          self.cl = tag[1]

  class Alignment:

    def __init__(self, qname, pos, seq):
      self.qname = qname
      self.seq = seq
      self.pos = int(pos)
      self.length = len(seq)
      self.sra_rowid = self.qname.split('.')[-2]

  def __init__(self):
    self.header = Samparser.Header()
    self.refseqdir = Samparser.RefSeqDir()
    self.program = Samparser.Programm()
    self.alignments = []

  def parse_header(self, cols):
    if cols[0] == '@HD':
      self.header.parse(cols)
    elif cols[0] == '@SQ':
      self.refseqdir.parse(cols)
    elif cols[0] == '@PG':
      self.program.parse(cols)
    else:
      return

  def parse(self, sam):
    for i in sam:
      print(i.decode().strip())
      cols = i.decode().strip().split('\t')
      if cols[0][0] == '@':
        self.parse_header(cols)
      else:
        self.alignments.append(self.Alignment(cols[0], cols[3], cols[9]))

class Magicblast:

  def __init__(self):
    self.cmd = 'magicblast'
    self.isPaired = False
    self.num_threads = 2
    self.outfmt = 'sam'
    self.out = 'magicblast_out'
    self.word_size = 20
    self.perc_identity = 60

  def run(self, db, sra, parser=Samparser()):
    magicblast = subprocess.Popen([self.cmd, '-db', db, '-sra', sra,
                                                 '-num_threads', str(self.num_threads),
                                                 '-outfmt', self.outfmt],
                                  stdout=subprocess.PIPE, bufsize=1)
    parser.parse(magicblast.stdout)
    return parser.alignments
