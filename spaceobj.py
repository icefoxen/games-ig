# spaceobj.py
# A space object.
# Basically, anything that exists on the starmap.

NONETYPE = 0
FLEETTYPE = 1
STARTYPE = 2

class SpaceObj:
    name = ""
    x = 0
    y = 0

    # This is often a class variable...
    sprite = ()

    def __init__( s ):
        pass


    def moveTo( s, x, y ):
        s.x = x
        s.y = y

    def getLocation( s ):
        return (s.x, s.y)

    def prepareSprite( self ):
      self.sprite.setAnim( 0 )


    # There has GOT TO BE A BETTER WAY!!!
    def getType( s ):
        return NONETYPE

    def draw( s, surface, screenx, screeny, screenw, screenh ):
        minx = screenx 
        maxx = screenx + screenw
        miny = screeny
        maxy = screeny + screenh
        # So if you override getLocation() (like fleet.py does), you can
        # make something act like it's somewhere it isn't, without
        # overriding this function.
        locx, locy = s.getLocation()
        if (locx >= minx and locx < maxx) and (locy >= miny and locy < maxy):
            objx = locx - screenx - (s.sprite.getW() / 2)
            objy = locy - screeny - (s.sprite.getH() / 2)
            s.prepareSprite()
            s.sprite.draw( surface, objx, objy )
