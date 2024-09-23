using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DirectoryTraversalScan.Components
{
    public static class IEnumerableExtension
    {
        public static string ToHex(this IEnumerable<byte> Bytes)
        {
            return Bytes
                .Select(x => x.ToHex())
                .Aggregate();
        }
    }
}
