# -*- coding: utf-8 -*-
import wx
import logging
from State import *
from R import *

class TaskBarIcon(wx.TaskBarIcon, OnStateChangeListener):
    def __init__(self, frame=None):
        OnStateChangeListener.__init__(self)
        wx.TaskBarIcon.__init__(self)
        #icon = wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO)
        icon = wx.EmptyIcon()
        bmp = wx.BitmapFromImage(wx.ImageFromStream(R['favicon.ico'], type=wx.BITMAP_TYPE_ICO))
        icon.CopyFromBitmap(bmp)
        self.__frame = frame
        self.SetIcon(icon, u"番茄时钟")
        self.__menu = self.CreatePopupMenu()
        # Popup menu when right click
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.__OnTaskBarRight)
        # Open mainframe when double click
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.__OnTaskBarLeftDClick)
        self.__state = State()
        self.__state.AddListener(self)
        self.SetActionCallBack('start', self.__OnStateStart)
        self.SetActionCallBack('stop', self.__OnStateStop)
        self.SetCallBack('IdleState', 'timeup', self.__OnIdleStateTimeUp)

    # override function
    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, u"打开")
        self.Bind(wx.EVT_MENU, self.__OnTaskBarLeftDClick, item)
        item = menu.Append(wx.ID_ANY, u"开始计时")
        self.Bind(wx.EVT_MENU, self.__OnPopupMenuStartDown, item)
        item = menu.Append(wx.ID_ANY, u"停止计时")
        item.Enable(False)
        self.Bind(wx.EVT_MENU, self.__OnPopupMenuStopDown, item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_ANY, u"退出")
        self.Bind(wx.EVT_MENU, self.__OnClose, item)
        return menu

    def __OnIdleStateTimeUp(self):
        notify = (u"懒货，该干活了！",
            u"发奋吧，少年！",
            u"是该做点什么了-.-!"
            )
        t = wx.DateTime().Now().GetSecond()
        self.ShowBalloon("", notify[t%3])

    def __OnStateStart(self):
        self.ShowBalloon("", u"番茄钟开始计时")
        self.__menu.FindItemByPosition(1).Enable(False)
        self.__menu.FindItemByPosition(2).Enable(True)

    def __OnStateStop(self):
        self.ShowBalloon("", u"番茄钟停止")
        self.__menu.FindItemByPosition(1).Enable(True)
        self.__menu.FindItemByPosition(2).Enable(False)

    def __OnPopupMenuStartDown(self, evt):
        self.__state.Start()

    def __OnPopupMenuStopDown(self, evt):
        self.__state.Stop()
        
    def __OnTaskBarRight(self, evt):
        if not self.__frame.IsShown():
            self.__menu.FindItemByPosition(0).SetItemLabel(u"打开")
        else:
            self.__menu.FindItemByPosition(0).SetItemLabel(u"隐藏")
        self.PopupMenu(self.__menu)

    def __OnTaskBarLeftDClick(self, evt):
        if self.__frame.IsIconized():
            self.__frame.Iconize(False)
        if not self.__frame.IsShown():
            self.__frame.Show()
        else:
            self.__frame.Hide()
        self.__frame.Raise()

    def __OnClose(self, evt):
        self.__frame.Destroy()
        self.RemoveIcon()
        self.Destroy()
        
