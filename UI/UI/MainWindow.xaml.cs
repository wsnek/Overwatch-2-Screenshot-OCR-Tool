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
                string baseDirectory = System.AppDomain.CurrentDomain.BaseDirectory;
                string screenshotToolPath = System.IO.Path.Combine(baseDirectory, "Overwatch-2-Screenshot-OCR-Tool.exe");

                Process screenshotProcess = new Process();
                screenshotProcess.StartInfo.FileName = screenshotToolPath;
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
