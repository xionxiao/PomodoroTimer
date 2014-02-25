# -*- coding: utf-8 -*-
from MainFrm import *
from TaskbarIcon import *
import wx
import sqlite3
from R import *
from State import *

class TimerApp(wx.App, OnStateChangeListener):
    # Work for every 25 min
    __work_time = wx.TimeSpan(0,25,0)
    # Rest for 5 min, not used by now
    __rest_time = wx.TimeSpan(0,5,0)
    # Idle time notify span
    __idle_time_notify = wx.TimeSpan(0,5,0)
    # 任务开始时间
    __start_time = None

    def __init__(self):
        # change order of __init__ call
        # wx.App.__init__ calls OnInit before OnStateChangeListener __init__
        OnStateChangeListener.__init__(self)
        wx.App.__init__(self)
         
    # override
    def OnInit(self):
        Prevent multiple instance of the program
        self.name = "PomodoroTimer-%s" % wx.GetUserId()
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox(u"已有一个程序实例在运行。", "ERROR")
            return False

        # Init State Object, State is Singleton, so call State() will get same object
        self.__state = State()
        self.__state.AddListener(self)
        self.SetActionCallBack('start', self.__OnStateStart)
        self.SetActionCallBack('stop', self.__OnStateStop)
        self.SetActionCallBack('timeup', self.__OnStateTimeUp)
        
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

    def __OnStateStart(self):
        self.__timer.Stop()
        state_name = self.__state.getState()
        if state_name is 'RestState':
            self.__timer.Start(self.__rest_time.GetMilliseconds(), True)
            self.__start_time = wx.DateTime.Now()
            self.__PlaySound('REMINDER.WAV')
        else: # workstate, idlestate and stopstate
            self.__timer.Start(self.__work_time.GetMilliseconds(), True)
            self.__start_time = wx.DateTime.Now()
            self.__PlaySound('HmReadyToWork.wav')

    def __OnStateStop(self):
        self.__timer.Stop()
        self.__PlaySound('REMINDER.WAV')
        state_name = self.__state.getState()
        if state_name in ('WorkState','RestState'):
            self.__timer.Start(self.__idle_time_notify.GetMilliseconds(), True)

    def __OnStateTimeUp(self):
        self.__timer.Stop()
        state_name = self.__state.getState()
        if state_name is 'WorkState':
            end_time = wx.DateTime.Now()
            self.__PlaySound('HmJobsDone.wav')
            # insert worktime to database
            c = self.__conn.cursor()
            t = (self.__start_time.FormatISODate(), 
                 self.__start_time.FormatISOTime(), 
                 end_time.FormatISOTime())
            c.execute("insert into timer values(?,?,?,'done')", t)
            self.__conn.commit()
            c.close() 
        elif state_name is 'RestState':
            self.__PlaySound('REMINDER.WAV')
        elif state_name is 'IdleState':
            self.__PlaySound('REMINDER.WAV')
        # For RestState, if timeup, RestState will change to IdleState
        self.__timer.Start(self.__idle_time_notify.GetMilliseconds(), True)

    # override
    def OnExit(self):
        self.__timer.Stop()
        self.__conn.close()
        
    def __OnTimer(self, evt):
        self.__state.TimeUp()
        
    # Get left time
    # Return type: wx.TimeSpan
    def GetTimeLeft(self):
        timeleft = wx.TimeSpan(0,0)
        state_name = self.__state.getState()
        if state_name is 'WorkState':
            timeleft = self.__work_time - (wx.DateTime.Now()-self.__start_time)
        elif state_name is 'RestState':
            timeleft = self.__rest_time - (wx.DateTime.Now()-self.__start_time)
        elif state_name is 'IdleState':
            timeleft = self.__work_time - (wx.DateTime.Now()-self.__start_time)
        elif state_name is 'StopState':
            timeleft = self.__work_time
        return timeleft

    def GetWorkTimeSpan(self):
        return self.__work_time

    def GetRestTimeSpan(self):
        return self.__rest_time

    def GetIdleNotifyTimeSpan(self):
        return self.__idle_time_notify

    def __PlaySound(self, name=None):
        if not name:
            soundFile = 'REMINDER.WAV'
        else:
            soundFile = name
        sound = wx.Sound()
        sound.CreateFromData(R[soundFile].read())
        sound.Play(wx.SOUND_ASYNC)

if __name__ == '__main__':
    app = TimerApp()
    app.MainLoop()
