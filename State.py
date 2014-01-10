# -*- coding: utf-8 -*-
from Singleton import *

class OnStateChangeListener:
    __lt = {}
    __state = {'WorkState', 'IdleState', 'RestState', 'InterruptState'}
    __action = ['start', 'stop', 'timeup']
    def __init__(self):
        for i in self.__state:
            self.__lt[i] = {}
            for j in self.__action:
                self.__lt[i][j] = None

    def __getitem__(self, name):
        return self.__lt[name]

    def OnStateChange(self, state, action):
        func = self.__lt[state.__class__.__name__][action]
        func and func()

    def SetCallBack(self, state, action, func):
        if not action in self.__action:
            # Todo: need new method for add callback functions
            #       state and action could be list
            if not [item for item in action if item in self.__action]:
                return
        if isinstance(state, _State):
            self.__lt[state.__class__.__name__][action] = func
        elif type(state) == str and state in self.__state:
            self.__lt[state][action] = func

class _State(Singleton):
    _current = None
    def __init__(self):
        self.__listener = []
    def Start(self):
        pass
    def Stop(self):
        pass
    def TimeUp(self):
        pass
    def AddListener(self, l):
        self.__listener.append(l)
    def Update(self, action):
        for i in self.__listener:
            i.OnStateChange(self, action)

# Proxy State class
class State(_State):
    def getName(self):
        return self._current.__class__.__name__

    def getLastState(self):
        return

    def getLastAction(self):
        return None

    def Start(self):
        if not _State._current:
            _State._current = WorkState()
        _State._current.Update('start')
        _State._current.Start()
    def Stop(self):
        if _State._current:
            _State._current.Update('stop')
            _State._current.Stop()
    def TimeUp(self):
        if _State._current:
            _State._current.Update('timeup')
            _State._current.TimeUp()
    def AddListener(self, l):
        WorkState().AddListener(l)
        IdleState().AddListener(l)
        RestState().AddListener(l)
        InterruptState().AddListener(l)

class IdleState(_State):
    def Start(self):
        _State._current = WorkState()
        _State._current.Start()
    def TimeUp(self):
        ''' 在日历，或者定时任务到来时提醒 '''
        pass

class WorkState(_State):
    def Start(self):
        # set timer and start timer
        # register TimeUp() to timer
        pass
    def TimeUp(self):
        _State._current = RestState()
    def Stop(self):
        # close timer
        _State._current = InterruptState()
        pass

class RestState(_State):
    def Start(self):
        _State._current = WorkState()
        pass
    def TimeUp(self):
        # reset timer
        pass
    def Stop(self):
        _State._current = IdleState()
        pass

class InterruptState(_State):
    def Start(self):
        _State._current = WorkState()
        pass
    def Stop(self):
        _State._current = IdleState()
        pass
    def TimeUp(self):
        # reset timer
        pass
