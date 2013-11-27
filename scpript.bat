@echo off 

"D:\Python27\python.exe" setup.py py2exe

"D:\Python27\python.exe" build.py py2exe

cd dist

"C:\Program Files\7-Zip\7z.exe" -aoa x library.zip -olibrary\ 
del library.zip 
 
cd library\ 
"C:\Program Files\7-Zip\7z.exe" a -tzip -mx9 ..\library.zip -r 
cd.. 
rd library /s /q 
 
"upx.exe" --best *.* 
cd ..