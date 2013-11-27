# -*- coding: utf-8 -*-
from MainFrm import *
from TaskbarIcon import *
import wx

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
        self.__tbicon = TaskBarIcon(self.__frame)
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
