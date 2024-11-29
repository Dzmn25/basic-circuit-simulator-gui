# -*- coding: utf-8 -*-

import wx
import math
import schemdraw
import schemdraw.elements as elm

NORMAL = "./assets/black.png"
SELECTED = "./assets/green.png"


class Data:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board(wx.Panel):
    def __init__(self, parent):
        # PROPIEDADES DE LA CLASE
        wx.Panel.__init__(self,parent)
        self.SetBackgroundColour("White")
        
        # GESTIONAR GRID
        self.filas = 4
        self.columnas = 4
        self.xsize, self.ysize = self.GetSize()
        self.matrix = []
        self.resized = False

        # GESTIONAR OBJETOS
        self.selected = None

        # EVENTOS
        self.Bind(wx.EVT_PAINT, self.onDraw)
        self.Bind(wx.EVT_SIZE, self.resize)

    def resize(self, event):
        self.cleanMatrix()
        self.xsize, self.ysize = self.GetSize()
        self.Refresh()
        event.Skip()

    def cleanMatrix(self):
        for i in self.matrix:
            for j in i:
                j.Destroy()
        self.matrix = []

    def initMatrix(self):
        matrix = []
        for i in range(1, self.filas + 1):
            fila = []
            coord_y = int((self.ysize / (self.filas + 1)) * i)
            for j in range(1, self.columnas + 1):
                coord_x = int((self.xsize / (self.columnas + 1) ) * j)
                interface = self.newInterface(Data(len(matrix), len(fila)), coord_x, coord_y)
                fila.append(interface)
            matrix.append(fila)
        return matrix

    def onDraw(self, event):
        self.matrix = self.initMatrix()
        event.Skip()

    def newInterface(self, data, x, y):
        interface = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.loadImage(NORMAL)) ,size=(8,8), pos=wx.Point((x, y)), style=wx.BORDER_NONE)
        interface.SetBackgroundColour("white")
        interface.data = data
        interface.Bind(wx.EVT_LEAVE_WINDOW, self.closeInterface)
        interface.Bind(wx.EVT_ENTER_WINDOW, self.openInterface)
        interface.Bind(wx.EVT_LEFT_DOWN, self.clicInterface)
        return interface

    def openInterface(self, event):
        interface = event.GetEventObject()
        self.setBitmap(interface, SELECTED)     

    def closeInterface(self, event):
        interface = event.GetEventObject()
        self.setBitmap(interface, NORMAL)
        event.Skip()

    def clicInterface(self, event):
        print("Ay, mi pancita")

    def loadImage(self, urlImg):
        img = wx.Image(urlImg)
        return img.Scale(8, 8, wx.IMAGE_QUALITY_NORMAL)
    
    def setBitmap(self, interface, urlImg):
        interface.SetBitmap(wx.Bitmap(self.loadImage(urlImg)))
