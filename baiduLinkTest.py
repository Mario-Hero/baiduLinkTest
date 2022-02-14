#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Mario Chen, 22.01.2022, Shenzhen
# My Github site: https://github.com/Mario-Hero

'''
# 本程序为百度网盘链接有效检测程序。可输入网址链接或拖入写有网址的txt文件进行测试。
# 本程序可检测以下类别：有效、分享已取消、分享违规、分享不存在。
# 打开程序后，输入q或quit或exit退出，或按下Ctrl-C退出。

# 本程序支持的链接模板
链接: https://pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q?pwd=xxxx 提取码: xxxx 复制这段内容后打开百度网盘手机App，操作更方便哦
链接: https://pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q 提取码: xxxx 复制这段内容后打开百度网盘手机App，操作更方便哦
https://pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q
https://pan.baidu.com/s/1jIw2Qkm
pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q
/s/1E7MsqV3Fv2zIRlDD1nG37Q
1E7MsqV3Fv2zIRlDD1nG37Q

# 本程序支持以空格、逗号、回车作为网址间隔方式
pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q
pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q,pan.baidu.com/s/1E7MsqV3Fv2zIRlDD1nG37Q

#打开程序后，请不要直接粘贴带有回车的内容。如有需要，可复制文本到txt文件中，然后把txt文件拖入到该python脚本运行。
'''

import os
import sys
import time
import random

try:
    import requests
except ImportError:
    os.system('pip install requests')
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    os.system('pip install bs4')
    from bs4 import BeautifulSoup

session = requests.Session()

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36"}

urlTested = []
shixiao = []
shixiaoLate = []
shixiaoQinquan = []
youxiao = []
bucunzai = []


def linkTest(url):
    baiurl = ''.join(x for x in url if ord(x) < 256)
    if ' ' in baiurl:
        for urlTemp in baiurl.split(' '):
            linkTest(urlTemp)
    else:
        if baiurl.startswith(':') or baiurl.startswith('：'):
            return linkTest(baiurl[1:])
        elif baiurl.startswith('https://'):
            if len(baiurl) <= 47:
                pass
            else:
                baiurl = baiurl[0:47]
        elif baiurl.startswith('pan.baidu.com'):
            baiurl = 'https://' + baiurl
        elif baiurl.startswith('/s/'):
            baiurl = 'https://pan.baidu.com' + baiurl
        elif baiurl.startswith('/'):
            baiurl = 'https://pan.baidu.com/s' + baiurl
        elif len(baiurl) == 23:
            baiurl = 'https://pan.baidu.com/s/' + baiurl
        else:
            return 3  # not baidu url, should ignore
        if baiurl in urlTested:
            return 3  # already exists, should ignore
        else:
            urlTested.append(baiurl)
        sleepTime = random.randint(1, 10) / 5.0
        time.sleep(sleepTime)
        try:
            resp = session.get(baiurl, headers=HEADER, timeout=5).content
        except requests.exceptions.RequestException as e:
            print(e.__class__.__name__)
            return 4  # cannot connect
        soup = BeautifulSoup(resp, 'lxml')
        if soup.select_one('.error-img'):
            reason = soup.find('div', {'id': 'share_nofound_des'}).text.strip()
            if '你来晚了' in reason:
                print(baiurl + ' 分享已取消')
                shixiaoLate.append(baiurl)
            elif '侵权' in reason:
                print(baiurl + ' 违规')
                shixiaoQinquan.append(baiurl)
            else:
                print(baiurl + ' 失效了')
                shixiao.append(baiurl)
            return 1  # 失效
        elif soup.select_one('.error-main'):
            print(baiurl + ' 不存在')
            bucunzai.append(baiurl)
            return 2  # 不存在
        else:
            print(baiurl + ' 有效')
            youxiao.append(baiurl)
            return 0  # 有效


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            while True:
                inputAddr = input('请输入百度云链接:\n')
                inputAddr = inputAddr.strip()
                if not inputAddr:
                    continue
                if inputAddr != 'q' and inputAddr != 'quit' and inputAddr != 'exit':
                    if os.path.isfile(inputAddr):
                        f = open(inputAddr, 'r', encoding='utf-8')
                        for line in f.readlines():
                            linkTest(line)
                        f.close()
                    elif '\n' in inputAddr:
                        for address in inputAddr.split('\n'):
                            linkTest(address)
                    elif ' ' in inputAddr:
                        for address in inputAddr.split(' '):
                            linkTest(address)
                    else:
                        linkTest(inputAddr)
                else:
                    break
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        print('正在测试链接...')
        for arg in sys.argv[1:]:
            if os.path.exists(arg):
                if os.path.isfile(arg):
                    f = open(arg, 'r', encoding='utf-8')
                    for line in f.readlines():
                        line = line.strip()
                        if ' ' in line:
                            for lineChild in line.split(' '):
                                linkTest(lineChild)
                        elif ',' in line:
                            for lineChild in line.split(','):
                                linkTest(lineChild)
                        else:
                            linkTest(line)
                    f.close()
            else:
                linkTest(arg)
        if shixiao:
            print('\n不明原因失效链接:')
            for shixiaoUrl in shixiao:
                print(shixiaoUrl)
            print(' ')
        if bucunzai:
            print('\n不存在链接:')
            for bucunzaiUrl in bucunzai:
                print(bucunzaiUrl)
            print(' ')
        if shixiaoLate:
            print('\n分享已取消链接:')
            for shixiaoLateUrl in shixiaoLate:
                print(shixiaoLateUrl)
            print(' ')
        if shixiaoQinquan:
            print('\n违规链接:')
            for shixiaoQinquanUrl in shixiaoQinquan:
                print(shixiaoQinquanUrl)
            print(' ')
        if not (shixiao or shixiaoLate or shixiaoQinquan or bucunzai):
            print('\n链接全部有效。\n')
        os.system('pause')
