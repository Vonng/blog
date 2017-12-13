# 制作OSX安装U盘

* 插入一个能用的8G或以上的U盘
* LaunchPad中打开“磁盘工具”，抹掉U盘，格式化为MacOS日志格式，为分区起一个好记的名字，如`OSX`

* 终端里键入
```bash
sudo /Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/U盘名 --applicationpath /Applications/Install\ OS\ X\ El\ Capitan.app --nointeraction
```

* Done

