using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Threading;

namespace DirectoryTraversalScan.Components
{
    public static class DispatcherExtension
    {
        public static object Invoke(this Dispatcher d, Action Action)
        {
            return d.Invoke(Action);
        }

        public static object BeginInvoke(this Dispatcher d, Action Action)
        {
            return d.BeginInvoke(Action);
        }
    }
}
