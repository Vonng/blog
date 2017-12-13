---
title: "嗅探无线网络数据包"
date: "2015-12-07"
author: "Vonng"
description: "以太网里抓包很简单，不过如果是无线数据包，就要稍微麻烦一点了。"
categories: ["Dev"]
featured: ""
featuredalt: ""
featuredpath: ""
linktitle: ""
type: "post"
---

结论：
Mac: airport, tcpdump
Windows:  Omnipeek
Linux: tcpdump, airmon-ng


<!--more-->

以太网里抓包很简单，各种软件一大把，什么Wireshark，Ethereal，Sniffer Pro 一抓一大把。不过如果是无线数据包，就要稍微麻烦一点了。网上找了一堆罗里吧嗦的文章，绕来绕去的,其实抓无线包一条命令就好了。

Windows下因为无线网卡驱动会拒绝进入混杂模式，所以比较蛋疼，一般是用Omnipeek去弄，不细说了。

Linux和Mac就很方便了。只要用tcpdump就可以，一般系统都自带了。最后-i选项的参数填想抓的网络设备名就行。Mac默认的WiFi网卡是en0。
`tcpdump -Ine -i en0 `

主要就是指定-I参数，进入监控模式。
`-I :Put the interface in "monitor mode"; this is supported only on IEEE 802.11 Wi-Fi interfaces, and supported only  on  some operating systems.`
进入监控模式之后计算机用于监控的无线网卡就上不了网了，所以可以考虑买个外置无线网卡来抓包，上网抓包两不误。

抓了包能干很多坏事，比如WEP网络抓几个IV包就可以用aircrack破密码，WPA网络抓到一个握手包就能跑字典破无线密码了。如果在同一个网络内，还可以看到各种未加密的流量……什么小黄图啊，隐私照啊之类的……。

假如我已经知道某个手机的MAC地址，那么只要
`tcpdump -Ine -i en0 | grep $MAC_ADDRESS `
就过滤出该手机相关的WiFi流量。

具体帧的类型详情参看802.11协议，《802.11无线网络权威指南》等。

顺便解释以下混杂模式与监控模式的区别：
混杂(promiscuous)模式是指：接收同一个网络中的所有数据包，无论是不是发给自己的。
监控(monitor)模式是指：接收某个物理信道中所有传输着的数据包。

>RFMON
>RFMON is short for radio frequency monitoring mode and is sometimes also described as monitor mode or raw monitoring mode. In this mode an 802.11 wireless card is in listening mode (“sniffer” mode).
>
>The wireless card does not have to associate to an access point or ad-hoc network but can passively listen to all traffic on the channel it is monitoring. Also, the wireless card does not require the frames to pass CRC checks and forwards all frames (corrupted or not with 802.11 headers) to upper level protocols for processing. This can come in handy when troubleshooting protocol issues and bad hardware.
>
>RFMON/Monitor Mode vs. Promiscuous Mode
>Promiscuous mode in wired and wireless networks instructs a wired or wireless card to process any traffic regardless of the destination mac address. In wireless networks promiscuous mode requires that the wireless card be associated to an access point or ad-hoc network. While in promiscuous mode a wireless card can transmit and receive but will only captures traffic for the network (SSID) to which it is associated.
>
>RFMON mode is only possible for wireless cards and does not require the wireless card to be associated to a wireless network. While in monitor mode the wireless card can passively monitor traffic of all networks and devices within listening range (SSIDs, stations, access points). In most cases the wireless card is not able to transmit and does not follow the typical 802.11 protocol when receiving traffic (i.e. transmit an 802.11 ACK for received packet).
>
>Both modes have to be supported by the driver of the wired or wireless card.

另外在研究抓包工具时，发现了Mac下有一个很好用的命令行工具airport，可以用来抓包，以及摆弄Macbook的WiFi。
位置在
`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport`

可以创建一个符号链接方便使用：
`sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport  /usr/sbin/airport`

常用的命令有：
显示当前网络信息：`airport -I`
扫描周围无线网络：`airport -s`
断开当前无线网络：`airport -z`
强制指定无线信道：`airport -c=$CHANNEL`

抓无线包，可以指定信道：
`airport en0 sniff [$CHANNEL]`
抓到的包放在/tmp/airportSniffXXXXX.cap，可以用tcpdump, tshark, wireshark等软件来读。

最实用的功能还是扫描周围无线网络。
