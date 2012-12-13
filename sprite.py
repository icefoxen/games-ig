# sprite.py
# A sprite object.  It draws itself on a surface, handles animations
# from a sheet or strip, and can have arbitrary animation sequences
# specified in a config file.
#
#  Sprite Sheet
#  ------> anim frames
# |oooooo
# |xxxxxx
# |yyyyyy
# |zzzzzz
# v
# different sprites or variations of the same sprite
#
# Simon Heath
# 19/9/2005

import wx

from loader import *

# ...iiiinteresting.  If a class has a variable whose default object
# is non-atomic, that object is shared between all instances of the
# class.  In other words, it's treated like Java's static members.
class Sprite:
   cfgfile = ""
   img = ()
   imgFile = ""
   numFramesW = 0
   numFramesH = 0
   sourcePoint = ()
   sourceSize = ()

   # "anim" is a hashtable of lists of 2-element lists.
   # yaml doesn't do tuples, which is what I'd prefer, but oh well.
   anims = {}
   currentAnimName = ""
   currentAnim = []
   currentFrameIndex = 0

   animLoop = False
   animDelay = 0
   lastAnim = 0

   def __init__( s, cfgfile ):
      s.cfgfile = cfgfile
      cfg = cfgloader.get( cfgfile )
      s.imgFile = cfg['imgFile']
      s.img = imgloader.get( s.imgFile )
      frameW = cfg['frameW']
      frameH = cfg['frameH']
      rct = s.img.GetSize()
      s.numFramesW = rct.GetWidth() / frameW
      s.numFramesH = rct.GetHeight() / frameH
      s.animDelay = cfg['animDelay']
      s.sourcePoint = wx.Point( 0, 0 )
      s.sourceSize = wx.Size( frameW, frameH )

      s.anims = cfg['anims']

   def getW( s ):
      return s.sourceSize.GetWidth()

   def getH( s ):
      return s.sourceSize.GetHeight()

   def draw( s, screen, x, y ):
      screen.BlitPointSize( wx.Point( x, y ), s.sourceSize, s.img,
                            s.sourcePoint, useMask=True )


   def setAnim( s, animname ):
      s.currentAnimName = animname
      s.currentFrameIndex = 0
      s.currentAnim = s.anims[animname]
      firstFrame = s.currentAnim[0]
      s.sourcePoint.x = (firstFrame[0] * s.getW())
      s.sourcePoint.y = (firstFrame[1] * s.getH())
      

   def setAnimLoop( s, loop ):
      s.animLoop = loop

   def setAnimDelay( s, delay ):
      s.animDelay = 0

   def anim( s, t ):
      if (t - s.lastAnim) > s.animDelay:
         s.lastAnim = t
         s.nextFrame()


   def nextFrame( s ):
      s.currentFrameIndex += 1
      if s.currentFrameIndex > (len( s.currentAnim ) - 1):
         s.currentFrameIndex = 0
      # Life would be nicer if currentAnim held tuples instead of
      # 2-element lists, but I don't wanna bother converting them
      # and this works anyway.  I'm not sure it would even make
      # much difference, internally or externally.
      s.sourcePoint.x = s.currentAnim[s.currentFrameIndex][0] * \
                        s.sourceSize.getWidth()
      s.sourcePoint.y = s.currentAnim[s.currentFrameIndex][1] * \
                        s.sourceSize.getHeight()
      

   def prevFrame( s ):
      s.currentFrameIndex -= 1
      if s.currentFrameIndex < 0:
         s.currentFrameIndex = len( s.currentAnim ) - 1
      s.sourcePoint.x = s.currentAnim[s.currentFrameIndex][0] * \
                        s.sourceSize.getWidth()
      s.sourcePoint.y = s.currentAnim[s.currentFrameIndex][1] * \
                        s.sourceSize.getHeight()

   def frameNumber( s, i ):
      return s.currentAnim

   def setAnimDelay( s, i ):
      s.animDelay = i
   def getAnimDelay( s, i ):
      return s.animDelay
   
