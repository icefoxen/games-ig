# star.py
# All systems are divided into three (or maybe four) zones, inner middle
# and outer.  They all have different stats and tendancies.  A race
# starts out only living in one of them; technology can make more
# avaliable.
#
# ...I think I'll implement this later.

import random
import math
import colony
import loader
import sprite
from spaceobj import *

RED    = 0
ORANGE = 1
YELLOW = 2 
GREEN  = 3
BLUE   = 4
WHITE  = 5

STARNAMES = loader.cfgloader.get( 'names.txt' )['stars']

class StarZone:
   maxPop = 0
   maxCities = 0
   richness = 0

   def __init__( self ):
      return
   

class Star( SpaceObj ):
   type = RED

   x = 0
   y = 0

   colony = None

   #zones = []
   maxPop = 0
   maxColonies = 0
   richness = 0

   fleets = []

   sprite = ()


   # XXX: We want some more specific randomness here; stars shouldn't be too
   # close together, and the stats should be weighted by the type of star
   # and zone.
   def __init__( self, maxx, maxy ):
      self.type = math.floor( random.randrange( 0, 6 ) )
      minspacing = 3
      self.x = int( random.uniform( 1, maxx / minspacing ) ) * minspacing
      self.y = int( random.uniform( 1, maxy / minspacing ) ) * minspacing

      #self.zones = [StarZone(), StarZone(), StarZone()]
      #for x in self.zones:
      #   x.maxCities = random.randrange( 5, 15 )
      #   x.maxPop = random.randrange( 0, 100 )
      #   x.richness = random.randrange( 0, 100 )

      self.maxColonies = random.randrange( 5, 15 )
      self.maxPop = random.randrange( 2, 25 ) * 5
      self.richness = random.randrange( 50, 150 )

      global STARNAMES
      self.name = STARNAMES[ random.randrange( 0, len( STARNAMES ) ) ]
      STARNAMES.remove( self.name )

      self.sprite = sprite.Sprite( "star.sprite" )

      
   def __repr__( self ):
      str = "%s: %d, %0.0f, %0.0f " % (self.name, self.type, self.x, self.y)
      str += "MaxPop: %d Maxcities: %d" % \
             (self.maxPop, self.maxColonies)
      if self.colony != ():
         str += "\n" + self.colony.__repr__()
      return str

   def prepareSprite( self ):
      self.sprite.setAnim( self.type )

   def getStarType( self ):
      return self.type

   # XXX: Not necessary?
   def makeColony( self, empire, initialPop ):
      self.colony = colony.Colony( empire, initialPop, self )

   def hasColony( self ):
      return self.colony != None

   def getColony( self ):
      return self.colony

   def setColony( self, c ):
      self.colony = c
      c.world = self

   # XXX: Destroy colony?  Handle removal from empire then...

   def getTotalMaxColonies( self ):
      #cities = 0
      #if self.hasColony():
      #   for x in self.zones:
      #      cities += x.maxCities + self.colony.empire.maxCitiesBonus
      #else:
      #   for x in self.zones:
      #      cities += x.maxCities
      #return cities
      if self.hasColony():
         return self.maxColonies + self.colony.empire.maxColoniesBonus
      else:
         return self.maxColonies

   #def getZone( self, x ):
   #   return self.zones[x]
   #
   #def maxCitiesInZone( self, x=[0] ):

   # Returns total maximum population, including cities.
   def getTotalMaxPop( self ):
      maxPop = self.maxPop
      if self.hasColony():
         maxPop += self.colony.empire.maxPopBonus
         maxPop += self.getTotalMaxColonies() * self.colony.empire.popPerColony
      return maxPop

   def getType( s ):
      return STARTYPE

   def hasOrbitingFleets( s ):
      return (s.fleets != [])

   def fleetIsOrbiting( s, fleet ):
      try:
         a.index( fleet )
         return True
      except ValueError:
         return False

   def addOrbitingFleet( s, fleet ):
      s.fleets.append( fleet )
      fleet.orbiting = s

   def removeOrbitingFleet( s, fleet ):
      s.fleets.remove( fleet )
      fleet.orbiting = None

   def fleetTypeInOrbit( s, typ ):
      for fleet in s.fleets:
         if fleet.getDesign() == typ:
            return True
      return False
