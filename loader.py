#
# loader.py
# This is a resource loader that makes sure resources have only
# been loaded once.  Resources are sounds, config files, images,
# and just about anything else.
#
# Simon Heath
# 15/9/2005

import os, pygame
from pygame.locals import *
import wx

import config

colorkey = (255, 0, 128)
currentmusic = ()
fontsize = 14

class ResourceLoader:
   rdir = ""
   rtable = {}
   loadFunc = {}
   def __init__( s, dir, loadFunc ):
      s.rdir = dir
      s.loadFunc = loadFunc

   # Ditches all the cached resources
   # Useful mainly for re-loading things after changes.
   def purge( s ):
      s.rtable = {}

   # Ditches a certain cached resource.
   def remove( s, name ):
      s.rtable.pop( name )

   def get( s, name ):
      if s.rtable.has_key( name ):
         return s.rtable[name]
      else:
         itm = s.loadFunc( (s.rdir + name) )
         s.rtable[name] = itm
         return itm


# This may be a horrid kludge, or it may be brilliant.
# Either way, DC.Blit needs another DC to blit from, not a Bitmap, so.
# We use SelectObject, which means that ONLY ONE MEMORY DC can 
# use the given bitmap.
def loadImage( s ):
   print "Image %s loaded" % s
   a = wx.Bitmap( s )
   bitmask = wx.Mask( a, wx.Colour( 255, 0, 128 ) )
   a.SetMask( bitmask )
   buff = wx.MemoryDC()
   buff.SelectObject( a )
   return buff

def loadSound( s ):
   print "Sound %s loaded" % s
   return pygame.mixer.Sound( s )

def loadConfig( s ):
   print "Config %s loaded" % s
   return config.ConfigLoader( s )

def loadFont( s  ):
   print "Font %s loaded in size %d" % (s, fontsize)
   return pygame.font.Font( s, fontsize )

imgloader = ResourceLoader( "images/", loadImage )
soundloader = ResourceLoader( "sounds/", loadSound )
cfgloader = ResourceLoader( "config/", loadConfig )
fontloader = ResourceLoader( "fonts/", loadFont )


def playMusic( music ):
   s = soundloader.get( music )
   currentmusic.stop()
   currentmusic = s
   currentmusic.play( -1 )  # -1 means infinate loop.

def playSound( sound ):
   return


def getDefaultFont():
   return fontloader.get( "cour.ttf" )
