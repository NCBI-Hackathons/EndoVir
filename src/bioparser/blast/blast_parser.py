#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \file blast_parser.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys
import argparse

import blast_json

class BlastWheel:

  def __init__(self, hub):
    self.hub = hub
    self.spokes = {}

  def add_spoke(self, rim, hsp):
    if rim.get_uid() not in self.spokes:
      self.spokes[rim.get_uid()] = []
    self.spokes[rim.get_uid()].append(hsp.get_uid())

  def show(self):
    print(self.hub)
    for i in self.spokes:
      print(i, self.spokes[i])

class BlastPlotter:

  def __init__(self):
    pass

  def collect_wheels(self, blastparser, hub='q'): # q=query, h=hit
    if hub == 'q':
      self.collect_query_hubs(blastparser.hspmap)

  def collect_query_hubs(self, hsps):
    query_wheelmap = {}
    for i in hsps:
      if hsps[i].query.get_uid() not in query_wheelmap:
        query_wheelmap[hsps[i].query.get_uid()] = BlastWheel(hsps[i].query.get_uid())
      query_wheelmap[hsps[i].query.get_uid()].add_spoke(hsps[i].hit, hsps[i])
    for i in query_wheelmap:
      query_wheelmap[i].show()

def main():
  ap = argparse.ArgumentParser(description='Blast JSON result test parser')
  b = blast_json.BlastParser()
  b.parse()

  bp = BlastPlotter()
  bp.collect_wheels(b)
  return 0

if __name__ == '__main__':
  main()
