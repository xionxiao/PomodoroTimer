import wx
from State import *
from R import *

class _CounterBar(wx.Window, OnStateChangeListener):
    def __init__(self, parent):
        OnStateChangeListener.__init__(self)
        wx.Window.__init__(self, parent, size=wx.Size(8,8))
        self.__sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.__sizer)
        state = State()
        state.AddListener(self)
        self.SetCallBack('WorkState', 'timeup', self.Increase)

    def __AddBlock(self, color=wx.BLUE):
        block = wx.Window(self, wx.ID_ANY, size=(8,6))
        block.SetBackgroundColour(color or wx.BLUE)
        self.__sizer.Add(block, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 1)

    def SetCount(self, count):
        self.__sizer.Clear()
        for i in range(0, count):
            self.__AddBlock()
        self.SetSizerAndFit(self.__sizer)

    def Increase(self, color=wx.BLUE):
        self.__AddBlock(color)
        self.SetSizerAndFit(self.__sizer)

class MainFrame(wx.Frame, OnStateChangeListener):
    def __init__(self):
        OnStateChangeListener.__init__(self)
        wx.Frame.__init__(self, None, title=u'番茄时钟 —— by xhui', size=(330,100),
                          style=(wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP) & #Raise User Action
                          ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        bmp = wx.BitmapFromImage(wx.ImageFromStream(R['favicon.ico'], type=wx.BITMAP_TYPE_ICO))
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(bmp)
        self.SetIcon(icon)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconify)

        self.__timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.__OnTimer, self.__timer)

        p = wx.Panel(self)
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL)
        font.SetPixelSize(wx.Size(18,32))
        self.text_box = wx.StaticText(p, -1, wx.GetApp().GetTimeLeft().Format("%M:%S"))
        self.text_box.SetFont(font)
        self.text_box.SetForegroundColour(wx.RED)

        font.SetPixelSize(wx.Size(10,20))
        self.btn_start = wx.Button(p, -1,  u"开始", size=(84,32))
        self.btn_start.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.__BtnStartDown, self.btn_start)
        self.btn_start.Enable(True)

        self.btn_stop = wx.Button(p, -1, u"结束", size=(84,32))
        self.btn_stop.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.__BtnStopDown, self.btn_stop)
        self.btn_stop.Enable(False)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        child_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_style = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL&~wx.BOTTOM
        child_sizer.Add(self.text_box, 0,sizer_style, 12)
        child_sizer.Add(self.btn_start, 0, sizer_style, 12)
        child_sizer.Add(self.btn_stop, 0,sizer_style & ~wx.LEFT, 12)
        top_sizer.Add(child_sizer, 0, wx.ALIGN_RIGHT)
        child_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__counter_bar = _CounterBar(p)
        child_sizer.Add(self.__counter_bar, 0, sizer_style, 0)
        top_sizer.Add(child_sizer, 0, wx.ALIGN_LEFT|wx.TOP, 10)
        p.SetSizer(top_sizer)

        self.__state = State()
        self.__state.AddListener(self)
        self.SetActionCallBack('start', self.__OnStateStart)
        self.SetActionCallBack('stop', self.__OnStateStop)
        self.SetActionCallBack('timeup', self.__OnStateTimeUp)

    def OnIconify(self, evt):
        self.Hide()
        evt.Skip()

    def OnClose(self, evt):
        self.Hide()
        # Prevent Exit Event
        evt.Veto()

    def __OnStateStart(self):
        time = wx.GetApp().GetTimeLeft()
        self.__timer.Start(1000)
        self.text_box.SetLabel(time.Format("%M:%S"))
        self.btn_start.Enable(False)
        self.btn_stop.Enable(True)
        self.btn_stop.SetLabel(u"中断")

    def __OnStateStop(self):
        self.__timer.Stop()
        state_name = self.__state.getState()
        time = wx.GetApp().GetWorkTimeSpan()
        self.btn_start.SetLabel(u"开始")
        self.btn_start.Enable(True)
        self.btn_stop.SetLabel(u"结束")
        self.text_box.SetForegroundColour(wx.RED)
        if state_name in ('StopState', 'IdleState'):
            self.btn_stop.Enable(False)
        elif  state_name is 'WorkState':
            self.btn_stop.Enable(True)
        elif state_name is 'RestState':
            self.btn_stop.Enable(True)
        self.text_box.SetLabel(time.Format("%M:%S"))

    def __OnStateTimeUp(self):
        self.__timer.Stop()
        state_name = self.__state.getState()
        self.btn_stop.SetLabel(u"结束")
        if state_name is 'WorkState':
            self.__OnWorkStateTimeUp()
        elif state_name is 'RestState':
            self.__OnRestStateTimeUp()
        elif state_name is 'IdleState':
            self.__OnIdleStateTimeUp()
        self.__PopUp()

    def __OnWorkStateTimeUp(self):
        time = wx.GetApp().GetRestTimeSpan()
        self.text_box.SetLabel(time.Format("%M:%S"))
        self.text_box.SetForegroundColour(wx.BLUE)
        self.btn_start.SetLabel(u"休息")
        self.btn_start.Enable(True)
        self.btn_stop.Enable(True)
        

    def __OnRestStateTimeUp(self):
        time = wx.GetApp().GetWorkTimeSpan()
        self.text_box.SetLabel(time.Format("%M:%S"))
        self.text_box.SetForegroundColour(wx.RED)
        self.btn_start.SetLabel(u"开始")
        self.btn_start.Enable(True)
        self.btn_stop.Enable(True)

    def __OnIdleStateTimeUp(self):
        time = wx.GetApp().GetWorkTimeSpan()
        self.text_box.SetLabel(time.Format("%M:%S"))
        self.text_box.SetForegroundColour(wx.RED)
        self.btn_start.SetLabel(u"开始")
        self.btn_start.Enable(True)
        self.btn_stop.Enable(True)
        

    def SetCount(self, count):
        self.__counter_bar.SetCount(count)

    # Popup main frame
    def __PopUp(self):
        if self.IsIconized():
            self.Iconize(False)
        if not self.IsShown():
            self.Show()
        self.Raise()

    # Timer tick
    def __OnTimer(self, evt):
        time = wx.GetApp().GetTimeLeft()
        self.text_box.SetLabel(time.Format("%M:%S"))

    def __BtnStartDown(self, evt):
        self.__state.Start()

    def __BtnStopDown(self, evt):
        self.__state.Stop()