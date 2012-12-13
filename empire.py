# empire.py
# The empire structure, a lot of gameplay systems,
# and so on.
# All the stats are absolute; the end result of race + tech.

import race
import colony


class Empire:
   name = ""
   race = ()
   color = ()

   # Aaaaall kinda planetary stats and modifiers.
   prodPerPop = 0
   
   colonyCost = 1000
   colonyMaint = 0
   popPerColony = 0
   
   factoryCost = 0
   factoryMaint = 0
   factoryPerPop = 0
   prodPerFact = 0

   maxColoniesBonus = 0
   maxPopBonus = 0

   defencesPerPop = 0
   defencesPerColony = 0
   defenceCost = 100

   # These are the actual admin values
   taxCosts = 0
   taxRate = 0.0
   scienceRate = 0.0
   scienceBonus = 0

   empireTreasury = 0
   empireTreasuryRate = 0.0

   fleetMaintainanceBonus = 0
   
   # All the planets you own
   planets = []

   # Ship stuff
   fleets = []
   fleetMaintainance = 0

   shipDesigns = []
   fleetDesigns = []


   # Moneys!
   treasury = 0

   techTree = ()

   def __init__( self, name, race, homeworld ):
      self.name = name
      self.race = race
      self.addNewColony( homeworld, 50 )
      self.updateValues()

   # This should be called after every tech is discovered, in case
   # some bonus changes.
   def updateValues( self ):
      # Right now, we have no techtree, so we add no tech bonus.
      self.prodPerPop = self.race.prodPerPop
      self.prodPerFact = self.race.prodPerFact
   
      self.colonyCost = self.race.colonyCost
      self.factoryCost = self.race.factoryCost
      self.factoryPerPop = self.race.factoryPerPop
      self.popPerColony = 20

      self.maxColoniesBonus = self.race.maxColoniesBonus
      self.maxPopBonus = self.race.maxPopBonus

      self.defencesPerPop = self.race.defencesPerPop
      self.defencesPerColony = self.race.defencesPerColony
      self.scienceBonus = self.race.researchRate
      self.fleetMaintainanceBonus = self.race.maintainanceRate


   def hasStar( self, worldname ):
      for x in self.planets:
         if x.name == worldname:
            return True
      return False
   
   # This is the canonical way to create a new colony.
   # There are other ways, but they should not be used.
   def addNewColony( self, world, pop ):
      if not self.hasStar( world.name ):
         self.planets.append( world )
         colony.Colony( self, pop, world )
      else:
         print "Warning: Empire.addNewColony(): tried to add", \
               world.name, "twice"

   # XXX: Make this work, make all fleet creation (ie colony build) use it.
   def addFleet( self, fleet ):
      self.fleets.append( fleet )

   def addFunds( self, amount ):
      self.treasury += amount

   # XXX: What if we run out of money?
   def getFunds( self, amount ):
      self.treasury -= amount
      if self.treasury < 0:
         self.treasury = 0
         print "Help!  We don't have enough money!"


   # Gross empire production
   # Total of all production, XXX: plus trade...
   def GEP( self ):
      accm = 0
      for x in self.planets:
         accm += x.colony.grossProd
      return accm

   # XXX: Make these work, maybe.
   def getStar( self, x, y ):
      return
   def getStarByName( self, name ):
      return
   def ownsStar( self, x, y ):
      return
   def isOwner( self, star ):
      return
   def getStars( self ):
      return self.planets

   # Gross empire costs --maintainance, research, treasury, 
   def GEC( self, gep ):
      fleetcosts = 0
      for x in self.fleets:
         fleetcosts += x.getMaintainance()
      researchcosts = self.scienceRate * gep
      treasurycosts = self.empireTreasuryRate * gep
      return fleetcosts + researchcosts + treasurycosts
   
   # Okay, we have to put everything together...
   # First, we figure the gross production of all planets, 
   # Next, we figure the GEC.  This is the fleet maintainance cost,
   # research cost, treasury rate, and I think that's it.  Add it all up
   # and divide by GEP, that gives us the tax rate.
   # We have to handle overrun if it exists by, ie, disbanding fleets or
   # pulling money from the treasury
   # Third, we do research changes
   # Fourth, we do each planet's production queue, do planetary growth,
   # and calculate new planetary production values.
   # Fifth, we re-sum the imperial treasury and such.
   # Sixth, we move ships and handle battles and such.
   def calcTurn( self ):
      # Step one
      gep = self.GEP()
      # Step two
      gec = self.GEC( gep )
      if gec > gep:
         print "Help!  Boss, we dun have enough dough!"
         gec = gep - 1
      self.taxRate = gec / max( gep, 1 )
      self.taxCosts = gec
      # Step three happens here

      # Step four
      for x in self.planets:
         x.colony.calcTurn()

      # Step five
      dirtyGreedyPoliticianProfit = gep * self.empireTreasuryRate
      self.empireTreasury += dirtyGreedyPoliticianProfit

      # Step six happens here
      for x in self.fleets:
         x.warpMove()


   # Hmm.  One, the designs should probably be a dictionary, not a list.
   # Two, adding a ship design should automatically add a fleet design
   # made purely of that ship.  And that fleet design should not be
   # deletable by the user, and should be deleted when the ship design
   # is scrapped.
   def addShipDesign( self, design ):
      self.shipDesigns.append( design )

   def delShipDesign( self, design ):
      return


   def addFleetDesign( self, design ):
      self.fleetDesigns.append( design )


   def delFleetDesign( self, design ):
      return

