# -*- coding: utf8 -*-
#!/usr/bin/python

from distutils.core import setup
import py2exe
import sys

# Change to x86 or amd64 according to your processor Architecture
if sys.argv[1] and (sys.argv[1] in ("amd64", "x86", "AMD64", "X86"):
    platform = sys.argv[1]
    sys.argv.pop(1)
else:
    platform = "x86"

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
""" % (platform, platform, platform)

"""
installs manifest and icon into the .exe
but icon is still needed as we open it
for the window icon (not just the .exe)
changelog and logo are included in dist
"""

setup(
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
    options = {"py2exe": {"dll_excludes":["MSVCP90.dll"]}}
)
