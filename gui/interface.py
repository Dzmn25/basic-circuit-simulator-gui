# -*- coding: utf-8 -*-

import wx
import wx.xrc
import wx.grid
from gui.board import Board

###########################################################################
## Class Interface
###########################################################################

class Interface ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Simulación de circuitos", 
                           pos = wx.DefaultPosition, 
                           size = wx.Size( 1100, 700 ), 
                           style = wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX )

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

        self.rbtnConector = wx.RadioButton( self, wx.ID_ANY, u"Conector", wx.DefaultPosition, wx.DefaultSize, 0 )
        bUtils.Add( self.rbtnConector, 0, wx.ALL, 5 )

        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.lblValue1 = wx.StaticText( self, wx.ID_ANY, u"Valor 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblValue1.Wrap( -1 )

        bUtils.Add( self.lblValue1, 0, wx.ALL|wx.EXPAND, 5 )

        bForm1 = wx.BoxSizer( wx.HORIZONTAL )

        self.bxUnit1 = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0)
        bForm1.Add( self.bxUnit1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.lblUnit1 = wx.StaticText( self, wx.ID_ANY, u"v", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblUnit1.Wrap( -1 )

        bForm1.Add( self.lblUnit1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bUtils.Add( bForm1, 0, wx.EXPAND, 5 )

        self.lblValue2 = wx.StaticText( self, wx.ID_ANY, u"Valor 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblValue2.Wrap( -1 )

        bUtils.Add( self.lblValue2, 0, wx.ALL, 5 )

        bForm2 = wx.BoxSizer( wx.HORIZONTAL )

        self.bxUnit2 = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bxUnit2.Disable()
        bForm2.Add( self.bxUnit2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.lblUnit2 = wx.StaticText( self, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblUnit2.Wrap( -1 )

        bForm2.Add( self.lblUnit2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bUtils.Add( bForm2, 1, wx.EXPAND, 5 )

        self.lblValue3 = wx.StaticText( self, wx.ID_ANY, u"Valor 3", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblValue3.Wrap( -1 )

        bUtils.Add( self.lblValue3, 0, wx.ALL, 5 )

        bForm3 = wx.BoxSizer( wx.HORIZONTAL )

        self.bxUnit3 = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bxUnit3.Disable()
        bForm3.Add( self.bxUnit3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        frecuencyChoices = [ u"KHz", u"MHz", u"GHz" ]
        self.frecuency = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, frecuencyChoices, 0 )
        self.frecuency.SetSelection( 0 )
        self.frecuency.Disable()
        bForm3.Add( self.frecuency, 0, wx.ALL, 5 )

        bUtils.Add( bForm3, 1, wx.EXPAND, 5 )


        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bButtons = wx.BoxSizer( wx.HORIZONTAL )

        self.btnReset = wx.Button( self, wx.ID_ANY, u"Limpiar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bButtons.Add( self.btnReset, 0, wx.ALL, 5 )

        self.btnNetlist = wx.Button( self, wx.ID_ANY, u"Netlist", wx.DefaultPosition, wx.DefaultSize, 0 )
        bButtons.Add( self.btnNetlist, 0, wx.ALL, 5 )

        self.btnMatlab = wx.Button( self, wx.ID_ANY, u"Matlab", wx.DefaultPosition, wx.DefaultSize, 0 )
        bButtons.Add( self.btnMatlab, 0, wx.ALL, 5 )


        bUtils.Add( bButtons, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.gridValues = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.gridValues.CreateGrid( 50, 4 )
        self.gridValues.EnableEditing( False )
        self.gridValues.EnableGridLines( True )
        self.gridValues.EnableDragGridSize( False )
        self.gridValues.SetMargins( 0, 0 )

        # Columns
        self.gridValues.SetColSize( 0, 30 )
        self.gridValues.SetColSize( 1, 90 )
        self.gridValues.SetColSize( 2, 90 )
        self.gridValues.SetColSize( 3, 90 )
        self.gridValues.EnableDragColMove( False )
        self.gridValues.EnableDragColSize( True )
        self.gridValues.SetColLabelValue( 0, u"ID" )
        self.gridValues.SetColLabelValue( 1, u"1" )
        self.gridValues.SetColLabelValue( 2, u"2" )
        self.gridValues.SetColLabelValue( 3, u"3" )
        self.gridValues.SetColLabelSize( 20 )
        self.gridValues.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.gridValues.EnableDragRowSize( False )
        self.gridValues.SetRowLabelSize( 0 )
        self.gridValues.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.gridValues.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        self.gridValues.SetMinSize( wx.Size( 330,100 ) )
        self.gridValues.SetMaxSize( wx.Size( 330,100 ) )

        bUtils.Add( self.gridValues, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bLayout.Add( bUtils, 0, wx.EXPAND, 5 )

        bUtils.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bMap = wx.BoxSizer( wx.VERTICAL )

        self.pChart = Board(self)
        bMap.Add( self.pChart, 1, wx.EXPAND |wx.ALL, 5 )

        bLayout.Add( bMap, 1, wx.EXPAND, 5 )

        self.SetSizer( bLayout )
        self.Layout()

        self.Centre( wx.BOTH )

        self.target = 'V'

        # Connect Events
        self.rbtnVoltaje.Bind( wx.EVT_RADIOBUTTON, self.OnBtnVoltaje )
        self.rbtnResistencia.Bind( wx.EVT_RADIOBUTTON, self.OnBtnResistencia )
        self.rbtnInductor.Bind( wx.EVT_RADIOBUTTON, self.OnBtnInductor )
        self.rbtnCapacitor.Bind( wx.EVT_RADIOBUTTON, self.OnBtnCapacitor )
        self.rbtnTlin.Bind(wx.EVT_RADIOBUTTON, self.OnBtnTlin )
        self.rbtnTloc.Bind(wx.EVT_RADIOBUTTON, self.OnBtnTloc )
        self.rbtnTlsc.Bind(wx.EVT_RADIOBUTTON, self.OnBtnTlsc )
        self.rbtnConector.Bind(wx.EVT_RADIOBUTTON, self.OnBtnConector )
        self.btnNetlist.Bind( wx.EVT_BUTTON, self.OnNetlist )
        self.btnReset.Bind( wx.EVT_BUTTON, self.OnReset )
        self.btnMatlab.Bind( wx.EVT_BUTTON, self.OnMatlab )
        self.pChart.Bind(wx.EVT_CHAR, self.onCancel)
        self.Bind(wx.EVT_CHAR, self.onCancel)

    def __del__( self ):
        pass

    def getTarget(self):
        return self.target
    
    def getValues(self):
        frecuencyChoices = [ u"KHz", u"MHz", u"GHz" ]
        values = []
        if self.getTarget() == 'N' or self.getTarget() == 'G' or self.getTarget() == 'O':
            values.append( ( float( self.bxUnit1.GetValue() ) , self.lblUnit1.GetLabelText() ) )
            values.append( ( float( self.bxUnit2.GetValue() ) , self.lblUnit2.GetLabelText() ) )
            values.append( ( float( self.bxUnit3.GetValue() ) , str(frecuencyChoices[self.frecuency.GetSelection()]) ) )
            return values
        else:
            values.append( ( float( self.bxUnit1.GetValue() ) , self.lblUnit1.GetLabelText() ) )
            return values
    
    def addComponent(self, id, values, pos):
        if len(values) == 1:
            self.gridValues.SetCellValue(pos, 0, id)
            self.gridValues.SetCellValue(pos, 1, str(values[0][0]) + str(values[0][1]) )
        elif len(values) == 3:
            self.gridValues.SetCellValue(pos, 0, id)
            self.gridValues.SetCellValue(pos, 1, str(values[0][0]) + str(values[0][1]) )
            self.gridValues.SetCellValue(pos, 2, str(values[1][0]) + str(values[1][1]))
            self.gridValues.SetCellValue(pos, 3, str(values[2][0]) + str(values[2][1]))

    def updateGrid(self, componentes):
        aux = 0
        self.gridValues.ClearGrid()
        for i in componentes:
            if i.id != " ":
                self.addComponent(i.id, i.values, aux)
                aux += 1
    
    def clearEntry(self, values):
        self.lblUnit1.SetLabelText(values[0])
        if len(values) == 3:
            self.lblValue1.SetLabelText("valor - Z") ; self.lblValue2.SetLabelText("Angulo - E") ; self.lblValue3.SetLabelText("Frecuencia - F")
            self.bxUnit2.Enable() ; self.lblUnit2.SetLabelText(values[1])
            self.bxUnit3.Enable() ; self.frecuency.Enable()
        else:
            self.lblValue1.SetLabelText("Valor:") ; self.lblValue2.SetLabelText("") ; self.lblValue3.SetLabelText("")
            self.bxUnit2.Disable() ; self.lblUnit2.SetLabelText(u"N/A")
            self.bxUnit3.Disable() ; self.frecuency.Disable() ; self.frecuency.SetSelection(0)
        pass


    # Virtual event handlers, override them in your derived class
    def OnBtnTlin(self, event):
        self.target = 'N'
        self.clearEntry([u"Ω", u"°", u"GHz"])
        event.Skip()

    def OnBtnTloc(self, event):
        self.target = 'O'
        self.clearEntry([u"Ω", u"°", u"GHz"])
        event.Skip()

    def OnBtnTlsc(self, event):
        self.target = 'G'
        self.clearEntry([u"Ω", u"°", u"GHz"])
        event.Skip()

    def OnBtnVoltaje( self, event ):
        self.target = 'V'
        self.clearEntry([u"v"])
        event.Skip()

    def OnBtnResistencia( self, event ):
        self.target = 'R'
        self.clearEntry([u"Ω"])
        event.Skip()

    def OnBtnInductor( self, event ):
        self.target = 'L'
        self.clearEntry([u"H"])
        event.Skip()

    def OnBtnCapacitor( self, event ):
        self.target = 'C'
        self.clearEntry([u"F"])
        event.Skip()

    def OnBtnConector(self, event):
        self.target = 'U'
        event.Skip()

    def OnNetlist( self, event ):
        self.pChart.printNetlist()
        event.Skip()

    def OnReset(self, event):
        self.pChart.clean()
        event.Skip()

    def OnMatlab(self, event):
        event.Skip()

    def onCancel(self, event):
        key = event.GetKeyCode()
        if key == 27:
            self.pChart.Cancel()