using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DirectoryTraversalScan.Components
{
    public static class ByteExtension
    {
        public static string ToHex(this byte x)
        {
            return Convert.ToString(x, 16).PadLeft(2, '0');
        }

        public static byte[] Overlong(this byte X)
        {
            return new[] { (byte)(0xC0 | ((X & 0xC0) >> 0x6)), (byte)((X | 0x80) & ~0x40) };
        }  
    }
}
