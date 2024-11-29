# -*- coding: utf-8 -*-

import wx
import matplotlib
import numpy as np
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx
import math

class Chart(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self,parent)
        self.ranges = {}
        self.dataset = {'x1': [], 'x2': [], 'pattern': []}
        self.SetRanges(-2,2)
        self.Plot()
        self.DoLayout()   

    def Append(self, x1, x2, pattern):
        self.dataset['x1'].append(x1)
        self.dataset['x2'].append(x2)
        self.dataset['pattern'].append(pattern) 

    def SetRanges(self, max, min):
        self.ranges['max'] = max
        self.ranges['min'] = min

    def ConfLimites(self):
        self.axes.set_xlim(self.ranges['min'],self.ranges['max'])
        self.axes.set_ylim(self.ranges['min'],self.ranges['max'])
        self.axes.grid('on')

    def Plot(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.ConfLimites()
        self.figure.subplots_adjust(0.076, 0.186, 0.871,0.971,0.2,0.2)
        self.figure.canvas.mpl_connect("button_press_event", self.handleEvent)
        self.figure.canvas.mpl_connect('motion_notify_event',self.motionHover)
        self.canvas = FigureCanvas(self,-1,self.figure)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()

    # Función para calcular la distancia entre dos puntos
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def motionHover(self, event):
        """if event.xdata != None:
            self.Parent.lblCoords.SetLabelText("x= "+str(round(event.xdata,2))+"  y= "+str(round(event.ydata,2)))"""
        if event.inaxes:
        # Obtener la posición del mouse
            mouse_pos = (event.xdata, event.ydata)
        
            # Buscar el vértice más cercano
            nearest_vertex = None
            min_dist = float('inf')
            
            for xi in self.figure.get_axes.x:
                for yi in self.figure.get_axes.y:
                    vertex = (xi, yi)
                    dist = self.distance(mouse_pos, vertex)
                    
                    if dist < min_dist:
                        min_dist = dist
                        nearest_vertex = vertex
            
            # Si el mouse está cerca del vértice, dibujar un punto
            if min_dist < 0.1:
                # Dibujar solo el punto rojo cerca del vértice
                self.DrawDot(nearest_vertex[0], nearest_vertex[1])  # Dibujar un punto rojo en el vértice
                self.figure.canvas.draw_idle()  # Redibujar la figura para mostrar el punto

    def handleEvent(self, event):
        if event.xdata != None:
            value = 1 if event.button == 1 else 0
            x = round(event.xdata,2)
            y = round(event.ydata,2)
            self.Append(x, y, value)
            self.DrawDot(x, y, value)
            self.RedrawLine()
            self.figure.canvas.draw_idle()

    def DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas,1,wx.LEFT | wx.TOP | wx.GROW)
        sizer.Add(self.toolbar,0,wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

    def DrawDot(self, x, y, value):
        color = 'b' if (value == 1) else 'r'
        self.axes.plot(x, y, "."+color)

    def Reset(self):
        self.Clear()
        self.dataset = {'x1': [], 'x2': [], 'pattern': []}
        self.Parent.UpdateTable("", "", "", "")
        self.figure.canvas.draw_idle()

    def Clear(self):
        self.axes.clear()
        self.ConfLimites()

    def DrawLine(self, w1, w2, b):
        self.axes.plot([-2, 2],[(1/w2) * (-w1*(-2)-b), (1*w2) * (-w1*2-b)], '--g', label="Neurona")
        self.axes.legend(loc = 'best')
        self.figure.canvas.draw_idle()

    
    """def Classification(self):
        neurona = Adaline(2,0.4, 0)
        neurona.AssociateChart(self)
        x = np.array([self.dataset['x1'], self.dataset['x2']])
        y = np.array(self.dataset['pattern'])
        neurona.train(x,y)"""

    def RedrawLine(self):
        for i in self.axes.get_lines():
            if i.get_label() == "Neurona":
                i.remove()