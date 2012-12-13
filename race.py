# race.py
# Holds all the race attributes.

class Race:
   name = ""

   # Habitability
   idealGrav = 0
   idealRad = 0
   gravRange = 0
   radRange = 0

   # Intrinsic bonuses
   prodPerPop = 0
   prodPerFact = 0

   colonyCost = 0
   factoryCost = 0
   factoryPerPop = 0

   maxColoniesBonus = 0
   maxPopBonus = 0

   defencesPerPop = 0
   defencesPerColony = 0

   diplomaticBonus = 0
   maintainanceRate = 0
   researchRate = 0
   growthRate = 0

   # Insert other bonuses here... scanner range, ECM/cloak bonus,
   # battle accuracy/evasion, base speed, trade come to mind.
   # I just want the fundamental framework for now.

   def __init__( self ):
      pass


# XXX: Need a better way of creating races.
# Config file?  Maybe...
baserace = Race()
baserace.name = "BaseRace"
baserace.idealGrav = 50
baserace.idealRad = 50
baserace.gravRange = 15
baserace.radRange = 15
baserace.prodPerPop = 1
baserace.prodPerFact = 5
baserace.colonyCost = 300
baserace.factoryCost = 25
baserace.factoryPerPop = 2
baserace.maxColoniesBonus = 1
baserace.maxPopBonus = 10
baserace.defencesPerPop = 1
baserace.defencesPerColony = 2
baserace.diplomaticBonus = -15
baserace.maintainanceRate = 0.99
baserace.researchRate = 1.1
baserace.growthRate = 0.5
