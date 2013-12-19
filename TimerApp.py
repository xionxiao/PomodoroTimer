# -*- coding: utf-8 -*-
from MainFrm import *
from TaskbarIcon import *
import wx
import sqlite3

class TimerApp(wx.App):
    # Work for every 25 min
    __work_time = wx.TimeSpan(0,25)
    # Rest for 5 min, not used by now
    __rest_time = wx.TimeSpan(0,5)
    # 任务开始时间
    __start_time = None

    # override
    def OnInit(self):
        # Prevent multiple instance of the program
        self.name = "PomodoroTimer-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox(u"已有一个程序实例在运行。", "ERROR")
            return False
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
        # Create database
        self.__conn = sqlite3.connect('timer.db')
        c = self.__conn.cursor()
        c.execute('''create table if not exists timer
                  (date text, start_time text,
                  end_time text, status text)''')
        c.execute('''select count(date) from timer
                   where date = "%s"''' % wx.DateTime.Now().FormatISODate())
        count = c.fetchone()[0]
        self.__frame.SetCount(count)
        self.__conn.commit()
        c.close()
        return True

    # override
    def OnExit(self):
        self.__conn.close()
        
    def __OnTimer(self, evt):
        end_time = wx.DateTime.Now()
        self.StopTask(evt)
        if self.__frame.IsIconized():
            self.__frame.Iconize(False)
        if not self.__frame.IsShown():
            self.__frame.Show()
        self.__frame.Raise()
        c = self.__conn.cursor()
        t = (self.__start_time.FormatISODate(),
             self.__start_time.FormatISOTime(),
             end_time.FormatISOTime())
        c.execute("insert into timer values(?,?,?,'done')", t)
        self.__conn.commit()
        c.close()
    
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

