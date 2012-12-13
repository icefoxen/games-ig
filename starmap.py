# starmap.py
# A map full of stars.  Yay!
#
# This could be converted to blit itself onto a surface at an arbitrary
# location, but it'd be a pain in the ass.  It doesn't really matter,
# so I'm not gonna bother.



import star, sprite
import spaceobj

import wx




class Starmap:
   w = 0
   h = 0

   # A quadtree would be rather nicer for this than a list.  Oh well!
   objects = []
   selected = ()

   def __init__( self, x, y, numstars ):
      self.w = x
      self.h = y
      for i in range( numstars ):
         self.objects.append( star.Star( x, y ) )
      self.selected = self.objects[0]


   def getSelectedObj( self ):
      return self.selected

   # Returns True if a new star has been selected, False otherwise
   # Should call the object-defined getLocation method!  This'll let fleets
   # in orbit report slightly false values, which would work.
   def selectObj( self, x, y ):
      delta = 7
      for obj in self.objects:
         objx, objy = obj.getLocation()
         if ((x > (objx - delta)) and (x < (objx + delta))) and \
             ((y > (objy - delta)) and (y < (objy + delta))):
            self.selected = obj
            print obj  # DEBUG
            return True

      return False

   def getStar( self, x, y ):
      for thingy in objects:
         if thingy.x == x and thingy.y == y:
            return thingy
      return False

   def getStarByName( self, name ):
      for thingy in objects:
         if thingy.name == name:
            return thingy
      return False

   def add( self, obj ):
      self.objects.append( obj )

   def remove( self, obj ):
      try:
         self.objects.remove( obj )
      except ValueError:
         print "Tried to remove %s twice!" % str( obj )
