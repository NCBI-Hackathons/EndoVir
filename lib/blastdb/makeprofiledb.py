#  makeprofiledb.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from . import database

class Makeprofiledb(database.BlastDatabase):

  def __init__(self, dbdir, name, typ):
    super().__init__(dbdir=dbdir, name=name, typ=typ, cmd='makeprofiledb')
