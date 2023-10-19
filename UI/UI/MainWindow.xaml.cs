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
        private Process screenshotProcess;

        public MainWindow()
        {
            InitializeComponent();
            this.Closed += MainWindow_Closed;
        }

        private void MainWindow_Closed(object sender, EventArgs e)
        {
            if (screenshotProcess != null && !screenshotProcess.HasExited)
            {
                screenshotProcess.Kill();
            }
        }

        private void StartScreenshotTool_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                string baseDirectory = System.AppDomain.CurrentDomain.BaseDirectory;
                string screenshotToolPath = System.IO.Path.Combine(baseDirectory, "Overwatch-2-Screenshot-OCR-Tool.exe");

                screenshotProcess = new Process();
                screenshotProcess.StartInfo.FileName = screenshotToolPath;
                screenshotProcess.StartInfo.UseShellExecute = false;
                screenshotProcess.StartInfo.CreateNoWindow = true; // This will prevent the console window from opening
                screenshotProcess.StartInfo.RedirectStandardOutput = true; //Redirects output

                screenshotProcess.OutputDataReceived += new DataReceivedEventHandler((s, args) =>
                {
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        outputTextBox.Text += args.Data + Environment.NewLine;
                    });
                });

                screenshotProcess.EnableRaisingEvents = true;
                screenshotProcess.Exited += ScreenshotProcess_Exited;

                screenshotProcess.Start();
                screenshotProcess.BeginOutputReadLine(); // Start asynchronous read operations on the redirected StandardOutput stream

                // Update the Screenshot Tool status text
                ScreenshotToolStatus.Content = "Screenshot Tool Status: Running";
            }
            catch (Exception ex)
            {
                // Handle any exceptions here
                MessageBox.Show("An error occurred: " + ex.Message);
            }
        }

        private void ScreenshotProcess_Exited(object sender, EventArgs e)
        {
            Dispatcher.Invoke(() =>
            {
                outputTextBox.Text += "Screenshot Tool process has exited." + Environment.NewLine;
                ScreenshotToolStatus.Content = "Screenshot Tool Status: Not Running";
            });
        }




        private void CloseScreenshotTool_Click(object sender, RoutedEventArgs e)
        {
            if (screenshotProcess != null && !screenshotProcess.HasExited)
            {
                screenshotProcess.CloseMainWindow(); // Attempt to close the main window
                if (!screenshotProcess.WaitForExit(2000)) // Wait for the process to exit for 2 seconds
                {
                    screenshotProcess.Kill(); // Forcefully kill the process if it hasn't exited gracefully (I am not sure if this is necessary, but it works.)
                }

                // Update the Screenshot Tool status text
                ScreenshotToolStatus.Content = "Screenshot Tool Status: Not Running";
            }
        }


    }
}
