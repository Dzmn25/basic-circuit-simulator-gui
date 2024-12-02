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

        # BANDERAS
        self.selected = None
        self.horizontal = True

        # CONTENEDORES
        self.options = []
        self.components = []
        self.matrix = []

        # EVENTOS
        self.Bind(wx.EVT_PAINT, self.onDraw)

    
    def initMatrix(self):
        matrix = []
        for i in range(1, self.filas + 1):
            fila = []
            coord_y = int((self.ysize / (self.filas + 1)) * i)
            for j in range(1, self.columnas + 1):
                coord_x = int((self.xsize / (self.columnas + 1) ) * j)
                interface = self.loadInterface(Data(len(matrix), len(fila)), coord_x, coord_y)
                fila.append(interface)
            matrix.append(fila)
        return matrix
    
    def onDraw(self, event):
        if len(self.matrix) == 0:
            self.xsize, self.ysize = self.GetSize()
            self.matrix = self.initMatrix()
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
    
    def componentAttrs(self, coords):
        pos_x, pos_y = coords
        if self.horizontal:
            scale_y = int( ( self.ysize / ( self.filas + 1 ) ) / 2)
            scale_x = int( ( self.xsize / ( self.columnas + 1) ) - GS )
            pos_x += GS
            pos_y = pos_y - (scale_x / 4) + GS 
        else:
            scale_y = int( self.ysize / ( self.filas + 1 ) - GS)
            scale_x = int( ( self.xsize / ( self.columnas + 1 ) ) / 2)
            pos_x -= scale_y / 4 + GS
            pos_y += GS
            self.horizontal = True
        return ((pos_x, pos_y), (scale_x, scale_y) )

    def loadComponent(self, schematic, coords):
        img = wx.Image(schematic)
        if self.horizontal == False:
            img = img.Rotate90()
        pos, scale = self.componentAttrs(coords)
        component = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img), wx.Point(pos), scale, style=0)
        component.Bind(wx.EVT_LEAVE_WINDOW, self.closeComponent)
        component.Bind(wx.EVT_ENTER_WINDOW, self.openComponent)
        self.components.append(component)

    def closeComponent(self, event):
        event.Skip()

    def openComponent(self, event):
        event.Skip()


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

    def resetOptions(self):
        for i in self.options:
            x, y = i
            self.setBitmap(self.matrix[x][y], NORMAL)
        x, y = self.selected.coords
        self.setBitmap(self.matrix[x][y], NORMAL)
        self.selected = None
        self.options = []


    def loadInterface(self, data, x, y):
        pos_x = x - (GS/2)
        pos_y = y - (GS/2)
        interface = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.loadImage(NORMAL)), wx.Point((pos_x, pos_y)), (GS,GS), wx.BORDER_NONE)
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
            self.selected = Data(None, None)
            self.selected.coords = m_pos
            self.selected.pos = interface.GetPosition()
        elif m_pos in self.options:
            if self.selected.coords[0] != m_pos[0]:
                self.horizontal = False
            self.loadComponent( self.componentFile('R'), self.selected.pos )
            self.resetOptions()
        event.Skip()


    def loadImage(self, dir):
        img = wx.Image(dir)
        return img.Scale(GS, GS, wx.IMAGE_QUALITY_NORMAL)
        
    def setBitmap(self, interface, dir):
        interface.SetBitmap(wx.Bitmap(self.loadImage(dir)))
