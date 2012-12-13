from sprite import *
from starmap import *

import wx


class TestWindow( wx.Panel ):
   def __init__( self, parent ):
      wx.Panel.__init__( self, parent )
      wx.EVT_PAINT( self, self.onPaint )
      self.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )

      self.sprite = Sprite( 'star.sprite' )

   def onPaint( self, event=None ):
      dc = wx.PaintDC( self )
      self.sprite.draw( dc, 10, 10 )

class TestFrame( wx.Frame ):
   def __init__( self, parent=None ):
      wx.Frame.__init__( self, parent, title="Foo", size=(400,300) )
      #win = TestWindow( self )
      starmap = Starmap( 1000, 1000, 500 )
      win = StarmapPanel( self, starmap )


app = wx.App()
frame = TestFrame()
frame.Show( True )
app.MainLoop()
