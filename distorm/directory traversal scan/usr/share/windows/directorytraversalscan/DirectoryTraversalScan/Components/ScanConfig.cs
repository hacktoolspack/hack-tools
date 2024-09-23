using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.ComponentModel;
using System.Reflection;
using System.Xml.Serialization;
using AutoSecTools.Components.Serialization;

namespace DirectoryTraversalScan.Components
{
    [Serializable]
    public class ScanConfig : INotifyPropertyChanged
    {
        #region INotifyPropertyChanged Members

        public event PropertyChangedEventHandler PropertyChanged;

        #endregion        

        private static string _configFile = new FileInfo(Assembly.GetExecutingAssembly().Location).Directory +
            "\\config.xml";

        private static XmlSerializer _serializer = new XmlSerializer(typeof(ScanConfig));

        public event EventHandler FlagTextChanged;

        private string _host = "localhost";

        public string Host
        {
            get { return _host; }
            set
            {
                _host = value;

                if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("Host"));
            }
        }

        private int _port = 80;

        public int Port
        {
            get { return _port; }
            set
            {
                _port = value;

                if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("Port"));
            }
        }

        private string _flagText = "windows";

        public string FlagText
        {
            get { return _flagText; }
            set
            {
                _flagText = value;

                if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("FlagText"));

                if (FlagTextChanged != null)
                    FlagTextChanged(this, new EventArgs());
            }
        }

        private string _file = "boot.ini";

        public string File
        {
            get { return _file; }
            set
            {
                _file = value;

                if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("File"));
            }
        }

        private string _path = "";

        public string Path
        {
            get { return _path; }
            set
            {
                _path = value;

                if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("Path"));
            }
        }

        public static ScanConfig Load()
        {
            return System.IO.File.Exists(_configFile) ?
                _serializer.Deserialize(_configFile) as ScanConfig :
                null;
        }

        public void Save()
        {
            _serializer.Serialize(_configFile, this);
        }
    }
}
