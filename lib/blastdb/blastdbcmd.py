#  blastdbcmd.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
# blast return codes
# https://www.ncbi.nlm.nih.gov/books/NBK279677/
#
#
#  Version: 0.0

import os
import sys
import re
import subprocess

class Blastdbcmd:

  def __init__(self):
    self.cmd = 'blastdbcmd'

  def exists(self, path):
    cmd = [self.cmd, '-db', path, '-info']

    bdbc = subprocess.run(cmd, stdout=subprocess.PIPE, bufsize=1)
    if bdbc.returncode > 0:
      return False
    return True
