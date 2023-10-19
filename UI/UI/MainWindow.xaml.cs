using System;
using System.IO;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace UI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            // Add your button click logic here
            MessageBox.Show("Button clicked!");
        }

        private void StartScreenshotTool_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                Process screenshotProcess = new Process();
                screenshotProcess.StartInfo.FileName = "PATH_TO_SCREENSHOT_EXE_HERE"; // Replace with the path to your ScreenshotTool.exe
                // TODO: update the find screenshot.exe process to use screenshot.exe that is present in the same file as UI.exe, to prevent strange things from happening
                // TODO: program will freeze up when the "Start screenshot Tool" picture is taken
                // TODO: program will continue taking screenshots after the program itself is closed, closing the program should completely destroy all processes.
                // TODO: when minimizing the application, make it go to the system tray
                // TODO: add icon
                screenshotProcess.StartInfo.UseShellExecute = false;
                screenshotProcess.StartInfo.CreateNoWindow = true; // This will prevent the console window from opening
                screenshotProcess.StartInfo.RedirectStandardOutput = true;

                screenshotProcess.OutputDataReceived += new DataReceivedEventHandler((s, args) =>
                {
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        outputTextBox.Text += args.Data + Environment.NewLine;
                    });
                });

                screenshotProcess.Start();
                screenshotProcess.BeginOutputReadLine(); // Start asynchronous read operations on the redirected StandardOutput stream

                screenshotProcess.WaitForExit();
                screenshotProcess.Close();
            }
            catch (Exception ex)
            {
                // Handle any exceptions here
                MessageBox.Show("An error occurred: " + ex.Message);
            }
        }
    }
}
