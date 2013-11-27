# -*- coding: utf-8 -*-
from MainFrm import *
import wx

class _TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame=None):
        wx.TaskBarIcon.__init__(self)
        icon = wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO)
        self.__frame = frame
        self.SetIcon(icon, u"番茄时钟")
        self.__menu = self.CreatePopupMenu()
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnTaskBarRight)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, u"打开")
        self.Bind(wx.EVT_MENU, self.OnTaskBarLeftDClick, item)
        item = menu.Append(wx.ID_ANY, u"开始计时")
        self.Bind(wx.EVT_MENU, wx.GetApp().StartTask, item)
        item = menu.Append(wx.ID_ANY, u"停止计时")
        item.Enable(False)
        self.Bind(wx.EVT_MENU, wx.GetApp().StopTask, item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_ANY, u"退出")
        self.Bind(wx.EVT_MENU, self.OnClose, item)
        return menu

    def OnStartTask(self, evt):
        self.ShowBalloon("", u"番茄钟开始计时")
        self.__menu.FindItemByPosition(1).Enable(False)
        self.__menu.FindItemByPosition(2).Enable(True)

    def OnStopTask(self, evt):
        self.ShowBalloon("", u"番茄钟停止")
        self.__menu.FindItemByPosition(1).Enable(True)
        self.__menu.FindItemByPosition(2).Enable(False)
        
    def OnTaskBarRight(self, evt):
        self.PopupMenu(self.__menu)

    def OnTaskBarLeftDClick(self, evt):
        if self.__frame.IsIconized():
            self.__frame.Iconize(False)
        if not self.__frame.IsShown():
            self.__frame.Show()
        else:
            self.__frame.Hide()
        self.__frame.Raise()

    def OnClose(self, evt):
        self.__frame.Destroy()
        self.RemoveIcon()
        self.Destroy()
        
class TimerApp(wx.App):
    # Work for every 25 min
    __work_time = wx.TimeSpan(0,25)
    # Rest for 5 min, not used by now
    __rest_time = wx.TimeSpan(0,5)
    # 任务开始时间
    __start_time = None

    def __init__(self):
        wx.App.__init__(self, False)
        # Init main frame
        self.__frame = MainFrame()
        self.SetTopWindow(self.__frame)
        self.__frame.Center()
        self.__frame.Show()
        # Init taskbar icon
        self.__tbicon = _TaskBarIcon(self.__frame)
        # Init timer
        self.__timer = wx.Timer()
        self.Bind(wx.EVT_TIMER, self.__OnTimer, self.__timer)

    def __OnTimer(self, evt):
        # self.__timespan.Subtract(wx.TimeSpan.Second())
        self.StopTask(evt)
    
    def StartTask(self, evt):
        self.__timer.Start(self.__work_time.GetMilliseconds(), True)
        self.__start_time = wx.DateTime.Now()
        self.__frame.OnStartTask(evt)
        self.__tbicon.OnStartTask(evt)
        self.__PlaySound('HmReadyToWork.wav')
        print('+' + str(self.__start_time))

    def StopTask(self, evt):
        self.__timer.Stop()
        self.__frame.OnStopTask(evt)
        self.__tbicon.OnStopTask(evt)
        self.__PlaySound('HmJobsDone.wav')
        print('-' + str(wx.DateTime().Now()))

    # Get left time
    # Return type: wx.TimeSpan -- positive for time left
    #                             nagative for time is up
    def GetTimeLeft(self):
        timeleft = self.__work_time - (wx.DateTime.Now()-self.__start_time)
        return timeleft
    
    def __PlaySound(self, name=None):
        if not name:
            soundFile = 'REMINDER.WAV'
        else:
            soundFile = name
        sound = wx.Sound(soundFile)
        sound.Play(wx.SOUND_ASYNC)
