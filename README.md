# baiduLinkTest 百度网盘链接有效性测试脚本

本程序为检测百度网盘链接有效性的Python脚本。

可输入网址链接后按回车进行测试，或拖入写有网址的txt文件到脚本上进行测试。

可检测以下类别：有效、分享已取消、分享违规、分享不存在。

项目下有个demo.txt文件，可以直接拖入到baiduLinkTest.py脚本上进行测试。

## 依赖

Python 3 以上

requests和bs4（如果没有安装，本程序会自动安装)

## 本程序支持的链接模板
链接: https://pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q?pwd=xxxx 提取码: xxxx 复制这段内容后打开百度网盘手机App，操作更方便哦

链接: https://pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q 提取码: xxxx 

https://pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q

https://pan.baidu.com/s/1jIw2Qkm

pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q

/s/1E7MsqV3Fv2zIRlDD1nG37Q

1E7MsqV3Fv2zIRlDD1nG37Q

（本程序也支持以空格、逗号、回车作为网址间隔方式）

## 其他

打开程序后，输入q或quit或exit退出，或按下Ctrl-C退出。

打开程序后，请不要直接粘贴带有回车的内容。如有需要，可复制文本到txt文件中，然后把txt文件拖入到该python脚本运行。

## License

The project is released under MIT License.