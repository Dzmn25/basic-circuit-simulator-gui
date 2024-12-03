# -*- coding: utf-8 -*-

import wx
from utils.schematics import Schematic, FILE_DIR

NORMAL = "./assets/etc/black.png"
SELECTED = "./assets/etc/green.png"
OPTION = "./assets/etc/blue.png"

COMPONENT_DIR = "./assets/components/"

GS = 8


class Node:
    def __init__(self, x, y, interface):
        self.coords = (x, y)
        interface.data = self.coords
        self.interface = interface
        self.up = None
        self.down = None
        self.right = None
        self.left = None


class Board(wx.Panel):
    def __init__(self, parent):
        # PROPIEDADES DE LA CLASE
        wx.Panel.__init__(self,parent)
        self.SetBackgroundColour("White")
        
        # GESTIONAR GRID
        self.filas = 4
        self.columnas = 4
        self.schematic = Schematic()

        # BANDERAS
        self.selected = None
        self.horizontal = True
        self.inverted = False
        self.special = False

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
            coord_y = self.cellHeight * i
            for j in range(1, self.columnas + 1):
                coord_x = self.cellWidth * j
                interface = self.loadInterface(coord_x, coord_y)
                fila.append(Node(len(matrix), len(fila), interface))
            matrix.append(fila)
        return matrix
    
    def onDraw(self, event):
        if len(self.matrix) == 0:
            xsize, ysize = self.GetSize()
            self.cellWidth = int ( xsize / (self.columnas + 1) )
            self.cellHeight = int ( ysize / (self.filas + 1) )
            self.matrix = self.initMatrix()
        event.Skip()

    
    def componentFile(self, component):
        success = False
        if component == 'O':
            success = self.schematic.genTLOC()
        elif component == 'N':
            success = self.schematic.genTLIN()
        elif component == 'G':
            success = self.schematic.genTLSC()
        elif component == 'R':
            success = self.schematic.genResistor(id, )
        elif component == 'V':
            file ="source"
        elif component == 'L':
            file ="inductor"
        elif component == 'C':
            file ="capacitor"
        return success
    
    def componentAttrs(self, coords):
        pos_x, pos_y = coords
        if self.horizontal:
            scale_y = int( self.cellHeight / 2)
            scale_x = self.cellWidth - GS 
            pos_y = pos_y - (scale_x / 4) + GS 
            if self.inverted:
                pos_x -= self.cellWidth - GS
                self.inverted = False
            else:
                pos_x += GS
        else:
            scale_y = self.cellHeight - GS
            scale_x = int( self.cellWidth / 2)
            pos_x -= scale_y / 4 + GS
            if self.inverted:
                pos_y -= self.cellHeight - GS
                self.inverted = False
            else:
                pos_y += GS
            self.horizontal = True
        return ((pos_x, pos_y), (scale_x, scale_y) )

    def loadComponent(self, schematic, coords):
        img = wx.Image(schematic)
        if self.horizontal == False:
            img = img.Rotate90()
        pos, scale = self.componentAttrs(coords)
        if self.special:
            img = img.Scale(scale[0], scale[1], wx.IMAGE_QUALITY_NORMAL)
            self.special = False
        component = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img), wx.Point(pos), scale, style=0)
        component.Bind(wx.EVT_LEAVE_WINDOW, self.closeComponent)
        component.Bind(wx.EVT_ENTER_WINDOW, self.openComponent)
        component.Bind(wx.EVT_LEFT_DOWN, self.leftCliComponent)
        component.Bind(wx.EVT_RIGHT_DOWN, self.rightCliComponent)
        component.SetTransparent(True)
        self.components.append(component)

    def closeComponent(self, event):
        component = event.GetEventObject()
        component.SetBackgroundColour("white")
        component.Update()
        #print("Sali de una imagen")

    def openComponent(self, event):
        component = event.GetEventObject()
        component.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ))
        component.Update()
        #print("Entre a una imagen")

    def leftCliComponent(self, event):
        # ELIMINAR
        event.Skip()

    def rightCliComponent(self, event):
        # EDITAR
        event.Skip()


    def loadOptions(self, coords):
        x, y = coords
        if x > 0:
            self.setBitmap(self.matrix[x-1][y].interface, OPTION)
            self.options.append((x-1, y))
        if y > 0:
            self.setBitmap(self.matrix[x][y-1].interface, OPTION)
            self.options.append((x, y-1))
        if x < (self.columnas -1):
            self.setBitmap(self.matrix[x+1][y].interface, OPTION)
            self.options.append((x+1, y))
        if y < (self.filas - 1):
            self.setBitmap(self.matrix[x][y+1].interface, OPTION)
            self.options.append((x, y+1))

    def resetOptions(self):
        for i in self.options:
            x, y = i
            self.setBitmap(self.matrix[x][y].interface, NORMAL)
        x, y = self.selected.coords
        self.setBitmap(self.matrix[x][y].interface, NORMAL)
        self.selected = None
        self.options = []


    def loadInterface(self, x, y):
        pos_x = x - (GS/2)
        pos_y = y - (GS/2)
        interface = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(self.scaleImage(NORMAL)), wx.Point((pos_x, pos_y)), (GS,GS), wx.BORDER_NONE)
        interface.SetBackgroundColour("white")
        interface.Bind(wx.EVT_LEAVE_WINDOW, self.closeInterface)
        interface.Bind(wx.EVT_ENTER_WINDOW, self.openInterface)
        interface.Bind(wx.EVT_LEFT_DOWN, self.clicInterface)
        return interface

    def openInterface(self, event):
        interface = event.GetEventObject()
        if self.selected == None:
            self.setBitmap(interface, SELECTED)  
        else:
            m_pos = interface.data
            if m_pos in self.options:
                self.setBitmap(interface, SELECTED)  

    def closeInterface(self, event):
        interface = event.GetEventObject()
        if self.selected == None:
            self.setBitmap(interface, NORMAL)
        else:
            m_pos = interface.data
            if m_pos in self.options:
                self.setBitmap(interface, OPTION)  

    def clicInterface(self, event):
        interface = event.GetEventObject()
        m_pos = interface.data
        if self.selected == None:
            self.loadOptions(m_pos)
            self.selected = self.matrix[m_pos[0]][m_pos[1]]
        elif m_pos in self.options:
            if m_pos[0] < self.selected.coords[0] or m_pos[1] < self.selected.coords[1]:
                self.inverted = True
            if self.selected.coords[0] != m_pos[0]:
                self.horizontal = False
            component = self.GetParent().getTarget()
            #self.componentFile(component)
            self.loadComponent( "./assets/components/resistor.png", self.selected.interface.GetPosition() )
            self.resetOptions()
        event.Skip()


    def scaleImage(self, dir):
        img = wx.Image(dir)
        return img.Scale(GS, GS, wx.IMAGE_QUALITY_NORMAL)
        
    def setBitmap(self, interface, dir):
        interface.SetBitmap(wx.Bitmap(self.scaleImage(dir)))
