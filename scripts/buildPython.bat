@echo off
title Python Script to Executable
echo Python Script to Executable by wsnek
echo.
echo Please make sure to have 'pyinstaller' installed: pip install pyinstaller

TIMEOUT /t 10 /nobreak

pyinstaller -F --noconfirm --clean --hidden-import=numpy OCRTesseract.py 


echo.
echo pyinstaller compilation of program is now complete
echo.
echo Program can now be exited
PAUSE