# empireset.py
# Holds a collection of empires, and lets one refer to them
# by name or index.
# Also compiles statistics and such, and might also remember
# diplomatic relations.
#
# XXX: How do we handle an empire dying??

import empire

class EmpireSet:
   empires = {}

   def __init__( self ):
      self.empires = {}

   # Man, I love python sometimes.
   def __iter__( self ):
      return self.empires.__iter__()

   def __getitem__( self, name ):
      return self.empires[name]

   def add( self, e ):
      self.empires[e.name] = e

   def getEmpireByName( self, name ):
      self.empires[name]

   def numEmpires( self ):
      return len( self.empires )
