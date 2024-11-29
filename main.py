# -*- coding: utf-8 -*-

import wx
from gui.interface import Interface

app = wx.App(False)
frame = Interface(None)
frame.Show()
app.MainLoop()