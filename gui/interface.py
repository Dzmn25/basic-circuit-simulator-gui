# -*- coding: utf-8 -*-

import wx
import wx.xrc
from gui.board import Board

###########################################################################
## Class Interface
###########################################################################

class Interface ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Simulación de circuitos", pos = wx.DefaultPosition, size = wx.Size( 750,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 233, 233, 233 ) )

        bLayout = wx.BoxSizer( wx.HORIZONTAL )

        bUtils = wx.BoxSizer( wx.VERTICAL )


        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.rbtnVoltaje = wx.RadioButton( self, wx.ID_ANY, u"Voltaje - V", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnVoltaje, 0, wx.ALL, 5 )

        self.rbtnResistencia = wx.RadioButton( self, wx.ID_ANY, u"Resistencia - R", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnResistencia, 0, wx.ALL, 5 )

        self.rbtnInductor = wx.RadioButton( self, wx.ID_ANY, u"Inductor - L", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnInductor, 0, wx.ALL, 5 )

        self.rbtnCapacitor = wx.RadioButton( self, wx.ID_ANY, u"Capacitor - C", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnCapacitor, 0, wx.ALL, 5 )

        self.rbtnTloc = wx.RadioButton( self, wx.ID_ANY, u"TLOC - O", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnTloc, 0, wx.ALL, 5 )

        self.rbtnTlin = wx.RadioButton( self, wx.ID_ANY, u"TLIN - N", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnTlin, 0, wx.ALL, 5 )

        self.rbtnTlsc = wx.RadioButton( self, wx.ID_ANY, u"TLSC - G", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnTlsc, 0, wx.ALL, 5 )

        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.lblCoords = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.lblCoords.Wrap( -1 )

        bUtils.Add( self.lblCoords, 0, wx.ALL|wx.EXPAND, 5 )

        self.btnCalcular = wx.Button( self, wx.ID_ANY, u"Calcular", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btnCalcular.SetFont( wx.Font( 13, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

        bUtils.Add( self.btnCalcular, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bLayout.Add( bUtils, 0, wx.EXPAND, 5 )

        bMap = wx.BoxSizer( wx.VERTICAL )

        self.pChart = Board(self)
        bMap.Add( self.pChart, 1, wx.EXPAND |wx.ALL, 5 )

        bLayout.Add( bMap, 1, wx.EXPAND, 5 )

        self.SetSizer( bLayout )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.rbtnVoltaje.Bind( wx.EVT_RADIOBUTTON, self.OnBtnVoltaje )
        self.rbtnResistencia.Bind( wx.EVT_RADIOBUTTON, self.OnBtnResistencia )
        self.rbtnInductor.Bind( wx.EVT_RADIOBUTTON, self.OnBtnInductor )
        self.rbtnCapacitor.Bind( wx.EVT_RADIOBUTTON, self.OnBtnCapacitor )
        self.btnCalcular.Bind( wx.EVT_BUTTON, self.OnCalcular )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnBtnVoltaje( self, event ):
        event.Skip()

    def OnBtnResistencia( self, event ):
        event.Skip()

    def OnBtnInductor( self, event ):
        event.Skip()

    def OnBtnCapacitor( self, event ):
        event.Skip()

    def OnCalcular( self, event ):
        event.Skip()