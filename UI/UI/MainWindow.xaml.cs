﻿using System;
using System.IO;
using System.Diagnostics;
using System.Windows;
using System.Linq;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Forms;
using System.ComponentModel;
using System.Windows.Threading;

namespace UI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Process screenshotProcess;
        private NotifyIcon notifyIcon;
        private bool isScreenshotToolRunning = false;

        public MainWindow()
        {
            InitializeComponent();
            this.Closed += MainWindow_Closed;
            this.StateChanged += MainWindow_StateChanged;

            this.MinWidth = 435;
            this.MinHeight = 330;

            this.MaxWidth = 500;
            this.MaxHeight = 500;

            outputTextBox.IsReadOnly = true;

            // Initialize NotifyIcon 
            notifyIcon = new NotifyIcon();
            notifyIcon.Icon = new System.Drawing.Icon("picture.ico");
            notifyIcon.Visible = false; // The icon will be visible when the window is minimized
            this.Icon = new System.Windows.Media.Imaging.BitmapImage(new Uri("picture.ico", UriKind.RelativeOrAbsolute));
            System.Windows.Application.Current.MainWindow.Icon = new System.Windows.Media.Imaging.BitmapImage(new Uri("picture.ico", UriKind.RelativeOrAbsolute));

            notifyIcon.MouseClick += notifyIcon_MouseClick;
        }

        private void notifyIcon_MouseClick(object sender, System.Windows.Forms.MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left)
            {
                this.Show();
                this.WindowState = WindowState.Normal;
                notifyIcon.Visible = false;
            }
        }

        private void MainWindow_Closed(object sender, EventArgs e)
        {
            if (screenshotProcess != null && !screenshotProcess.HasExited)
            {
                screenshotProcess.Kill();
            }
            StopPythonScript();

        }

        private void StartScreenshotTool_Click(object sender, RoutedEventArgs e)
        {
            if (isScreenshotToolRunning)
            {
                outputTextBox.Text += "An instance of Screenshot Tool is already running!" + Environment.NewLine;
                return;
            }

            try
            {
                isScreenshotToolRunning = true;

                string baseDirectory = System.AppDomain.CurrentDomain.BaseDirectory;
                string screenshotToolPath = System.IO.Path.Combine(baseDirectory, "Overwatch-2-Screenshot-OCR-Tool.exe");

                screenshotProcess = new Process();
                screenshotProcess.StartInfo.FileName = screenshotToolPath;
                screenshotProcess.StartInfo.UseShellExecute = false;
                screenshotProcess.StartInfo.CreateNoWindow = true; // This will prevent the console window from opening
                screenshotProcess.StartInfo.RedirectStandardOutput = true; // Redirects output
                screenshotProcess.StartInfo.RedirectStandardInput = true; // Redirects input

                screenshotProcess.OutputDataReceived += new DataReceivedEventHandler((s, args) =>
                {
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        if (args.Data != null && args.Data.Contains("Do you want to delete the excess screenshots? (Y/N): "))
                        {
                            // Display the user prompt in a MessageBox or another UI element
                            MessageBoxResult result = System.Windows.MessageBox.Show(args.Data, "User Prompt", MessageBoxButton.YesNo);

                            // Send the user's response to the process
                            screenshotProcess.StandardInput.WriteLine(result == MessageBoxResult.Yes ? "Y" : "N");
                        }
                        else if (args.Data != null)
                        {
                            outputTextBox.Text += args.Data + Environment.NewLine;
                        }
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
                System.Windows.MessageBox.Show("An error occurred: " + ex.Message);
                isScreenshotToolRunning = false;
            }
        }

        private void ScreenshotProcess_Exited(object sender, EventArgs e)
        {
            Dispatcher.Invoke(() =>
            {
                outputTextBox.Text += "Screenshot Tool process has exited." + Environment.NewLine;
                ScreenshotToolStatus.Content = "Screenshot Tool Status: Not Running";
                isScreenshotToolRunning = false;
            });
        }

        private void CloseScreenshotTool_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (screenshotProcess != null && !screenshotProcess.HasExited)
                {
                    screenshotProcess.CloseMainWindow(); // Attempt to close the main window
                    if (!screenshotProcess.WaitForExit(2000)) // Wait for the process to exit for 2 seconds
                    {
                        screenshotProcess.Kill(); // Forcefully kill the process if it hasn't exited gracefully
                    }
                }

                // Update the Screenshot Tool status text
                ScreenshotToolStatus.Content = "Screenshot Tool Status: Not Running";
            }
            catch (Exception ex)
            {
                // Handle any exceptions here
                System.Windows.MessageBox.Show("An error occurred while closing the screenshot tool: " + ex.Message);
            }
        }

        private void MainWindow_StateChanged(object sender, EventArgs e)
        {
            if (WindowState == WindowState.Minimized)
            {
                this.Hide(); // Hide the window
                notifyIcon.Visible = true; // Show the icon in the system tray
                notifyIcon.ShowBalloonTip(1000, "Minimized to tray", "The tool has been minimized to your system tray.", ToolTipIcon.None); // Display a notification
            }
        }

        // Dispose of the NotifyIcon when the application is closing
        protected override void OnClosing(CancelEventArgs e)
        {
            if (notifyIcon != null)
            {
                notifyIcon.Dispose();
            }
            base.OnClosing(e);
        }

        private void CaptureOutputAndUpdateUI(object sender, DataReceivedEventArgs e)
        {
            if (e.Data != null)
            {
                Dispatcher.BeginInvoke(new Action(() =>
                {
                    outputTextBox.AppendText(e.Data + Environment.NewLine);
                }), DispatcherPriority.Normal);
            }
        }

        private void RunPythonScript()
        {
            try
            {
                string baseDirectory = System.AppDomain.CurrentDomain.BaseDirectory;
                string pythonScriptPath = System.IO.Path.Combine(baseDirectory, "OCRTesseract.exe");

                if (!File.Exists(pythonScriptPath))
                {
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        outputTextBox.Text += "Python script not found!" + Environment.NewLine;
                    });
                    return;
                }

                ProcessStartInfo start = new ProcessStartInfo();
                start.FileName = pythonScriptPath;
                start.UseShellExecute = false;
                start.CreateNoWindow = true;
                start.RedirectStandardOutput = true;
                start.RedirectStandardError = true;

                Process process = new Process();
                process.StartInfo = start;
                process.EnableRaisingEvents = true;
                process.OutputDataReceived += CaptureOutputAndUpdateUI;
                process.ErrorDataReceived += CaptureOutputAndUpdateUI;

                process.Exited += (sender, e) =>
                {
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        outputTextBox.Text += "Python script processing complete." + Environment.NewLine;
                    });
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();
            }
            catch (Exception ex)
            {
                System.Windows.MessageBox.Show("An error occurred while running the Python script: " + ex.Message);
            }
        }

        private void StopPythonScript()
        {
            try
            {
                // Find and stop the OCR process
                Process[] processes = Process.GetProcessesByName("OCRTesseract");
                Process selectedProcess = null;

                foreach (Process process in processes)
                {
                    if (process.MainWindowTitle == "YourUniqueTitle")
                    {
                        selectedProcess = process;
                        break;
                    }
                }

                if (selectedProcess != null)
                {
                    selectedProcess.Kill();
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        outputTextBox.Text += $"OCRTesseract process with PID {selectedProcess.Id} has been stopped." + Environment.NewLine;
                    });
                }
                else
                {
                    outputTextBox.Dispatcher.Invoke(() =>
                    {
                        outputTextBox.Text += "OCRTesseract process not found." + Environment.NewLine;
                    });
                }
            }
            catch (Exception ex)
            {
                // Handle any exceptions here
                System.Windows.MessageBox.Show("An error occurred while stopping the OCR process: " + ex.Message);
            }
        }

        private void RunPythonScript_Click(object sender, RoutedEventArgs e)
        {
            RunPythonScript();
        }

        private void StopPythonScript_Click(object sender, RoutedEventArgs e)
        {
            StopPythonScript();
        }
    }
}
