# -*- coding: utf-8 -*-
from TimerApp import *
import logging
import os

def SetupLog():
    logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), 
    	format='%(asctime)s %(message)s',
    	level=logging.DEBUG
    	)
    logging.info("================ App Start ================")
    pass

if __name__ == "__main__":
    SetupLog()
    app = TimerApp()
    app.MainLoop()
