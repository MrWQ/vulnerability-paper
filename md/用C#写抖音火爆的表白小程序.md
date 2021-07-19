> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/MiLIxBX215FDNmJZ9oZ2xg)

我们刷抖音的时候经常看到一些有趣的程序，使用 vbs、html、python、bat 批处理代码实现的较多。其实都很简单，今天我们用 C# 来实现以下。其实都是一些过时的东西，初学者可以当做乐趣练习一下编程。网上也有很多源码，我们目的是要搞明白的是代码的意思才是最重要的。

**最终效果：**

**![](https://mmbiz.qpic.cn/mmbiz_gif/icJwZKk2RDibN2K4JNpgWFBGOJLdUGE5zjIg83yicLtM4q4sPicoUwuuBPlkHBs0yFvZdFic06VCTmrJq2DvJIiaPgTQ/640?wx_fmt=gif)**

**制作过程：**

1. 创建一个. net  framework 窗体项目。

2. 加入两个标签、两个 button 按钮、图片框

3. 设置标签字体、颜色

4. 加入图片到图片框

5. 设置窗体启动居中、大小、背景色

6. 按钮 caption 标题属性、位置等

![](https://mmbiz.qpic.cn/mmbiz_png/icJwZKk2RDibN2K4JNpgWFBGOJLdUGE5zjsaRa5QR5OhD0FX5RGiaGTaIchucHiaVtdXfvT9N2lFlwwx9v0UUWxSqA/640?wx_fmt=png)

**代码：**

```
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DemoLove
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("我就知道你会同意的", "(*^▽^*)");
            MessageBox.Show("恭喜你拥有一名可爱的男朋友~~", "(*^▽^*)");
            MessageBox.Show("♥♥爱你，么么哒♥♥","(*^▽^*)");
            this.Dispose();

        }

        private void button2_MouseEnter(object sender, EventArgs e)
        {
            int x = this.ClientSize.Width - button2.Width;
            int y = this.ClientSize.Height - button2.Height;
            Random r = new Random();
            button2.Location = new Point(r.Next(0, x + 1), r.Next(0, y + 1));  //按钮随机移动坐标

        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            MessageBox.Show("明人不说暗话！", "(╯_╰)╭");
            MessageBox.Show("我喜欢你！", "(╯_╰)╭");
            MessageBox.Show("我知道你在等我这一句话！", "(╯_╰)╭");
            MessageBox.Show("请你不要拒绝我", "(╯_╰)╭");
            MessageBox.Show("拒绝我，不存在的", "(╯_╰)╭");
            MessageBox.Show("这辈子都不可能让你离开我", "(╯_╰)╭");
            MessageBox.Show("跟我走吧", "(╯_╰)╭");
            MessageBox.Show("房产证上写你名", "(╯_╰)╭");
            MessageBox.Show("我会洗衣还会做饭", "(╯_╰)╭");
            MessageBox.Show("爱你。么么哒~", "(╯_╰)╭");
            MessageBox.Show("行，我们就去民政局登记吧", "(╯_╰)╭");
            MessageBox.Show("不回答不能退出哦！", "(╯_╰)╭");
            e.Cancel = true;  //不能关闭窗体 取消当前事件操作，则不关闭窗体

        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //this.label1.Focus();
        }
    }
}
```

赶紧发给你要表白的妹子吧~~ 不想答应程序关闭不了，键盘 alt+f4 拒绝一切花里胡哨就可以关闭程序了哈哈~ 需要源码的伙伴公众号私信【love】领取哦。