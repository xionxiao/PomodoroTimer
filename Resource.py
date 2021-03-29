# -*- coding: utf8 -*-
import os, base64, zlib
from io import BytesIO

_R_Class_String = """
# -*- coding: utf8 -*-
import base64, zlib
from io import BytesIO

class _R(dict):
    def __getitem__(self, name):
        return BytesIO(
            zlib.decompress(
                base64.b64decode(
                    super(_R,self).__getitem__(name)
                    )))

R = _R()
"""

class Resource():
    __res_list = {}
    def add(self, id, filename):
        if os.path.isfile(filename):
            self.__res_list[id] = filename

    def compile(self):
        with open("R.py", "w+") as f:
            f.write(_R_Class_String)
            for r in self.__res_list:
                with open(self.__res_list[r], 'rb') as source:
                    d = source.read()
                    data = base64.b64encode(zlib.compress(d))
                    #f.write('R[' + repr(r) + '] = """' + bytes.decode(data) + '"""\n\n')
                    f.write('R[' + repr(r) + '] = ' + str(data) + '\n\n')
                

    def retrive(self, id):
        sf = zlib.decompress(base64.b64decode(self.__res_list[id]))
        return BytesIO(sf)

# test case
if __name__ == "__main__":
    r = Resource()
    r.add('favicon.ico', 'favicon.ico')
    r.add('HmJobsDone.wav', 'HmJobsDone.wav')
    r.add('REMINDER.WAV', 'REMINDER.WAV')
    r.add('HmReadyToWork.wav', 'HmReadyToWork.wav')
    r.add('requirements', 'requirements.txt')
    r.compile()
    from R import *
    print(R['favicon.ico'])
    print(R['HmJobsDone.wav'].read())
