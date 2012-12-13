# ship.py
# Ships.  Well, the skeleton of a ship, at the moment.


# This is the blueprint of a ship.
# ...hm...  I think we can just use these.
class ShipDesign:
    battleSpeed = 0
    cost = 0
    name = "Default name"

    def __init__( s, name, bs, cost ):
        s.name = name
        s.battleSpeed = bs
        s.cost = cost

    def getSpeed( s ):
        return s.battleSpeed

    def getCost( s ):
        return s.cost

    def getName( s ):
        return s.name


class CarrierDesign:
    warpSpeed = 0
    cost = 0

    def __init__( s, ws, cost ):
        s.warpSpeed = ws
        s.cost = cost

    def getCost( s ):
        return s.cost

    def getSpeed( s ):
        return s.warpSpeed

defaultCarrier = CarrierDesign( 100, 10000 )
defaultShip = ShipDesign( "Rampaging Ramrod", 100, 10 )
