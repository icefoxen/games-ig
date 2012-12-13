# main.ml
# Not quite sure how all this should hook together, yet...
#
# We have to tie together the real GUI, whatever GUI hard-coding we
# end up doing, and the starmap, and put it all in the same event
# and drawing structure.


import sys, pygame
from pygame.locals import *

from starmap import *
from universe import *
#import input
import empire
import empireset
import race
import colony
import fleet
import ship
from gui import *

import wx



def genUniverse():
   starmap = Starmap( 1000, 1000, 500 )
   empires = empireset.EmpireSet()
   testEmp = empire.Empire( "Foobian", race.baserace, \
                            starmap.selected, )
   testEmp.addNewColony( starmap.selected, 50 )
   empires.add( testEmp )
   return Universe( starmap, empires )



def main():
   pygame.init()
   app = wx.PySimpleApp()
   frame = wx.Frame( None, title="Imperium Gate", size=(800,600) )

   universe = genUniverse()
   
   MainScreen( frame, universe )
   frame.Show( True )

   app.MainLoop()



if __name__ == '__main__':
   main()
