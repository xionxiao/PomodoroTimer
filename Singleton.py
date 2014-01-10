# -*- coding: utf-8 -*-
class _Singleton(type):
    __instances = {}
 
    def __call__(cls):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(_Singleton, cls).__call__()
        return cls.__instances[cls]
 
class Singleton(_Singleton('Singleton', (object, ), {})):
    pass
