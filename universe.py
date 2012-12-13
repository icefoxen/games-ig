# universe.py
# A universe.
# This keeps track of EVERYTHING, does turn generation, etc.
# It does NOT draw itself!


import ship
import fleet
import empire
import empireset

import pygame
from pygame.locals import *

class Universe:
   starmap = ()
   empires = ()
   turnnum = 0

   def __init__( self, starmap, empires ):
       self.empires = empires
       self.starmap = starmap
       for name in empires:
           emp = empires[name]
           # Put out starting ships
           f = fleet.Fleet( 'Alpha', ship.defaultCarrier, emp )
           f.addShip( ship.defaultShip )
           f.moveTo( 10, 100 )
           f.setDest( emp.getStars()[0] )
           emp.addFleet( f )
           starmap.add( f )

   def calcTurn( self ):
       lastturn = pygame.time.get_ticks()
       print "Generating turn..."
       self.turnnum += 1

       for x in self.empires:
           self.empires[x].calcTurn()

       thisturn = pygame.time.get_ticks()
       print "Calculated turn %d, took %d ms" % \
             (self.turnnum, (thisturn - lastturn))
