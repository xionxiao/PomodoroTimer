# -*- coding: utf8 -*-
#!/usr/bin/python

from distutils.core import setup
import py2exe

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>XPomodoro</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

"""
installs manifest and icon into the .exe
but icon is still needed as we open it
for the window icon (not just the .exe)
changelog and logo are included in dist
"""

setup(
    windows = [
        {
            "script": "Timer.pyw",
            "icon_resources": [(1, "favicon.ico")],
            "other_resources": [(24,1,manifest)]
        }
    ],
    data_files=["favicon.ico", "REMINDER.WAV"],
    options = {"py2exe": {"dll_excludes":["MSVCP90.dll","MSVCR90.dll"]}}
)
