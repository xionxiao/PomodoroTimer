# -*- coding: utf8 -*-
#!/usr/bin/python

from distutils.core import setup
import py2exe
import sys, platform

# Change to x86 or amd64 according to your processor Architecture
if len(sys.argv) > 1 and (sys.argv[1] in ("amd64", "x86", "AMD64", "X86")):
    arch = sys.argv[1]
    sys.argv.pop(1)
else:
    machine = platform.uname()[4]
    if machine in ('x86', 'X86', 'x86_32', 'X86_32'):
        arch = 'x86'
    elif machine in ('amd64', 'AMD64', 'x86_64', 'X86_64'):
        arch = 'AMD64'

sys.argv.append('py2exe')

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="%s"
    name="Controls"
    type="win32"
/>
<description>XPomodoroTimer</description>
<dependency>
    <dependentAssembly> 
        <assemblyIdentity 
            type="win32" 
            name="Microsoft.VC90.CRT" 
            version="9.0.21022.8" 
            processorArchitecture="%s" 
            publicKeyToken="1fc8b3b9a1e18e3b" 
        /> 
    </dependentAssembly> 
</dependency>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="%s"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
""" % (arch, arch, arch)

"""
installs manifest and icon into the .exe
but icon is still needed as we open it
for the window icon (not just the .exe)
changelog and logo are included in dist
"""
if arch == 'x86':
    bundle_files = 1
else:
    bundle_files = 3
py2exe_options = {#'packages': 'encodings',
                  'compressed': True,
                  'verbose': True,
                  #'optimize': 2,
                  'bundle_files': bundle_files,
                  'dll_excludes': ["MSVCP90.dll","w9xpopen.exe"]}

setup(
    name = "Promodoro Timer",
    version = '1.1.0',
    author = 'xhui',
    #zipfile = None,
    description = 'A simple time management tool, uses The Pomodoro Technique.',
    windows = [
        {
            "script": "App.pyw",
            "icon_resources": [(1, "favicon.ico")],
            "other_resources": [(24,1,manifest)]
        }
    ],
    data_files=["favicon.ico", "REMINDER.WAV",
                "HmJobsDone.wav", "HmReadyToWork.wav",
                "LICENSE","CHANGELOG"],
    options = {"py2exe": py2exe_options}
)
