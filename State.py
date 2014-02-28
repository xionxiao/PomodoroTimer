# -*- coding: utf-8 -*-
from Singleton import *
import logging

class OnStateChangeListener:
    __state = {'WorkState', 'IdleState', 'RestState', 'StopState'}
    __action = ['start', 'stop', 'timeup']

    def __init__(self):
        self.__lt = {}
        for i in self.__state:
            self.__lt[i] = {}
            for j in self.__action:
                self.__lt[i][j] = None
    
    #def __getitem__(self, name):
    #    return self.__lt[name]

    def OnStateChange(self, state, action):
        if action in self.__action:
            func = self.__lt[state.__class__.__name__][action]
            func and func()

    def SetCallBack(self, state, action, func):
        if not hasattr(func, '__call__'):
            return
        if not action in self.__action:
            # Todo: need new method for add callback functions
            #       state and action could be list
            if not [item for item in action if item in self.__action]:
                return
        if isinstance(state, _State):
            self.__lt[state.__class__.__name__][action] = func
        elif type(state) == str and state in self.__state:
            self.__lt[state][action] = func

    def SetStateCallBack(self, state, func):
        if isinstance(state, _State):
            for a in self.__action:
                self.SetCallBack(state, a, func)

    def SetActionCallBack(self, action, func):
        if action in self.__action:
            for s in self.__state:
                self.SetCallBack(s, action, func)

    def _PrintCallBacks(self, state, action):
        if hasattr(self.__lt[state][action], '__call__'): 
            print state + ' ' + action + ' ' + self.__lt[state][action].func_name

    def _PrintCallBacks(self):
        for state in self.__state:
            for action in self.__action:
                if hasattr(self.__lt[state][action], '__call__'): 
                    print state + ' ' + action + ' ' + self.__lt[state][action].func_name

class _State(Singleton):
    _currentState = None
    def __init__(self):
        self.__listener = []
    def Start(self):
        pass
    def Stop(self):
        pass
    def TimeUp(self):
        pass
    def AddListener(self, l):
        if isinstance(l, OnStateChangeListener):
            self.__listener.append(l)
    def Update(self, action):
        for i in self.__listener:
            i.OnStateChange(self, action)

class IdleState(_State):
    def Start(self):
        _State._currentState = WorkState()

    def TimeUp(self):
        _State._currentState = IdleState()

    def Stop(self):
        _State._currentState = StopState()

class WorkState(_State):
    def Start(self):
        _State._currentState = WorkState()

    def TimeUp(self):
        _State._currentState = RestState()
        
    def Stop(self):
        _State._currentState = IdleState()

class RestState(_State):
    def Start(self):
        _State._currentState = RestState()

    def TimeUp(self):
        _State._currentState = IdleState()

    def Stop(self):
        _State._currentState = IdleState()

class StopState(_State):
    def Start(self):
        _State._currentState = WorkState()

    def TimeUp(self):
        pass

    def Stop(self):
        pass

# Proxy State class
class State(_State):
    if not _State._currentState:
        _State._currentState = StopState()

    def getState(self):
        return self._currentState.__class__.__name__

    def Start(self):
        str = '[' + self.getState() + "] --start--> ["
        _State._currentState.Update('start')
        _State._currentState.Start()
        str += self.getState() + ']'
        logging.info(str)

    def Stop(self):
        str = '[' + self.getState() + "] --stop--> ["
        _State._currentState.Update('stop')
        _State._currentState.Stop()
        str += self.getState() + ']'
        logging.info(str)

    def TimeUp(self):
        str = '[' + self.getState() + "] --timeup--> ["
        _State._currentState.Update('timeup')
        _State._currentState.TimeUp()
        str += self.getState() + ']'
        logging.info(str)

    def AddListener(self, l, state=None):
        if not state:
            WorkState().AddListener(l)
            IdleState().AddListener(l)
            RestState().AddListener(l)
            StopState().AddListener(l)
        elif issubclass(state.__class__, _State):
            state.AddListener(l)
