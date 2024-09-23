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
using System.Collections.ObjectModel;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Windows.Media;

namespace DirectoryTraversalScan.Components
{
    public class ResponseSet : INotifyPropertyChanged
    {
        #region INotifyPropertyChanged Members

        public event PropertyChangedEventHandler PropertyChanged;

        #endregion

        private string _responseCode;

        public string ResponseCode
        {
            get { return _responseCode; }
            set { _responseCode = value; }
        }

        private ObservableCollection<Response> _responses = new ObservableCollection<Response>();

        public ObservableCollection<Response> Responses
        {
            get { return _responses; }
            //set 
            //{
            //    _responses = value;

            //    if (PropertyChanged != null)
            //        PropertyChanged(this, new PropertyChangedEventArgs("Responses"));
            //}
        }
    }

    public class Response : INotifyPropertyChanged
    {
        #region INotifyPropertyChanged Members

        public event PropertyChangedEventHandler PropertyChanged;

        #endregion

        public string Text { get; set; }

        //public string FirstLine
        //{
        //    get
        //    {
        //        var t = Text.Split('\r', '\n');

        //        return t.Length != 0 ? t[0] : "[none]";
        //    }
        //}

        private string _requestStatus;
        
        public string RequestStatus
        {
        	get { return _requestStatus; }
        	set
        	{                
        		_requestStatus = value;
        
        		if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("RequestStatus"));
        	}
        }

        private ObservableCollection<string> _requests;

        public ObservableCollection<string> Requests
        {
            get { return _requests; }
            set 
            {
                _requests = value;
                _requests.CollectionChanged += new System.Collections.Specialized.NotifyCollectionChangedEventHandler(_requests_CollectionChanged);
                _requests_CollectionChanged(this, null);
            }
        }

        void _requests_CollectionChanged(object sender, System.Collections.Specialized.NotifyCollectionChangedEventArgs e)
        {
            RequestStatus = _requests.Count + " Request" +
                (_requests.Count != 1 ? "s" : "");
        }

        private SolidColorBrush _backgroundColor;

        public SolidColorBrush BackgroundColor
        {
            get { return _backgroundColor; }
            set
            {
                _backgroundColor = value;

                if (PropertyChanged != null)
                    PropertyChanged(this, new PropertyChangedEventArgs("BackgroundColor"));
            }
        }

        public Response()
        {
            Requests = new ObservableCollection<string>();
        }
    }
}
