# -*- coding: utf-8 -*-

import wx
from utils.schematics import Schematic, FILE_DIR

NORMAL = "./assets/etc/black.png"
SELECTED = "./assets/etc/green.png"
OPTION = "./assets/etc/blue.png"
OCCUPED = "./assets/etc/red.png"

COMPONENT = "./assets/component.png"

OPPOSITE = { "up": "down", "down":"up", "left":"right", "right":"left" }

GS = 8


class Node:
    def __init__(self, x, y, interface):
        self.coords = (x, y)
        interface.data = self.coords
        self.interface = interface
        self.id = None
        self.neighbors = {
            "up" : None,
            "down" : None,
            "right" : None,
            "left" : None
        }

class Component:
    def __init__(self, origin, dest, dir, id, values, uiElement):
        self.start = origin
        self.end = dest
        self.dir = dir
        self.id = id
        self.values = values
        self.uiElement = uiElement

class Board(wx.Panel):
    def __init__(self, parent):
        # PROPIEDADES DE LA CLASE
        wx.Panel.__init__(self,parent)
        self.SetBackgroundColour("White")
        
        # GESTIONAR GRID
        self.filas = 4
        self.columnas = 4
        self.schematic = Schematic()

        #IDS
        self.nodeId = 0

        # BANDERAS
        self.selected = None
        self.horizontal = True
        self.inverted = False
        self.special = False

        # CONTENEDORES
        self.options = []
        self.occupied = []
        self.components = []
        self.matrix = []
        self.availables = []

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
                x = len(matrix)
                y = len(fila)
                node = Node(x, y, interface)
                node.neighbors["up"] = 1 if x == 0 else None
                node.neighbors["left"] = 1 if y == 0 else None
                node.neighbors["down"] = 1 if x == (self.filas - 1) else None
                node.neighbors["right"] = 1 if y == (self.columnas - 1) else None
                fila.append(node)
            matrix.append(fila)
        return matrix
    
    def initSource(self):
        self.inverted = True
        self.horizontal = False
        id = self.schematic.genImg("V", self.horizontal)
        if id != None:
            ori = (self.filas - 1, 0) ; dest = (self.filas - 2, 0)
            self.lockOptions(ori, dest)
            pos = self.matrix[ori[0]][ori[1]].interface.GetPosition()
            self.newComponent( COMPONENT, ori, dest, pos, id)
            self.setNodeId(ori, dest)

    def initGround(self):
        id = self.schematic.genImg("T", self.horizontal)
        if id != None:
            for i in range(self.columnas - 1):
                ori = (self.filas - 1, i) ; dest = (self.filas - 1, i+1)
                self.lockOptions(ori, dest)
                pos = self.matrix[ori[0]][ori[1]].interface.GetPosition()
                self.newComponent( COMPONENT, ori, dest, pos, id)
                self.setNodeId(ori, dest, "T")
    
    def onDraw(self, event):
        if len(self.matrix) == 0:
            xsize, ysize = self.GetSize()
            self.cellWidth = int ( xsize / (self.columnas + 1) )
            self.cellHeight = int ( ysize / (self.filas + 1) )
            self.matrix = self.initMatrix()
            self.initSource()
            self.initGround()
        event.Skip()

    def Cancel(self):
        if self.selected != None:
            self.resetOptions()

    def addAvailable(self, ori, dest):
        if not ori in self.availables:
            self.availables.append(ori)
        if not dest in self.availables:
            self.availables.append(dest)


    def loadComponent(self, button, m_pos):
        target =  self.GetParent().getTarget()
        if m_pos[0] < self.selected.coords[0] or m_pos[1] < self.selected.coords[1]:
            self.inverted = True
        if self.selected.coords[0] != m_pos[0]:
            self.horizontal = False
        self.lockOptions(button.data, self.selected.coords)
        id = self.schematic.genImg( target, self.horizontal )
        if id != None:
            self.newComponent( COMPONENT, self.selected.coords, m_pos , self.selected.interface.GetPosition(), id)
            self.setNodeId(self.selected.coords, m_pos)
        self.resetOptions()
    
    def componentAttrs(self, coords):
        pos_x, pos_y = coords
        if self.horizontal:
            scale_y = int( self.cellHeight / 2)
            scale_x = self.cellWidth - GS 
            pos_y -= (scale_x / 4) + GS - 8
            if self.inverted:
                pos_x -= self.cellWidth - GS
                self.inverted = False
            else:
                pos_x += GS
        else:
            scale_y = self.cellHeight - GS
            scale_x = int( self.cellWidth / 2)
            pos_x -= scale_y / 4 + GS + 5
            if self.inverted:
                pos_y -= self.cellHeight - GS
                self.inverted = False
            else:
                pos_y += GS
            self.horizontal = True
        return ((pos_x, pos_y), (scale_x, scale_y) )

    def newComponent(self, schematic, origin, dest, coords, id):
        img = wx.Image(schematic)
        dir = "right" if self.inverted == False else "left"
        if self.horizontal == False:
            #img = img.Rotate90()
            dir = "down" if self.inverted == False else "up"
        pos, scale = self.componentAttrs(coords)
        if self.special:
            img = img.Scale(scale[0], scale[1], wx.IMAGE_QUALITY_NORMAL)
            self.special = False
        uiComponent = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img), wx.Point(pos), scale, style=0)
        uiComponent.Bind(wx.EVT_LEAVE_WINDOW, self.closeComponent)
        uiComponent.Bind(wx.EVT_ENTER_WINDOW, self.openComponent)
        uiComponent.Bind(wx.EVT_LEFT_DOWN, self.leftCliComponent)
        uiComponent.index = len(self.components) 
        component = Component(origin, dest, dir, id, self.GetParent().getValues(), uiComponent)
        self.components.append(component)
        self.addAvailable(origin, dest)
        self.GetParent().updateGrid(self.components)

    def closeComponent(self, event):
        component = event.GetEventObject()
        component.SetBackgroundColour("white")
        component.Refresh()

    def openComponent(self, event):
        component = event.GetEventObject()
        component.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ))
        component.Refresh()

    def leftCliComponent(self, event):
        # EDITAR
        uiElement = event.GetEventObject()
        component = self.components[uiElement.index]
        if self.GetParent().getTarget() == component.id[0]:
            component.values = self.GetParent().getValues()
            self.GetParent().updateGrid(self.components)

    """
    # ELIMINAR 
    NO ES VIABLE ELIMINAR COMPONENTES, ES MEJOR REINICIAR LA INTERFAZ
    def rightCliComponent(self, event):
        if self.selected == None:
            component = event.GetEventObject()
            x,y = component.start ; dir = component.dir
            self.matrix[x][y].neighbors[dir] = None
            x,y = component.end ; dir = self.getOpposite(dir)
            self.matrix[x][y].neighbors[dir] = None
            self.schematic.removed(component.id[0])
            self.components.pop(component.aux)
            component.Destroy()
            self.GetParent().updateGrid(self.components)
    """

    def getOpposite(self, dir):
        return OPPOSITE[dir]


    def loadOptions(self, coords):
        x, y = coords
        available = self.matrix[x][y].neighbors
        if x > 0:
            if available["up"] == None:
                self.setBitmap(self.matrix[x-1][y].interface, OPTION)  
                self.options.append((x-1, y))
            else:
                self.setBitmap(self.matrix[x-1][y].interface, OCCUPED)
                self.occupied.append((x-1, y))
        if y > 0:
            if available["left"] == None:
                self.setBitmap(self.matrix[x][y-1].interface, OPTION)
                self.options.append((x, y-1))
            else:
                self.setBitmap(self.matrix[x][y-1].interface, OCCUPED)
                self.occupied.append((x, y-1))
        if x < (self.columnas -1):
            if available["down"] == None:
                self.setBitmap(self.matrix[x+1][y].interface, OPTION)
                self.options.append((x+1, y))
            else:
                self.setBitmap(self.matrix[x+1][y].interface, OCCUPED)
                self.occupied.append((x+1, y))
        if y < (self.filas - 1):
            if available["right"] == None:
                self.setBitmap(self.matrix[x][y+1].interface, OPTION)
                self.options.append((x, y+1))
            else:
                self.setBitmap(self.matrix[x][y+1].interface, OCCUPED)
                self.occupied.append((x, y+1))

    def resetOptions(self):
        for i in self.options:
            x, y = i
            self.setBitmap(self.matrix[x][y].interface, NORMAL)
        for i in self.occupied: 
            x, y = i
            self.setBitmap(self.matrix[x][y].interface, NORMAL)
        x, y = self.selected.coords
        self.setBitmap(self.matrix[x][y].interface, NORMAL)
        self.selected = None
        self.options = []
        self.occupied = []

    def lockOptions(self, ori, dest):
        ox, oy = ori
        dx, dy = dest
        if oy > dy:
            self.matrix[ox][oy].neighbors["left"] = dest
            self.matrix[dx][dy].neighbors["right"] = ori
        elif oy < dy:
            self.matrix[ox][oy].neighbors["right"] = dest
            self.matrix[dx][dy].neighbors["left"] = ori
        elif ox > dx:
            self.matrix[ox][oy].neighbors["up"] = dest
            self.matrix[dx][dy].neighbors["down"] = ori
        elif ox < dx:
            self.matrix[ox][oy].neighbors["down"] = dest
            self.matrix[dx][dy].neighbors["up"] = ori


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
        if interface.data in self.availables or interface.data in self.options:
            if self.selected == None:
                self.setBitmap(interface, SELECTED)  
            else:
                m_pos = interface.data
                if m_pos in self.options:
                    self.setBitmap(interface, SELECTED)  

    def closeInterface(self, event):
        interface = event.GetEventObject()
        if interface.data in self.availables or interface.data in self.options:
            if self.selected == None:
                self.setBitmap(interface, NORMAL)
            else:
                m_pos = interface.data
                if m_pos in self.options:
                    self.setBitmap(interface, OPTION) 

    def validateInterface(self, coords):
        x,y = coords
        neighbors = self.matrix[x][y].neighbors
        return neighbors["up"] == None or neighbors["down"] == None or neighbors["right"] == None or neighbors["left"] == None

    def clicInterface(self, event):
        interface = event.GetEventObject()
        if interface.data in self.availables or interface.data in self.options:
            m_pos = interface.data
            if not self.validateInterface(m_pos):
                return
            if self.selected == None:
                self.loadOptions(m_pos)
                self.selected = self.matrix[m_pos[0]][m_pos[1]]
            elif m_pos in self.options:
                if self.GetParent().getTarget() != "V":
                    self.loadComponent(interface, m_pos)
        event.Skip()

    def setNodeId(self, origin, dest, manual=None):
        if self.matrix[origin[0]][origin[1]].id == None:
            self.manageNodeId(origin)
            self.manageNodeId(dest)
        elif self.matrix[dest[0]][dest[1]].id == None:
            if self.GetParent().getTarget() == "U" or manual != None:
                self.matrix[dest[0]][dest[1]].id = self.matrix[origin[0]][origin[1]].id
            else:
                self.manageNodeId(dest)

    def manageNodeId(self, coords):
        x, y = coords
        self.matrix[x][y].id = self.nodeId
        self.nodeId += 1


    def scaleImage(self, dir):
        img = wx.Image(dir)
        return img.Scale(GS, GS, wx.IMAGE_QUALITY_NORMAL)
        
    def setBitmap(self, interface, dir):
        interface.SetBitmap(wx.Bitmap(self.scaleImage(dir)))
