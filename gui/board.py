# -*- coding: utf-8 -*-

import wx

NORMAL = "./assets/etc/black.png"
SELECTED = "./assets/etc/green.png"
OPTION = "./assets/etc/blue.png"

COMPONENT = "./assets/components/"

GS = 8


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

        # BANDERAS
        self.selected = None

        # CONTENEDORES
        self.options = []
        self.components = []
        self.matrix = []

        # EVENTOS
        self.Bind(wx.EVT_PAINT, self.onDraw)
        self.Bind(wx.EVT_SIZE, self.resize)

    def resize(self, event):
        self.xsize, self.ysize = self.GetSize()
        self.Refresh()
        event.Skip()

    def componentFile(self, op):
        file = ""
        if op == 'O':
            file ="TLOC"
        elif op == 'N':
            file ="TLIN"
        elif op == 'G':
            file ="TLSC"
        elif op == 'R':
            file ="resistor"
        elif op == 'V':
            file ="source"
        elif op == 'I':
            file ="inductor"
        elif op == 'C':
            file ="capacitor"
        return COMPONENT + file + ".png"

    def loadComponent(self, schematic, coords, horizontal=True):
        img = wx.Image(schematic)
        if horizontal:
            scale_y = int((self.ysize / (self.filas + 1)) / 2)
            scale_x = int(self.xsize / (self.columnas + 1))
        else:
            scale_y = int(self.ysize / (self.filas + 1))
            scale_x = int((self.xsize / (self.columnas + 1)) / 2)

        img = img.Scale(scale_x, scale_y, wx.IMAGE_QUALITY_HIGH)
        component = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img), wx.Point(coords), (scale_x, scale_y), style=0)
        self.components.append(component)

    def loadOptions(self, coords):
        x, y = coords
        if x > 0:
            self.setBitmap(self.matrix[x-1][y], OPTION)
            self.options.append((x-1, y))
        if y > 0:
            self.setBitmap(self.matrix[x][y-1], OPTION)
            self.options.append((x, y-1))
        if x < (self.columnas -1):
            self.setBitmap(self.matrix[x+1][y], OPTION)
            self.options.append((x+1, y))
        if y < (self.filas - 1):
            self.setBitmap(self.matrix[x][y+1], OPTION)
            self.options.append((x, y+1))

    def resetOptions(self, current):
        for i in self.options:
            x, y = i
            self.setBitmap(self.matrix[x][y], NORMAL)
        x, y = self.selected
        self.setBitmap(self.matrix[x][y], NORMAL)
        x, y = current
        self.setBitmap(self.matrix[x][y], SELECTED)
        self.selected = None
        self.options = []

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
        self.loadComponent(self.componentFile('R'), (0, 0))
        event.Skip()

    def newInterface(self, data, x, y):
        pos_x = x - (GS/2)
        pos_y = y - (GS/2)
        interface = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.loadImage(NORMAL)) ,size=(GS,GS), pos=wx.Point((pos_x, pos_y)), style=wx.BORDER_NONE)
        interface.SetBackgroundColour("white")
        interface.data = data
        interface.Bind(wx.EVT_LEAVE_WINDOW, self.closeInterface)
        interface.Bind(wx.EVT_ENTER_WINDOW, self.openInterface)
        interface.Bind(wx.EVT_LEFT_DOWN, self.clicInterface)
        return interface

    def openInterface(self, event):
        interface = event.GetEventObject()
        if self.selected == None:
            self.setBitmap(interface, SELECTED)  
        else:
            m_pos = (interface.data.x, interface.data.y)
            if m_pos in self.options:
                self.setBitmap(interface, SELECTED)  


    def closeInterface(self, event):
        interface = event.GetEventObject()
        if self.selected == None:
            self.setBitmap(interface, NORMAL)
        else:
            m_pos = (interface.data.x, interface.data.y)
            if m_pos in self.options:
                self.setBitmap(interface, OPTION)  

    def clicInterface(self, event):
        interface = event.GetEventObject()
        m_pos = (interface.data.x, interface.data.y)
        if self.selected == None:
            self.loadOptions(m_pos)
            self.selected = m_pos
        elif m_pos in self.options:
            self.resetOptions(m_pos)
            #CREAR LA ARISTA CON LA IMAGEN DEL ESQUEMATICO
        event.Skip()

    def loadImage(self, dir):
        img = wx.Image(dir)
        return img.Scale(GS, GS, wx.IMAGE_QUALITY_NORMAL)
        
    def setBitmap(self, interface, dir):
        interface.SetBitmap(wx.Bitmap(self.loadImage(dir)))
