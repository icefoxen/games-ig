# colony.py
# Contains all the data of a colonized world.

# Well whaddya know, Python can have packages with mutal dependancies.
# colony imports star imports colony.  Yay for dynamic typing!
# Suck it, OCaml!
import star
from fleet import *

class ProdItem:
   prodAmount = 0
   percent = 0.0
   locked = False

   def __repr__( s ):
      return "%d resources, %f/1.0 production, locked = %d" % \
             (s.prodAmount, s.percent, s.locked)

SHIP = 0
DEFENCE = 1
FACTORY = 2
COLONY = 3


class BuildQueue:
   items = []

   def __init__( s ):
      s.items = [ProdItem(), ProdItem(), ProdItem(), ProdItem()]
      for x in s.items:
         x.percent = 0.25

   def __getitem__( s, item ):
      return s.items[item]

   def __repr__( s ):
      string =  "Ship: " + str( s[SHIP] ) + "\n"
      string += "Defence: " + str( s[DEFENCE] ) + "\n"
      string += "Factory: " + str( s[FACTORY] ) + "\n"
      string += "Colony: " + str( s[COLONY] )
      return string

   def incProd( s, item ):
      if s.items[item].percent == 1.0:
         return
      # Sloppy, but simple
      for x in s.items:
         if (x.percent > 0.0) and (not x.locked):
            x.percent -= 0.01
            s.items[item].percent += 0.01

      if s.items[item].percent > 1.0:
         s.items[item].percent = 1.0
         print "Hax!"

   def decProd( s, item ):
      if s.items[item].percent == 0.0:
         return
      for x in s.items:
         if (x.percent < 1.0) and (not x.locked):
            x.percent += 0.01
            s.items[item].percent -= 0.01

      if s.items[item].percent < 0.0:
         s.items[item].percent = 0.0
         print "More hax!"
         

   def setProd( s, item, amount ):
      if (amount < 0) or (amount > 1.0):
         print "You bastard!"
         return
      while amount > s.items[item].percent:
         s.incProd( item )
      while amount < s.items[item].percent:
         s.decProd( item )


   def toggleLock( s, item ):
      s.items[item].locked = not s.items[item].locked

   def doProduction( s, totalAmount ):
      totalPercent = 0.0
      for x in s.items:
         totalPercent += x.percent
         if totalPercent >= 1.0:
            x.percent -= totalPercent - 1.0
         x.prodAmount += totalAmount * x.percent
         


class Colony:
   empire = ()
   pop = 0
   colonies = 0
   factories = 10
   defences = 0
   world = ()

   grossProd = 0
   netProd = 0

   queue = ()


   fleetBuilding = ()

   def __init__( s, empire, pop, world ):
      s.empire = empire
      s.pop = pop
      s.world = world
      world.colony = s
      s.queue = BuildQueue()
      print "Colony created:" + str( world )

   def __repr__( s ):
      string = "Owner: %s Pop: %d Colonies: %d Factories: %d Defences: %d\n" \
               % (s.empire.name, s.pop, s.colonies, s.factories, \
                  s.defences)
      string += "GrossProd: %d NetProd: %d\n" % (s.grossProd, s.netProd)
      string += str( s.queue )
      return string

   def getProd( s, item ):
      return s.queue[item].percent

   def setProd( s, item, amount ):
      s.queue.setProd( item, amount )

   def toggleLock( s, item ):
      s.queue.toggleLock( item )

   def calcGrossProd( s ):
      # You can have more factories than you can currently operate,
      # but not more than your current max pop can operate.
      operableFactories = s.pop * s.empire.factoryPerPop
      numFactories = min( s.factories, operableFactories )
      s.grossProd = (s.empire.prodPerFact * numFactories) + \
                       (s.empire.prodPerPop * s.pop)

   def calcNetProd( s ):
      s.netProd = s.grossProd * (1 - s.empire.taxRate)

   def taxesCollected( s ):
      return s.grossProd - s.netProd

   def getMaxPop( s ):
      return (s.world.maxPop + s.empire.maxPopBonus) + \
                 (s.colonies * s.empire.popPerColony)

   def calcPopGrowth( s ):
      s.pop = s.pop + (s.pop * s.empire.race.growthRate)
      if s.pop > s.getMaxPop():
         s.pop = s.getMaxPop()

   # Okay.  First, we calc gross production.
   # Second, we calc growth and do production
   def calcTurn( s ):
      s.calcGrossProd()
      s.calcNetProd()
      s.calcPopGrowth()
      s.calcProductionQueue()
      

   def calcProductionQueue( s ):
      s.queue.doProduction( s.netProd )
      s.calcFactoryProduction()
      s.calcFleetProduction()
      s.calcDefenceProduction()
      s.calcColonyProduction()

   # Now, make other things work, and make keys/buttons to change
   # production proportions.
   # Yay!  Elegance!
   def calcFactoryProduction( s ):
      s.queue[FACTORY].prodAmount -= s.getFactoryMaint()
      if s.queue[FACTORY].prodAmount < 0:
         s.factories -= 1
         s.queue.setProd( FACTORY, s.getFactoryMaint() )
         s.queue[FACTORY].prodAmount = 0
         print "Factories not maintained!"
         return


      #factoriesProduced = s.queue[FACTORY].prodAmount / s.empire.factoryCost
      #resourcesLeft = s.queue[FACTORY].prodAmount % s.empire.factoryCost
      #s.factories += s

      # This is best 'cause we need to check for max factories.
      while (s.queue[FACTORY].prodAmount > s.empire.factoryCost) and \
            (s.factories < s.getMaxFactories()):
         s.factories += 1
         s.queue[FACTORY].prodAmount -= s.empire.factoryCost
         
      if s.factories == s.getMaxFactories():
         s.empire.addFunds( s.queue[FACTORY].prodAmount )
         s.queue[FACTORY].prodAmount = 0



   def calcFleetProduction( s ):
      if s.fleetBuilding == ():
         return

      if s.queue[SHIP].prodAmount > s.fleetBuilding.getCost( 1 ):
         numFleets = s.queue[SHIP].prodAmount / s.fleetBuilding.getCost( 1 )
         leftover = s.queue[SHIP].prodAmount % s.fleetBuilding.getCost( 1 )

         if s.world.fleetTypeInOrbit( s.fleetBuilding ):
            # Hmm, there can be more than one of a certain fleet-type...
            # No, there actually can't.  We don't have non-merging fleets yet.
            for fleet in s.world.fleets:
               if fleet.getDesign() == s.fleetBuilding:
                  fleet.scale += numFleets
                  s.queue[SHIP].prodAmount = leftover
                  return
               print "This should never happen!"

         # We haven't found it, oh well...
         s.world.addOrbitingFleet( Fleet( s.empire, s.fleetBuilding,
                                          count=numFleets ) )
         s.queue[SHIP].prodAmount = leftover
         
            
                                   
            


   def calcDefenceProduction( s ):
      defencesProduced = s.queue[DEFENCE].prodAmount / s.empire.defenceCost
      resourcesLeft = s.queue[DEFENCE].prodAmount % s.empire.defenceCost
      s.defences += defencesProduced
      s.queue[DEFENCE].prodAmount = resourcesLeft

   def calcColonyProduction( s ):
      s.queue[COLONY].prodAmount -= s.getColonyMaint()
      if s.queue[COLONY].prodAmount < 0:
         s.colonies -= 1
         s.queue.setProd( COLONY, s.getColonyMaint() )
         s.queue[COLONY].prodAmount = 0
         print "Colonies not maintained!"
         return


      while (s.queue[COLONY].prodAmount >= s.empire.colonyCost) and \
            (s.colonies < s.getMaxColonies()):
         s.colonies += 1
         s.queue[COLONY].prodAmount -= s.empire.colonyCost
         
      if s.colonies == s.getMaxColonies():
         s.empire.addFunds( s.queue[COLONY].prodAmount )
         s.queue[COLONY].prodAmount = 0

   
   def getFactoryMaint( s ):
      return s.factories * s.empire.factoryMaint


   # Returns the max number of factories the current pop can operate
   def getMaxFactories( s ):
      return s.pop * s.empire.factoryPerPop


   def getColonyMaint( s ):
      return s.colonies * s.empire.colonyMaint

   def getMaxColonies( s ):
      return s.world.maxColonies + s.empire.maxColoniesBonus


   def setFleetBuilding( s, fleetdesign ):
      s.fleetBuilding = fleetdesign

   # Defence maintainance doesn't change with tech...
   # It's 1% of the price of the defence.  Well, so if you get tech
   # that makes defences cheaper...
   def getDefenceMaint( s ):
      return s.defences * s.empire.defenceCost * 0.01
