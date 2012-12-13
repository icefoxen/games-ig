# gui.py
# Draws the GUI
#

import pygame
from pygame.locals import *

import loader
from star import *
import starmap
import spaceobj
import colony

import wx

GAME_ID = 101
DESIGN_ID = 102
FLEET_ID = 103
PLANETS_ID = 104
MAP_ID = 105
RACES_ID = 106
TECH_ID = 107
TURN_ID = 110

MOVE_ID = 111

SHIPSLIDER_ID = 120
DEFENCESLIDER_ID = 121
FACTORYSLIDER_ID = 122
COLONYSLIDER_ID = 123

SHIPTOGGLE_ID = 130
DEFENCETOGGLE_ID = 131
FACTORYTOGGLE_ID = 132
COLONYTOGGLE_ID = 133


# Hmmm, status bar...

class MainScreen( wx.Panel ):
   
   def __init__( self, parent, universe ):
      wx.Panel.__init__( self, parent )

      self.moving = False
      self.movingFleet = ()

      self.universe = universe

      self.sm = StarmapPanel( self, universe.starmap )

      self.notebook = wx.Notebook( self )
      self.starpanel = StarPanel( self.notebook )
      self.fleetpanel = FleetPanel( self.notebook )
      self.notebook.AddPage( self.starpanel, "Star" )
      self.notebook.AddPage( self.fleetpanel, "Fleets" )

      hsizer = wx.BoxSizer( wx.HORIZONTAL )
      hsizer.Add( self.sm, 4, flag=wx.EXPAND | wx.ALL )
      hsizer.Add( self.notebook, 1, flag=wx.EXPAND | wx.ALL, border=2 )


      bottombar = MenuPanel( self, self.universe )

      vsizer = wx.BoxSizer( wx.VERTICAL )
      vsizer.Add( hsizer, 15, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( bottombar, 1, flag=wx.ALIGN_CENTER, border=1 )


      self.SetSizer( vsizer )



      wx.EVT_BUTTON( self, TURN_ID, self.doNextTurn )
      wx.EVT_TOGGLEBUTTON( self, MOVE_ID, self.doMove )

   def doMove( self, event ):
      if event.Checked():
         self.moving = True
         self.movingFleet = self.universe.starmap.getSelectedObj()
         
      


   def doSelection( self, selected ):
      if self.moving:
         self.movingFleet.setDest( selected )
         self.fleetpanel.focusOn( self.movingFleet )
         self.moving = False
         self.fleetpanel.unToggleMove()
         self.universe.starmap.selectObj( self.movingFleet.x,
                                          self.movingFleet.y )
      else:
         if selected.getType() == spaceobj.STARTYPE:
            self.setSidebar( 0 )
            self.starpanel.focusOn( selected )
         elif selected.getType() == spaceobj.FLEETTYPE:
            self.setSidebar( 1 )
            self.fleetpanel.focusOn( selected )
         else:
            print "HELP!  Impossible spaceobj type!"


   def setSidebar( self, i ):
      self.notebook.SetSelection( i )

   def doNextTurn( self, e ):
      self.universe.calcTurn()
      selection = self.universe.starmap.getSelectedObj()
      if selection.getType() == FLEETTYPE:
         self.fleetpanel.focusOn( selection )
      else:
         self.starpanel.focusOn( selection )

      self.sm.paint( e )

   
class StarPanel( wx.Panel ):
   def __init__( self, parent ):      
      wx.Panel.__init__( self, parent )

      self.star = None

      self.nametext = wx.StaticText( self, label="Star name" )
      # The way it resizes these things is kinda wiggy.
      # Figure out how it works.
      self.xtext = wx.StaticText( self, label="               " )
      self.ytext = wx.StaticText( self, label="" )

      self.maxColonytext = wx.StaticText( self, label="Max Colonies" )
      self.maxPoptext = wx.StaticText( self, label="Max pop" )
      self.richnesstext = wx.StaticText( self, label="Mineral richness" )

      self.seperator = wx.StaticLine( self )
      self.colonypanel = ColonyPanel( self )

      
      hsizer = wx.BoxSizer( wx.HORIZONTAL )
      hsizer.Add( self.xtext, flag=wx.EXPAND, border=1 )
      hsizer.Add( self.ytext, flag=wx.EXPAND, border=1 )

      vsizer = wx.StaticBoxSizer( wx.StaticBox( self ), wx.VERTICAL )
      vsizer.Add( self.nametext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( hsizer, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.maxColonytext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.maxPoptext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.richnesstext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.seperator, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.colonypanel, flag=wx.EXPAND | wx.ALL, border=1 )

      self.SetSizer( vsizer )

      

   def focusOn( self, star ):
      self.nametext.SetLabel( star.name )
      self.xtext.SetLabel( "X: " + str( star.x ) )
      self.ytext.SetLabel( "Y: " + str( star.y ) )
      self.maxColonytext.SetLabel( "Max colonies: " + str( star.maxColonies ) )
      self.maxPoptext.SetLabel( "Max pop: " + str( star.maxPop ) )
      self.richnesstext.SetLabel( "Richness: " + str( star.richness ) )

      self.colonypanel.focusOn( star )
                         

# Sliders: Make it kinda like the Pax Imperia research; to put 
# resources into one, you have to first take resources out of another,
# putting it in a "free" pool.  Any resources in this pool just
# go into treasury or whatever.  Each slider only takes points from
# the free pool, and only puts points into the free pool.
# This may simplify management.
class ColonyPanel( wx.Panel ):
   def __init__( self, parent ):
      wx.Panel.__init__( self, parent )
      self.colony = None

      self.shipslider = wx.Slider( self, SHIPSLIDER_ID )
      self.defenceslider = wx.Slider( self, DEFENCESLIDER_ID )
      self.factoryslider = wx.Slider( self, FACTORYSLIDER_ID )
      self.colonyslider = wx.Slider( self, COLONYSLIDER_ID )

      self.shipslider.SetRange( 0, 100 )
      self.defenceslider.SetRange( 0, 100 )
      self.factoryslider.SetRange( 0, 100 )
      self.colonyslider.SetRange( 0, 100 )

      self.shiptoggle = wx.CheckBox( self, SHIPTOGGLE_ID, "Ship" )
      self.defencetoggle = wx.CheckBox( self, DEFENCETOGGLE_ID, "Def" )
      self.factorytoggle = wx.CheckBox( self, FACTORYTOGGLE_ID, "Fact" )
      self.colonytoggle = wx.CheckBox( self, COLONYTOGGLE_ID, "Col" )

      fgsizer = wx.FlexGridSizer( 4, 2, 0, 0 )
      fgsizer.AddGrowableCol( 1, 1 )
      fgsizer.AddGrowableCol( 2, 10 )

      fgsizer.Add( self.shiptoggle, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.shipslider, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.defencetoggle, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.defenceslider, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.factorytoggle, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.factoryslider, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.colonytoggle, flag=wx.EXPAND | wx.ALL, border=1 )
      fgsizer.Add( self.colonyslider, flag=wx.EXPAND | wx.ALL, border=1 )
      self.SetSizer( fgsizer )

      wx.EVT_SLIDER( self, SHIPSLIDER_ID, self.setShipSlider )
      wx.EVT_SLIDER( self, DEFENCESLIDER_ID, self.setDefenceSlider )
      wx.EVT_SLIDER( self, FACTORYSLIDER_ID, self.setFactorySlider )
      wx.EVT_SLIDER( self,  COLONYSLIDER_ID, self.setColonySlider )

      wx.EVT_CHECKBOX( self, SHIPTOGGLE_ID, self.lockShipSlider )
      wx.EVT_CHECKBOX( self, DEFENCETOGGLE_ID, self.lockDefenceSlider )
      wx.EVT_CHECKBOX( self, FACTORYTOGGLE_ID, self.lockFactorySlider )
      wx.EVT_CHECKBOX( self, COLONYTOGGLE_ID, self.lockColonySlider )

   def setShipSlider( self, e ):
      if self.colony != None:
         self.colony.setProd( colony.SHIP, self.shipslider.GetValue() / 100.0 )
         self.focusOn( self.colony.world )

   def setDefenceSlider( self, e ):
      if self.colony != None:
         self.colony.setProd( colony.DEFENCE, self.defenceslider.GetValue() / 100.0 )
         self.focusOn( self.colony.world )
      
   def setFactorySlider( self, e ):
      if self.colony != None:
         self.colony.setProd( colony.FACTORY, self.factoryslider.GetValue() / 100.0 )
         self.focusOn( self.colony.world )
            
   def setColonySlider( self, e ):
      if self.colony != None:
         self.colony.setProd( colony.COLONY, self.colonyslider.GetValue() / 100.0 )
         self.focusOn( self.colony.world )

   def lockShipSlider( self, e ):
      self.colony.toggleLock( colony.SHIP )

   def lockDefenceSlider( self, e ):
      self.colony.toggleLock( colony.DEFENCE )
      
   def lockFactorySlider( self, e ):
      self.colony.toggleLock( colony.FACTORY )

   def lockColonySlider( self, e ):
      self.colony.toggleLock( colony.COLONY )



   def focusOn( self, star ):
      if star.hasColony():
         self.colony = star.getColony()

         self.shipslider.SetValue(
            int( self.colony.getProd( colony.SHIP ) * 100 ) )
         self.defenceslider.SetValue(
            int( self.colony.getProd( colony.DEFENCE ) * 100 ) )
         self.factoryslider.SetValue(
            int( self.colony.getProd( colony.FACTORY ) * 100 ) )
         self.colonyslider.SetValue(
            int( self.colony.getProd( colony.COLONY ) * 100 ) )
      else:
         self.colony = None
         self.shipslider.SetValue( 0 )
         self.defenceslider.SetValue( 0 )
         self.factoryslider.SetValue( 0 )
         self.colonyslider.SetValue( 0 )




class FleetPanel( wx.Panel ):
   def __init__( self, parent ):
      wx.Panel.__init__( self, parent )

      self.fleet = None
      self.nametext = wx.StaticText( self, label="Name" )
      self.desttext = wx.StaticText( self, label="Destination" )
      self.etatext = wx.StaticText( self, label="ETA" )
      self.shipslist = wx.ListBox( self, size=wx.Size( -1, 150 ) )

      self.moveButton = wx.ToggleButton( self, MOVE_ID, "Move" )

      vsizer = wx.StaticBoxSizer( wx.StaticBox( self ), wx.VERTICAL )
      vsizer.Add( self.nametext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.desttext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.etatext, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.shipslist, flag=wx.EXPAND | wx.ALL, border=1 )
      vsizer.Add( self.moveButton, flag=wx.EXPAND | wx.ALL, border=1 )

      self.SetSizer( vsizer )

   def focusOn( self, fleet ):
      self.nametext.SetLabel( "Fleet " + fleet.getName() )

      destname = ""
      if fleet.getDest() == None:
         destname = "Orbiting " + fleet.orbiting.name
      else:
         destname = "Going to " + fleet.getDest().name
      self.desttext.SetLabel( destname )
      self.etatext.SetLabel( "ETA: " + str( fleet.getETA() ) + " turns" )

      a = fleet.getShips()
      self.shipslist.Clear()
      for x in a:
         self.shipslist.Append( (x.getName() + ": " + str( a[x] ) ) )



   def unToggleMove( self ):
      self.moveButton.SetValue( False )
      



class MenuPanel( wx.Panel ):
   def __init__( self, parent, universe ):
      wx.Panel.__init__( self, parent )

      self.universe = universe

      gameB = wx.Button( self, GAME_ID, 'Game' )
      designB = wx.Button( self, DESIGN_ID, 'Design' )
      fleetB = wx.Button( self, FLEET_ID, 'Fleet' )
      planetsB = wx.Button( self, PLANETS_ID, 'Planets' )
      mapB = wx.Button( self, MAP_ID, 'Map' )
      racesB = wx.Button( self, RACES_ID, 'Races' )
      techB = wx.Button( self, TECH_ID, 'Tech' )
      turnB = wx.Button( self, TURN_ID, 'Next Turn' )

      sizer = wx.BoxSizer( wx.HORIZONTAL )
      sizer.Add( gameB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( designB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( fleetB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( planetsB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( mapB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( racesB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( techB, flag=wx.EXPAND | wx.ALL, border=1 )
      sizer.Add( turnB, flag=wx.EXPAND | wx.ALL, border=1 )


      self.SetSizer( sizer )

   def doNextTurn( self, e ):
      self.universe.calcTurn()



# wx.lib.colourchooser.canvas.Canvas may be quite useful here
class StarmapPanel( wx.Panel ):   
   def __init__( self, parent, starmap ):
      wx.Panel.__init__( self, parent )
      wx.EVT_PAINT( self, self.paint )

      self.parent = parent

      self.starmap = starmap

      # Logical screenworld coordinates
      self.screenx = 0
      self.screeny = 0
      self.screenw = 0
      self.screenh = 0
      self.cursorSprite = sprite.Sprite( "cursor.sprite" )

      wx.EVT_LEFT_DOWN( self, self.onClick )



   # We must repaint on a click, as we've moved or highlighted stuff.
   # Yay!
   def onClick( self, e ):
      x = e.GetX()
      y = e.GetY()
      if not self.starmap.selectObj( self.screenx + x, self.screeny + y ):
         self.centerScreenOn( x, y )
      self.paint( e )

      # Magic happens here to make the fleet panel display when we
      # click on a fleet, and so on.
      # This also gives it the right things to display.
      selected = self.starmap.getSelectedObj()
      self.parent.doSelection( selected )





   def getSelected( self ):
      return self.starmap.getSelected()

   def moveScreenTo( self, x, y ):
      maxx = self.starmap.w - self.screenw
      maxy = self.starmap.h - self.screenh
      self.screenx = x
      if self.screenx > maxx:
         self.screenx = maxx
      elif self.screenx < 0:
         self.screenx = 0

      self.screeny = y
      if self.screeny > maxy:
         self.screeny = maxy
      elif self.screeny < 0:
         self.screeny = 0

   def centerScreenOn( self, x, y ):
      if (x < self.screenw) and (y < self.screenh):
         self.moveScreenTo( self.screenx + (x - (self.screenw / 2)), \
                            self.screeny + (y - (self.screenh / 2)) )



   # What would be cool is if we could draw little numbers on the gridlines.
   def drawGrid( self, dc ):
      GRIDINC = 100

      dc.SetPen( wx.Pen( wx.Colour( 48, 48, 48 ), 1, wx.SOLID ) )
      
      xoffset = GRIDINC - (self.screenx % GRIDINC)
      yoffset = GRIDINC - (self.screeny % GRIDINC)
      for x in range( xoffset, self.screenw, GRIDINC ):
         dc.DrawLine( x, 0, x, self.screenh )

      for y in range( yoffset, self.screenh, GRIDINC ):
         dc.DrawLine( 0, y, self.screenw, y )


   def drawStars( self, surface ):
      for x in self.starmap.objects:
         x.draw( surface, self.screenx, self.screeny, \
                 self.screenw, self.screenh )



   def drawCursor( self, surface ):
      objx, objy = self.starmap.selected.getLocation()
      minx = self.screenx 
      maxx = self.screenx + self.screenw
      miny = self.screeny
      maxy = self.screeny + self.screenh
      
      # Draw cursor
      if (objx >= minx and objx < maxx) and (objy >= miny and objy < maxy):
         selectx = objx - self.screenx - \
                   (self.cursorSprite.getW() / 2)
         selecty = objy - self.screeny - \
                   (self.cursorSprite.getH() / 2)
         self.cursorSprite.draw( surface, selectx, selecty )

      if self.starmap.selected.getType() == spaceobj.FLEETTYPE:
         self.starmap.selected.drawPath( surface, self.screenx, self.screeny, \
                                 self.screenw, self.screenh )


   def paint( self, evt ):
      dc = wx.PaintDC( self )
      
      size = self.GetClientSize()
      self.screenw = size.GetWidth()
      self.screenh = size.GetHeight()

      dc.SetBrush( wx.Brush( wx.BLACK, wx.SOLID ) )
      dc.SetPen( wx.Pen( wx.BLACK, wx.SOLID ) )
      # Clear the screen
      dc.DrawRectangle( 0, 0, self.screenw, self.screenh )
      self.drawGrid( dc )
      self.drawStars( dc )
      self.drawCursor( dc )
