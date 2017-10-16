#  blastdbcmd.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import re
import subprocess

class Blastdbcmd:

  def __init__(self):
    self.cmd = 'blastdbcommand'

  def exists(self, dbname, path=None):
    re_error = re.compile("BLAST Database error:")
    if path != None:
      db = os.join(path, db)

    bdbc = subprocess.Popen([self.cmd, '-db', db, '-info'], stdout=subprocess.PIPE)
    for i in bdbc.stdout:
      if re.match(re_error, i.decode().strip()):
        return False
    return True
