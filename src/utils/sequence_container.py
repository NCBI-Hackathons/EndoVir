#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import io
import os
import sys

from . import endovir_utils

class SequenceContainer:

  def __init__(self, path=None):
    self.path = path
    self.sequences = {}

  def set_path(self, path):
    self.path = path
    return path

  def load_sequences(self, parser, warn=True):
    if not endovir_utils.isNotEmptyFile(self.path):
      sys.exit("Error: non-existent or empty: {0}".format(self.path))
    for i in parser.parse(self.path):
      self.add_sequence(i, warn)

  def get_sequences(self):
    return [self.sequences[x] for x in self.sequences]

  def add_sequence(self, sequence, warn=True):
    if sequence.name in self.sequences and warn:
      print("Warning: name already in index {}".format(sequence.name), file=sys.stderr)
    self.sequences[sequence.name] = sequence

  def rename_sequence(self, sequence, new_name):
    self.sequences[new_name] = self.sequences.pop(sequence.name)
    self.sequences[new_name].name = new_name

  def contains(self, sequence_name):
    return sequence_name in self.sequences

  def get_sequence(self, name):
    return self.sequences[name]

  def remove_sequence(self, sequence_name):
    return self.sequences.pop(sequence_name, None)

  def write(self, formatter):
    if self.path != None:
      fh = open(self.path)
      for i in self.sequences:
        fh.write(formatter.format(self.sequences[i]))
      fh.close()
