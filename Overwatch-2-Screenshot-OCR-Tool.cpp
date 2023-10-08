#include <iostream>
#include <windows.h>
#include <string>
#include <ctime>

//This code is designed for WINDOWS ONLY

using namespace std;

bool SaveHBITMAPToFile(HBITMAP hBitmap, LPCWSTR filename)
{
    BITMAP bmp;
    HDC hdcMem;
    HANDLE hf;                  // file handle
    BITMAPFILEHEADER hdr;       // bitmap file-header
    PBITMAPINFOHEADER pbih;     // bitmap info-header
    DWORD dwTotal;              // total count of bytes
    DWORD cb;                   // incremental count of bytes
    BYTE* hp;                   // byte pointer
    DWORD dwTmp;

    hdcMem = CreateCompatibleDC(0);
    SelectObject(hdcMem, hBitmap);
    GetObject(hBitmap, sizeof(BITMAP), (LPSTR)&bmp);

    pbih = (PBITMAPINFOHEADER)malloc(sizeof(BITMAPINFOHEADER));
    if (!pbih)
    {
        return false;
    }

    pbih->biSize = sizeof(BITMAPINFOHEADER);
    pbih->biWidth = bmp.bmWidth;
    pbih->biHeight = bmp.bmHeight;
    pbih->biPlanes = 1;
    pbih->biBitCount = 24; // 24-bit BMP
    pbih->biCompression = BI_RGB;
    pbih->biSizeImage = 0;
    pbih->biXPelsPerMeter = 0;
    pbih->biYPelsPerMeter = 0;
    pbih->biClrUsed = 0;
    pbih->biClrImportant = 0;

    dwTotal = ((pbih->biWidth * pbih->biBitCount + 31) / 32) * 4 * pbih->biHeight;
    cb = dwTotal;

    hp = (BYTE*)GlobalAlloc(GMEM_FIXED, cb);
    if (!hp)
    {
        return false;
    }

    if (!GetDIBits(hdcMem, hBitmap, 0, (UINT)pbih->biHeight, hp, (BITMAPINFO*)pbih, DIB_RGB_COLORS))
    {
        return false;
    }

    hf = CreateFile(filename, GENERIC_READ | GENERIC_WRITE, (DWORD)0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, (HANDLE)NULL);
    if (hf == INVALID_HANDLE_VALUE)
    {
        return false;
    }

    hdr.bfType = 0x4d42; // 0x42 = "B" 0x4d = "M"
    // Compute the size of the entire file.
    hdr.bfSize = (DWORD)(sizeof(BITMAPFILEHEADER) + pbih->biSize + cb);
    hdr.bfReserved1 = 0;
    hdr.bfReserved2 = 0;
    // Compute the offset to the array of color indices.
    hdr.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + pbih->biSize;

    // Copy the BITMAPFILEHEADER into the .BMP file.
    if (!WriteFile(hf, (LPVOID)&hdr, sizeof(BITMAPFILEHEADER), (LPDWORD)&dwTmp, NULL))
    {
        return false;
    }
    // Copy the BITMAPINFOHEADER and RGBQUAD array into the file.
    if (!WriteFile(hf, (LPVOID)pbih, sizeof(BITMAPINFOHEADER) + pbih->biClrUsed * sizeof(RGBQUAD), (LPDWORD)&dwTmp, (NULL)))
    {
        return false;
    }
    // Copy the array of color indices into the .BMP file.
    dwTotal = cb;
    dwTmp = 0;
    while (dwTotal > (DWORD)0)
    {
        if (!WriteFile(hf, (LPSTR)hp + dwTmp, (DWORD)cb, (LPDWORD)&dwTmp, NULL))
        {
            return false;
        }
        dwTotal -= dwTmp;
    }

    if (!CloseHandle(hf))
    {
        return false;
    }

    GlobalFree((HGLOBAL)hp);
    return true;
}

int main()
{
    string trigger = "tab";
    bool take_screenshot = false;
    int screenshot_count = 1;

    while (true)
    {
        if (GetAsyncKeyState(VK_TAB))
        {
            if (!take_screenshot)
            {
                // Capture the screen
                HDC hdcScreen = GetDC(NULL);
                int width = 1920;
                int height = 1080;
                HDC hdcMem = CreateCompatibleDC(hdcScreen);
                HBITMAP hBitmap = CreateCompatibleBitmap(hdcScreen, width, height);
                HBITMAP hOldBitmap = (HBITMAP)SelectObject(hdcMem, hBitmap);
                BitBlt(hdcMem, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY);

                // Save the screenshot as BMP
                string filename = "screenshot_" + to_string(screenshot_count) + ".bmp";

                // Convert the filename to wide-character
                wstring wFilename(filename.begin(), filename.end());

                if (SaveHBITMAPToFile(hBitmap, wFilename.c_str()))
                {
                    cout << "Screenshot saved to: " << filename << endl;
                }
                else
                {
                    cerr << "Failed to save screenshot!" << endl;
                }

                // Clean up resources
                SelectObject(hdcMem, hOldBitmap);
                DeleteObject(hBitmap);
                DeleteDC(hdcMem);
                ReleaseDC(NULL, hdcScreen);

                // Increment screenshot count
                screenshot_count++;
                take_screenshot = true;
            }
        }
        else
        {
            take_screenshot = false;
        }

        // Add a delay to avoid continuously taking screenshots (this is in MILLISECONDS ON WINDOWS, SECONDS ON LINUX!)
        Sleep(150);
    }

    return 0;
}