import os, base64, zlib
import StringIO

_R_Class_String = """
class _R(dict):
    def __getitem__(self, name):
        return StringIO.StringIO(
            zlib.decompress(
                base64.decodestring(
                    super(_R,self).__getitem__(name)
                    )))

R = _R()
"""

class Resource():
    __res_list = {}
    def Add(self, id, filename):
        if os.path.isfile(filename):
            self.__res_list[id] = filename

    def Compile(self):
        rf = open('R.py', 'w+')
        rf.write('import base64, zlib, StringIO\n')
        rf.write(_R_Class_String)
        for r in self.__res_list:
            f = open(self.__res_list[r], 'rb').read();
            data = base64.encodestring(zlib.compress(f));
            rf.write('R[' + repr(r) + '] = """' + data + '"""\n\n')
        rf.close()

    def Retrive(self, id):
        sf = zlib.decompress(base64.decodestring())
        return StringIO.StringIO(sf)

# test case
if __name__ == "__main__":
    r = Resource()
    r.Add('favicon.ico', 'favicon.ico')
    r.Add('HmJobsDone.wav', 'HmJobsDone.wav')
    r.Add('REMINDER.WAV', 'REMINDER.WAV')
    r.Add('HmReadyToWork.wav', 'HmReadyToWork.wav')
    r.Compile()
    from R import *
    print(R['favicon.ico'])
    print(R['HmJobsDone.wav'].read())
