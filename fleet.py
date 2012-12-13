# fleet.py
# All ships are in fleets.
# Fleets can be merged, split, and in general messed with.
#
# Hrm.  There may be times when you want ships to move together but
# not fight together... hmph.  Too bad.
#
# Hmmmm...  Maybe one unified index of each kind of spaceobj, and
# everything indices into that?  Makes keeping track of 'em easier, but...
# Nah.  The starmap keeps track of 'em all.

import ship
import sprite
from spaceobj import *
from math import *

import wx


LASTFLEET = 0

class Fleet( SpaceObj ):
    name = ""
    ships = {}
    carrier = ()

    destStar = None
    orbiting = None

    sprite = ()
    owner = ()

    x = 0
    y = 0

    def __init__( s, name, carrier, owner ):
        s.name = name
        s.owner = owner
        s.carrier = carrier

        s.sprite = sprite.Sprite( "fleet.sprite" )

    def __repr__( s ):
        return "Fleet %s" % s.name

    def getOwner( s ):
        return s.owner

    def setOwner( s, o ):
        s.owner = o

    def getWarpSpeed( self ):
        return self.carrier.getSpeed()

    def getBattleSpeed( self ):
        maxspeed = 99999999
        for x in self.ships:
            maxspeed = min( maxspeed, x.getSpeed() )
        return maxspeed

    def getShips( self ):
        return self.ships

    def addShips( self, ship, n ):
        if ship in self.ships:
            self.ships[ship] += n
        else:
            self.ships[ship] = n

    def removeShips( self, ship, n ):
        if ship in self.ships:
            self.ships[ship] -= n
            if self.ships[ship] < 1:
                self.ships.pop( ship )

    def addShip( self, ship ):
        self.addShips( ship, 1 )

    def removeShip( self, ship ):
        self.removeShip( ship, 1 )

    def getCount( self ):
        total = 0
        for x in self.ships:
            total += self.ships[x]
        return total

    def getName( s ):
        return s.name

    def setName( s, name ):
        s.name = name

    def getCost( s ):
        cost = 0
        for x in s.ships:
            cost += (x.getCost() * s.ships[x])
        return 1

    def getMaintainance( s ):
        return s.getCost() * 0.01
    
    def getLocation( s ):
        if s.orbiting != None:
            return (s.x + 7, s.y - 7)
        else:
            return (s.x, s.y)

    def getDest( s ):
        return s.dest

    def drawPath( s, surface, screenx, screeny, screenw, screenh ):
        # Yeah yeah, code duplication is evil.
        minx = screenx 
        maxx = screenx + screenw
        miny = screeny
        maxy = screeny + screenh
        locx, locy = s.getLocation()
        objx = locx - screenx - (s.sprite.getW() / 2)
        objy = locy - screeny - (s.sprite.getH() / 2)

        if s.destStar != None:
            destx, desty = s.getDest().getLocation()
            destx = destx - screenx
            desty = desty - screeny

            # Random fudge factor to center sprites
            objx += (s.sprite.getW() / 2)
            objy += (s.sprite.getH() / 2)

            surface.SetPen( wx.Pen( wx.Colour( 0, 0, 255), 1, wx.SOLID ) )
            surface.DrawLine( objx, objy, destx, desty )



    def prepareSprite( self ):
        if self.orbiting:
            self.sprite.setAnim( 1 )
        else:
            self.sprite.setAnim( 0 )

    def setDest( s, star ):
        s.destStar = star

    def getDest( s ):
        return s.destStar

    def getETA( s ):
        if s.destStar == None:
            return 0
        return ceil( s.getDistToTarget() / s.getWarpSpeed() )

    def getDistToTarget( s ):
        if s.destStar == None:
            return 0
        destx = s.destStar.x
        desty = s.destStar.y
        deltaX = destx - s.x
        deltaY = desty - s.y
        distToTarget = sqrt( (deltaX ** 2) + (deltaY ** 2) )
        return distToTarget

    
    # I'm too lazy to do proper sin/cos stuff, so I'm being... creative.
    def warpMove( s ):
        if s.destStar == None:
            return
        destx = s.destStar.x
        desty = s.destStar.y
        deltaX = destx - s.x
        deltaY = desty - s.y
        distToTarget = sqrt( (deltaX ** 2) + (deltaY ** 2) )
        if distToTarget == 0:
            return
        portionMovable = (s.getWarpSpeed()) / distToTarget
        if portionMovable >= 1:
            s.moveTo( destx, desty )
            s.destStar.addOrbitingFleet( s )
            s.destStar = None
        else:
            moveX = deltaX * portionMovable
            moveY = deltaY * portionMovable
            s.x += moveX
            s.y += moveY


    # This is the spaceobj type!
    def getType( s ):
        return FLEETTYPE

##     def draw( s, surface, screenx, screeny, screenw, screenh ):
##         minx = screenx 
##         maxx = screenx + screenw
##         miny = screeny
##         maxy = screeny + screenh
##         # So if you override getLocation() (like fleet.py does), you can
##         # make something act like it's somewhere it isn't, without
##         # overriding this function.
##         locx, locy = s.getLocation()
##         objx = locx - screenx - (s.sprite.frameW / 2)
##         objy = locy - screeny - (s.sprite.frameH / 2)
##         if (locx >= minx and locx < maxx) and (locy >= miny and locy < maxy):
##             s.prepareSprite()
##             s.sprite.draw( surface, objx, objy )




## CORERING = 0
## DEFENCERING = 1
## PICKETRING = 2

# A FleetDesign gives the desired proportions and positions of
# various ships in a fleet.
# Hmmm...
# Blah, my mind no work at the moment.  I'm really not entirely sure
# how to make this work...
# How it SHOULD work is this:
# Each fleet has a "design", which tells you how many ships of each class
# it should have and where.  Fleets can be scaled up and down, so you can
# have fleets of the same design with 5 ships, or 500.
#
# The last bit is the tricky bit.  I may make it so you can't have extra
# ships in a fleet or such, so I can just use a direct scaling multiplier.
# And then when two fleets of the same type meet, they can merge transparently.
## class FleetDesign:
##     rings = []
##     name = ""

##     warpSpeed = 0
##     battleSpeed = 0

##     def __init__( s, name ):
##         s.rings = [{}, {}, {}]
##         s.name = name

##     def addShips( s, ring, ship, count ):
##         if ship in s.rings:
##             s.rings[ring][ship] += count
##         else:
##             s.rings[ring][ship] = count
##         s.updateSpeeds()

##     def removeShips( s, ring, ship, count ):
##         if ship in s.rings:
##             s.rings[ring][ship] -= count
##             if s.rings[ring][ship] < 0:
##                 s.rings.pop( ship )
##         s.updateSpeeds()

##     def getCost( s, desiredSize ):
##         cost = 0
##         for ring in s.rings:
##             for ship in ring:
##                 cost += ship.cost * ring[ship]
##         return cost

##     def updateSpeeds( s ):
##         # This bit is wrong, but I dunno how to make it right...
##         s.warpSpeed = 999999
##         s.battleSpeed = 999999
##         for ring in s.rings:
##             for ship in ring:
##                 s.warpSpeed = min( ship.warpSpeed, s.warpSpeed )
##                 s.battleSpeed = min( ship.battleSpeed, s.battleSpeed )

##     def getName( self ):
##         return self.name


## class Fleet( SpaceObj ):
##     scale = 1
##     design = ()

##     owner = ()
##     name = ""


##     # When you have extra ships, remember to account for different speed!
##     #extraShips = []

##     destStar = None
##     orbiting = None

##     # Class variable!
##     sprite = sprite.Sprite( "fleet.sprite" )

##     def __init__( s, owner, design, name="", count=1 ):
##         s.owner = owner
##         s.design = design
##         s.scale = count

##         #s.extraShips = [{},{},{}]

##         global LASTFLEET
##         s.fleetnum = LASTFLEET
##         if name == "":
##             s.name = ("Fleet %d" % s.fleetnum)
##         else:
##             s.name = name
##         LASTFLEET += 1

##     def prepareSprite( self ):
##         if self.orbiting:
##             self.sprite.setAnim( 1 )
##         else:
##             self.sprite.setAnim( 0 )

##     def setDest( s, star ):
##         s.destStar = star

##     def getDest( s ):
##         return s.destStar
    
##     def scale( s, number ):
##         s.scale += number

##     # I'm too lazy to do proper sin/cos stuff, so I'm being... creative.
##     def warpMove( s ):
##         if s.destStar == None:
##             return
##         destx = s.destStar.x
##         desty = s.destStar.y
##         deltaX = destx - s.x
##         deltaY = desty - s.y
##         distToTarget = sqrt( (deltaX ** 2) + (deltaY ** 2) )
##         if distToTarget == 0:
##             return
##         portionMovable = (s.design.warpSpeed * 1.0) / distToTarget
##         if portionMovable >= 1:
##             s.moveTo( destx, desty )
##             s.destStar.addOrbitingFleet( s )
##             s.destStar = None
##         else:
##             moveX = deltaX * portionMovable
##             moveY = deltaY * portionMovable
##             s.x += moveX
##             s.y += moveY


##     # This is the spaceobj type!
##     def getType( s ):
##         return FLEETTYPE

##     def getDesign( s ):
##         return s.design


##     def getLocation( s ):
##         if s.orbiting != None:
##             return (s.x + 7, s.y - 7)
##         else:
##             return (s.x, s.y)

##     def drawPath( s, surface, screenx, screeny, screenw, screenh ):
##         # Yeah yeah, code duplication is evil.
##         minx = screenx 
##         maxx = screenx + screenw
##         miny = screeny
##         maxy = screeny + screenh
##         locx, locy = s.getLocation()
##         objx = locx - screenx - (s.sprite.frameW / 2)
##         objy = locy - screeny - (s.sprite.frameH / 2)

##         if s.destStar != None:
##             destx, desty = s.getDest().getLocation()
##             destx = destx - screenx
##             desty = desty - screeny

##             # Random fudge factor
##             objx += (s.sprite.frameW / 2)
##             objy += (s.sprite.frameH / 2)
##             pygame.draw.line( surface, (0,0,64), (objx,objy),
##                               (destx, desty) )

##     def getCost( s ):
##         return s.design.getCost( s.scale )

##     def getMaintainance( self ):
##         return self.getCost() * 0.01



##     def draw( s, surface, screenx, screeny, screenw, screenh ):
##         minx = screenx 
##         maxx = screenx + screenw
##         miny = screeny
##         maxy = screeny + screenh
##         # So if you override getLocation() (like fleet.py does), you can
##         # make something act like it's somewhere it isn't, without
##         # overriding this function.
##         locx, locy = s.getLocation()
##         objx = locx - screenx - (s.sprite.frameW / 2)
##         objy = locy - screeny - (s.sprite.frameH / 2)
##         if (locx >= minx and locx < maxx) and (locy >= miny and locy < maxy):
##             s.prepareSprite()
##             s.sprite.draw( surface, objx, objy )

##     def getName( self ):
##         return self.name

##     def getDesign( self ):
##         return self.design



