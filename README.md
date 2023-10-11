# Overwatch-2-Screenshot-OCR-Tool
A tool that will take a screenshot of the score when opened, and use OCR to input all scoreboard into a .csv file.

## Preliminary Information
1. The ScreenshotTool saves all images in the SAME file that its located in (ie: if you have the ScreenshotTool in a folder on your desktop, all images will be saved in that folder).
2. The OCRTesseract tool analyzes all images in the same folder that it is located in.
3. The OCRTesseract tool does not run on its own, it needs to be ran to analyze and input data.

## How to Use
1. Compile and run ScreenshotTool.exe using **C++17 or later**
2. Once running, every time the TAB key is pressed, a screenshot in .bmp format is taken.
3. Compile and run OCRTesseract tool (ensure that OCRTesseract is in the same folder as the ScreenshotTool and images are located in).
4. Data from the ScreenshotTool will be parsed into the OCRTesseract tool and data will be inputted into result.csv.
5. Open result.csv to read data results, parse and analyze the data however you want.

## Dependencies that need to be downloaded (Py only, No C++ dependencies need to be downloaded)
1. PyTesseract
2. cv2
