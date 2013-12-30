import wx
from R import *

class _CounterBar(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, size=wx.Size(8,8))
        self.__sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.__sizer)

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

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u'番茄时钟 —— by xhui', size=(330,100),
                          style=(wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP) & #Raise User Action
                          ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        bmp = wx.BitmapFromImage(wx.ImageFromStream(R['favicon.ico'], type=wx.BITMAP_TYPE_ICO))
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(bmp)
        self.SetIcon(icon)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconify)
        
        p = wx.Panel(self)
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.NORMAL)
        font.SetPixelSize(wx.Size(18,32))
        self.text_box = wx.StaticText(p, -1, "25:00")
        self.text_box.SetFont(font)
        self.text_box.SetForegroundColour(wx.RED)

        font.SetPixelSize(wx.Size(10,20))
        self.btn_start = wx.Button(p, -1,  u"开始", size=(84,32))
        self.btn_start.SetFont(font)
        self.Bind(wx.EVT_BUTTON, wx.GetApp().StartTask, self.btn_start)
        self.btn_start.Enable(True)
        
        self.btn_stop = wx.Button(p, -1, u"停止", size=(84,32))
        self.btn_stop.SetFont(font)
        self.Bind(wx.EVT_BUTTON, wx.GetApp().StopTask, self.btn_stop)
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

    def OnIconify(self, evt):
        self.Hide()
        evt.Skip()

    def OnClose(self, evt):
        self.Hide()
        # Prevent Exit Event
        evt.Veto()

    def SetCount(self, count):
        self.__counter_bar.SetCount(count)
        
    def OnStartTask(self, evt):
        time = wx.GetApp().GetTimeLeft()
        self.__timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.__OnTimer, self.__timer)
        self.__timer.Start(1000)
        self.text_box.SetLabel(time.Format("%M:%S"))
        self.btn_start.Enable(False)
        self.btn_stop.Enable(True)
        
    def OnStopTask(self, evt):
        time = wx.GetApp().GetTimeLeft()
        self.__timer.Stop()
        if time.IsPositive():
            # more than 1 minite mark as cancel and set conter_bar block red
            if (time < wx.TimeSpan(0,1)):
                self.__counter_bar.Increase(wx.RED)
            self.text_box.SetLabel(time.Format("%M:%S"))
        else:
            self.__counter_bar.Increase()
            self.text_box.SetLabel(time.Format("00:00"))
        self.btn_start.Enable(True)
        self.btn_stop.Enable(False)
        
    def __OnTimer(self, evt):
        time = wx.GetApp().GetTimeLeft()
        self.text_box.SetLabel(time.Format("%M:%S"))
