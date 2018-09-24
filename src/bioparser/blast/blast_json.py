#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description A blast parsre for results in JSON
#-------------------------------------------------------------------------------

import os
import sys
import json

from . import components
#from .components import query
#from .components import hit
#from .components import hsp

class BlastParser:

  def __init__(self):
    self.querymap = {}
    self.query_ivals = {}
    self.hitmap = {}
    self.hspmap = {}

  def parse(self, src):
    blast_result = json.load(src)
    self.parse_results(blast_result['BlastOutput2']['report']['results'])


  def parse_results(self, results):
    bl_query = self.add_query(components.query.BlastQuery(results['search']['query_id'],
                                               results['search']['query_title'],
                                               results['search']['query_len']))


    self.add_hits(results['search']['hits'], bl_query)

  def add_hits(self, hits, bl_query):
    for i in hits:
      bl_hit = self.add_hit(components.hit.BlastHit(i['description'][0]['id'],
                                         i['description'][0]['accession'],
                                         i['description'][0]['title'],
                                         i['len'],
                                         i['num']))
      for j in i['hsps']:
        print('qry: ',bl_query.length)
        print('hit: ',bl_hit.length)
        h = self.add_hsp(components.hsp.Hsp(j, bl_query, bl_hit))
        print("----------------")

  def add_hsp(self, hsp):
    if hsp.get_uid() not in self.hspmap:
      self.hspmap[hsp.get_uid()] = hsp
    return hsp

  def add_query(self, query):
    if query.get_uid() not in self.querymap:
      self.querymap[query.get_uid()] = query
    return self.querymap[query.get_uid()]

  def add_hit(self, hit):
    if hit.get_uid() not in self.hitmap:
      self.hitmap[hit.get_uid()] = hit
    return self.hitmap[hit.get_uid()]

  def show_queries(self):
    for i in self.querymap:
      self.querymap[i].dump()

  def show_hits(self):
    for i in self.hitmap:
      self.hitmap[i].dump()
