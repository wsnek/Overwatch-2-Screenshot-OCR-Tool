# Overwatch-2-Screenshot-OCR-Tool
A tool that will take a screenshot of the score when opened, and use OCR to input all scoreboard into a .csv file.

## Preliminary Information
1. The ScreenshotTool contains no extra dependencies that need to be downloaded by the user.
2. The OCRTesseract tool requires dependencies that need to be downloaded by the user, the following dependencies are required: pytesseract, os, csv, csv2.
3. The ScreenshotTool saves all images in the SAME file that its located in (ie: if you have the ScreenshotTool in a folder on your desktop, all images will be saved in that folder).
4. The OCRTesseract tool analyzes all images in the same folder that it is located in.
5. The OCRTesseract tool does not run on its own, it needs to be ran every once in a while to analyze and input data.

## How to Use
1. Compile and run ScreenshotTool.exe
2. Once running, every time the TAB key is pressed, a screenshot in .bmp format is taken.
3. Compile and run OCRTesseract tool (ensure that OCRTesseract is in the same folder as the ScreenshotTool and images are located in).
4. Data from the ScreenshotTool will be parsed into the OCRTesseract tool and data will be inputted into result.csv.
5. Open result.csv to read data results, parse and analyze the data however you want.

## Tools Used
1. C++
2. Python
3. iostream
4. windows.h
5. string
6. ctime
7. os
8. pytesseract
9. csv
10. csv2
