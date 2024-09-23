using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Serialization;

namespace AutoSecTools.Components.Serialization
{
    public static class XmlSerializerExtension
    {
        public static void Serialize(this XmlSerializer Serializer, string Filename, object o)
        {
            using (var s = File.Create(Filename))
                Serializer.Serialize(s, o);
        }

        public static object Deserialize(this XmlSerializer Serializer, string Filename)
        {
            using (var s = File.OpenRead(Filename))
                return Serializer.Deserialize(s);
        }
    }
}
