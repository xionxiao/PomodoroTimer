@echo off 

python setup.py py2exe

cd dist

7z -aoa x library.zip -olibrary\ 
del library.zip 
 
cd library\ 
7z.exe a -tzip -mx9 ..\library.zip -r 
cd.. 
rd library /s /q 
 
upx --best *.* 
cd ..
