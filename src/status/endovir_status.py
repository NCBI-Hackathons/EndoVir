#  -------------------------------------------------------------------------------
#  \file endovir_status.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.1.0
#  \description
#  -------------------------------------------------------------------------------

import io
import os
import sys
import enum

class EndovirStatusManager:

  @staticmethod
  def set_status_codes(status_codes, status_name='EndovirStatusCodes'):
    status_codes.insert(0, 'OK')
    return enum.Flag(status_name, status_codes)

  def __init__(self, status_codes):
    self.status = 0
    self.triggers = {}
    self.status_codes = status_codes

  def set_status(self, status_name, trigger=None):
    self.status |= self.status_codes[status_name].value
    self.triggers[status_name] = trigger

  def get_status(self, status_name='OK'):
    return (self.status & self.status_codes[status_name].value) == self.status_codes[status_name].value

  def list_triggers(self, triggers=None):
    if triggers != None:
      for i in triggers:
        print(i, self.triggers[i])
    else:
      for i in self.triggers:
        print(i, self.triggers[i])
