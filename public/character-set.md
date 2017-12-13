---
title: "现代编码模型"
date: "2016-07-24"
author: "Vonng"
description: "字符集，编码，这些知识让很多基础不牢的程序员困惑不已。本文阐述了现代编码模型中的核心基本概念，并阐述了Python2中常见的字符编码问题的深层次原因。"
categories: ["Dev"]
featured: ""
featuredalt: ""
featuredpath: ""
linktitle: ""
type: "post"
---



# 现代编码模型
字符编码，在计算机导论中经常作为开门的前几个话题来讲，然而很多CS教材对这个话题基本都是走马观花地几页带过。导致了许多人对如此重要且基本的概念认识模糊不清。直到在实际编程中，尤其是遇到多语言、国际化的问题，被虐的死去活来之后才痛下决心去重新钻研。诸如此类极其基础却又容易被人忽视的的知识点还有：大小端表示，浮点数细节，正则表达式，日期时间处理等。本文是系列的第一篇，旨在阐明字符编码这个大坑中许多纠缠不清的概念。

<!--more-->

## 基本概念
现代编码模型自底向上分为五个层次：
* 抽象字符表(Abstract Character Repertoire)
* 编码字符集(Coded Character Set)
* 字符编码表(Character Encoding Form)
* 字符编码方案(Character Encoding Schema)
* 传输编码语法(Transfer Encoding Syntax)

[现代编码模型-Wiki](https://zh.wikipedia.org/wiki/%E5%AD%97%E7%AC%A6%E7%BC%96%E7%A0%81#.E7.8E.B0.E4.BB.A3.E7.BC.96.E7.A0.81.E6.A8.A1.E5.9E.8B "现代编码模型-Wiki")
[Unicode术语表](http://unicode.org/glossary/ "Unicode术语表")


## 抽象字符集 ACR
抽象字符集是现代编码模型的最底层，它是一个集合，通过枚举指明了所属的所有抽象字符。但是要了解抽象字符集是什么，我们首先需要了解什么是**字符**与**抽象字符**
#### 字符 (character, char)
字符是指字母、数字、标点、表意文字（如汉字）、符号、或者其他文本形式的书写“原子”。
例： `a`,`啊`,`あ`,` α`,`Д`等，都是抽象的字符。

#### 抽象字符(Abstract Chacacter)
抽象字符就是抽象的字符。(像是废话)
像`a`这样的字符是有形的，但在计算机中，有许多的字符是空白的，甚至是不可打印的。比如ASCII字符集中的NULL，就是一个抽象字符。
注意\x00,\000,NULL,0 这些写法都只是这个抽象字符的某种表现形式，而不是这个抽象字符本身。

#### 抽象字符集 ACR (Abstract Character Repertoire)
抽象字符集顾名思义，指的是**抽象字符的集合**。
已经有了很多[标准](http://www.iana.org/assignments/character-sets/character-sets.xhtml "标准")的字符集定义。
比如US-ASCII, UCS(Unicode), GBK这些我们耳熟能详的名字，都是(或者至少是)抽象字符集。

US-ASCII定义了128个抽象字符的集合。GBK挑选了两万多个中日韩汉字和其他一些字符组成字符集，而UCS则尝试去容纳一切的抽象字符。它们都是抽象字符集。
抽象字符 英文字母`A`同时属于US-ASCII, UCS, GBK这三个字符集。
抽象字符 中文文字`蛤`不属于US-ASCII，属于GBK字符集，也属于UCS字符集。
抽象文字 Emoji `😂`不属于US-ASCII与GBK字符集，但属于UCS字符集。

集合的一个重要特性，就是无序性。
集合中的元素都是无序的，所以抽象字符集中的字符都是**无序的**。

抽象字符集对应的就是python中的set的概念。
例：我可以自己定义一个字符的集合，叫这个集合为haha字符集。
`haha_acr = { 'a', '吼', 'あ', ' α', 'Д' }`

不过大家觉得抽象字符集这个名字太啰嗦，所以有时候就直接叫它们字符集了。

最后需要注意一点的是，字符集也是有开放与封闭的区分的。
ASCII抽象字符集定义了128个抽象字符，再也不会增加，这就是一个封闭字符集。
Unicode尝试收纳所有的字符，一直在不断地扩张之中。最近(2016.06)Unicode9.0.0已经收纳了128,237个字符，并且未来仍然会继续增长，这就是一个开放的字符集。

### 编码字符集 CCS (Coded Character Set)

```
Coded Character Set. A character set in which each character 
is assigned a numeric code point. Frequently abbreviated as 
character set, charset, or code set; the acronym CCS is also used.
```

**编码字符集**是一个每个所属字符都分配了**码位**的**字符集**。
编码字符集也经常简单叫做字符集。这是何等的卧槽，虽然从面向对象的角度讲，'子类对象'是一个'父类对象'这个表述是不错的，但这样随意叫无疑会把CCS与ACR搞混。

抽象字符集(Character set)是抽象字符的集合，而集合是无序的。
无序的抽象字符集并没有什么卵用，因为我们只能判断某个字符是否属于某个字符集，却无法方便地引用，指称这个集合中的某个特定元素。
`ASCII(编码)字符集中的0号字符`和`ASCII(抽象)字符集中的那个代表什么都没有的通常表示为NULL的抽象字符`这两种表述指称了同一个字符，但是哪个更方便呢？

所以为了更好的描述，操作字符，我们可以为抽象字符集中的每个字符关联一个**数字编号**，这个数字编号称之为**码位(Code Point)**。

通常根据习惯，我们为字符分配的**码位**通常都是非负整数，习惯上用十六进制表示。且一个编码字符集中字符与码位的映射是一一映射。

举个例子，为haha抽象字符集进行编码，就可以得到haha编码字符集。
`haha_ccs = { 'a' : 0x0, '吼':0x1 , 'あ':0x2 , ' α':0x3 , 'Д':0x4  }`
字符`吼`与码位`0x1`关联，这时候，在haha编码字符集中，`吼`就不再是一个单纯的抽象字符了，而是一个**编码字符(Coded Chacter)**，且拥有**码位(Code Point)** `0x1`。

因此：CCS = { k:i for i, k in enumerate(ACR)}
如果说抽象字符集是一个Set，那么编码字符集就可以类比为一个Dict。它的key是字符，而value则是码位。至于码位具体是怎样分配的，这个规律就不好说了。比如为什么我想给haha_ccs的`吼`字符分配码位`0x1`而不是`0x23333`呢？因为我觉得这样可以续一秒，说不定有的CCS就是这么粗暴呢。

最常见的编码字符集就是UCS (Universal Character Set)
	UCS. Acronym for Universal Character Set, which is specified by International Standard ISO/IEC 10646, which is equivalent in repertoire to the Unicode Standard.
下面的讨论主要围绕Unicode标准进行，毕竟ASCII能有什么好说的。

UCS就是统一字符集，就是由 ISO/IEC 10646所定义的编码字符集。通常说的“Unicode字符集”大体上指的就是它——统一字符集。不过Unicode本身指的是一系列用于计算机表示所有语言字符的**标准**。

举个UCS的例子吧，大家喜闻乐见的Emoji表情“😂”，在UCS中其码位为0x1F602。
(如果这个站点不支持Emoji，你就看不到这个字符了……)
```
>>> '😂'.decode('utf-8')
u'\U0001f602'
```

关于CCS，这些大概已经已经足够了，不过还有一个细节需要注意。
目前按照Unicode9.0.0的标准，UCS理论上收录了128,237个字符,也就是0x1F4ED个。不过在Mac下进行一些尝试，实际能用的最大的码位点在0x1F6D0 ，也就是128,720，竟然超过了收录的字符数，这又是为什么呢？
```python2
# Python2
>>> print u'\U0001F6D0'
🛐
>>> print u'\U0001F6D1'
🛑
```
**码位(Code Point)** 是非负整数没错，但这不代表它一定是连续分配的。
出现这种情况只有一个原因，那就是UCS的码位分配不是连续的，中间有一段空洞，即存在一段码位，没有分配对应的字符。

实际上，Unicode实际分配的码位是0x0000~0x0xD7FF与0xE000~0x10FFFF这两段的。中间0xD800~0xDFFF这2048个码位留作它用的，并不对应实际的字符。如果直接尝试去输出这个码位段的'字符'，结果会告诉你这是个非法字符。
```python
>>> print u'\UDDDD'
  File "<stdin>", line 1
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 0-5: truncated \UXXXXXXXX escape
```
* `0x0000~0xD7FF and 0xE000~0x10FFFF` 称为**Unicode标量值(Unicode scala value)**
* `0xD800~0xDBFF` 称为**Hign-surrogate**
* `0xDC00~0xDFFF` 称为**Low-surrogate**
  这样设计的原因，会在下一节字符编码表CEF中讲到。


## 字符编码表 CEF (Character Encoding Form)
	Unicode Encoding Form. A character encoding form that assigns each Unicode scalar value to a unique code unit sequence. The Unicode Standard defines three Unicode encoding forms: UTF-8, UTF-16, and UTF-32

现在我们拥有一个编码字符集了。
这个字符集中的每个字符都有一个非负整数**码位**与之一一对应。
看上去很好，既然计算机可以存储整数，而现在字符又可以表示为整数，我们是不是可以说，用计算机存储字符的问题已经得到了解决呢？

慢着！还有一个问题没有解决。
在讲抽象字符集ACR的时候曾经提起，UCS是一个开放字符集，未来可能有更多的符号加入到这个字符集中来。也就是说UCS需要的**码位**，理论上是无限的。
但是计算机的整形能表示的整数范围是有限的。譬如，一个字节的无符号整形(unsigned char, uint8)能够表示的码位只有0~0xFF，共256个；而一个无符号短整形(unsigned short, uint16)的可用码位只有0~0xFFFF，共65536个；一个整形(unsigned int, uint32)能表示的码位有0~0xFFFFFFFF，共4294967295个。

虽然说目前来看，UCS收录的符号总共也就十多万个。但谁知道哪天制定Unicode标准的同志们不会玩心大发，造几十亿个Emoji加入UCS中去。这是一对有限与无限的矛盾，必须通过一种方式进行调和。这个解决方案，就是字符编码表(Character Encoding Form)。

字符编码表是一个将**Unicode标量值(Unicode scalar value)**一一映射为**码元序列(Code Unit Sequences)**的映射。
之所以必须是一一映射，那是因为我们不光要编码，也要解码。
在Unicode中，指定了三种标准的字符编码表，UTF-8,UTF-16,UTF-32。分别将Unicode标量值映射为比特数为8、16、32的码元的序列。
即，UTF-8的码元为uint8, UTF-16的码元为uint16, UTF-32的码元为uint32。
当然也有一些非标准的CEF，如UCS-2,UCS-4，在此不多介绍。

* 码元
  Code unit: The minimal bit combination that can represent a unit of encoded text for processing or interchange.
  码元是能用于处理或交换编码文本的最小比特组合。通常计算机处理字符的码元为一字节，即8bit。同时因为计算机中char其实是一种整形，而整形的计算往往以计算机的字长作为一个基础单元，通常来讲，也就是4字节。Unicode定义了三种不同的CEF，分别采用了1字节，2字节，4字节的码元，正好对应了计算机中最常见的三种整形长度。

如何将一个无限大的整数，**一一映射**为指定字宽的码元序列。
这个问题可以通过变长编码来解决。
无论是UTF-8还是UTF-16，本质思想都是通过预留标记位来指示码元序列的长度。从而实现变长编码的。

举个例子：

| 样例字符 | 码位      | UTF-8码元序列           | UTF-16码元序列    | UTF-32码元序列 |
| ---- | ------- | ------------------- | ------------- | ---------- |
| A    | 0x41    | 0x41                | 0x0041        | 0x00000041 |
| 蛤    | 0x86E4  | 0xE8 0x9B 0xA4      | 0x86E4        | 0x000086E4 |
| 😂   | 0x1F602 | 0xF0 0x9F 0x98 0x82 | 0xDE02 0xD83D | 0x0001F602 |
(最下面那个是个Emoji大笑)
```python
>>> (u'A',u'A'.encode('utf-8'),u'A'.encode('utf-16be'),u'A'.encode('utf-32be'))
(u'A', 'A', '\x00A', '\x00\x00\x00A')
>>> (u'蛤',u'蛤'.encode('utf-8'),u'蛤'.encode('utf-16be'),u'蛤'.encode('utf-32be'))
(u'\u86e4', '\xe8\x9b\xa4', '\x86\xe4', '\x00\x00\x86\xe4')
>>> (u'😂',u'😂'.encode('utf-8'),u'😂'.encode('utf-16be'),u'😂'.encode('utf-32be'))
(u'\U0001f602', '\xf0\x9f\x98\x82', '\xd8=\xde\x02', '\x00\x01\xf6\x02')
```

各个CEF的细节我建议参看维基百科[UTF-8 ](https://zh.wikipedia.org/wiki/UTF-8 "UTF-8 ")与[UTF-16](https://zh.wikipedia.org/wiki/UTF-16 "UTF-16")，写的相当清楚，我就没必要在此再写一遍了。
更深入学习方式就是直接阅读[Unicode9.0.0 Standard](http://www.unicode.org/versions/Unicode9.0.0/)


## 字符编码方案 CES (Character Encoding Schema)
**Unicode encoding scheme**: A specified byte serialization for a Unicode encoding
form, including the specification of the handling of a byte order mark (BOM), if
allowed.

简单说，字符编码方案CES等于字符编码表CEF加上字节序列化的方案。
历史上字符编码方案(Character Encoding Schema)曾经就是指UTF(Unicode Transformation Formats)。所以UTF-X到底是属于字符编码方案CES还是属于字符编码表CEF，就成为了一个模棱两可的问题。

通过CEF，我们已经可以将字符转为码元(Code Unit)。无论是哪种UTF-X的码元，都可以找到计算机中与之对应的整形存放。那么现在我们能说存储处理交换字符这个问题解决了吗？
还不行。
因为从码元落实到底层的存储，还有一些问题需要解决。
假设一个字符按照UTF16拆成了A，B两个码元，那实际存储的时候究竟应该把A放在前面呢还是B放在前面呢？而另一个程序又如何知道当前这份文件是按照什么样的端序存储码元的呢？
无论是大端法与小端法的选择，还是用于决定编码字节序的标记，都是CES需要操心的方案。

所以Unicode实际上定义了7种字符编码方案CES：
* UTF-8
* UTF-16LE
* UTF-16BE
* UTF-16
* UTF-32LE
* UTF-32BE
* UTF-32
  其中呢，UTF-8因为已经采用字节作为码元了，所以实际上是不存在字节序的问题。其他两种CES嘛，都有一个大端版本一个小端版本，还有一个随机应变大小端带BOM的版本。

当然，这里也出现一个问题，UTF-X可以同时指代字符编码表CEF或者字符编码方案CES。UTF-8问题还好，因为UTF-8的字节序列化方案太朴素了，以至于CES和CEF都没什么区别。但其他两种：UTF-16,UTF-32，就比较棘手了。当我们说UTF-16时，既可以指代UTF-16字符编码表，又可以指代UTF-16字符编码方案。所以当有人说“这个字符串是UTF-16编码的”时，鬼知道他到底说的到底是一个（UTF-16 encoding form的）码元序列还是(UTF-16 encoding schema 的)带BOM序列化好的一串字节流。

简单的说，字符编码表CEF和字符编码方案CES区别如下：
c ∈ CCS ---CEF-->  Code Unit Sequence
c ∈ CCS ---CES-->  Byte Sequence

我们通常所说的动词**编码(Encode)**就是指使用CES，将CCS中字符组成的字符串转变为字节序列。而**解码(Decode)**就是反过来，将字节序列通过CES的一一映射还原为CCS中字符组成的序列。

注意这里的CCS不一定是UCS，比如也有可能是GBK，而CES也不一定是UTF-X，也可能是M$的一大堆CodePageXXX...。

下面给一个Python编码的小例子，说明CES的概念。
```python
#我的终端是UTF-8编码，所以输入字面量😂，其实输入的是其UTF-8字节流。
>>> s='😂'
>>> s
#Python解释器收到了😂的UTF-8编码字节流
'\xf0\x9f\x98\x82'
#print会往我的终端写回一样的字节流，终端是UTF-8编码，所以会打印Emoji
>>> print s
😂
# 对utf-8编码的字节流解码，得到UCS中的一个字符
>>> us = s.decode('utf-8')
>>> us
u'\U0001f602'
# 对UCS中的字符进行UTF-8编码
>>> us.encode('utf-8')
'\xf0\x9f\x98\x82'
# 对UCS中的字符进行UTF-16le编码
>>> us.encode('utf-16le')
'=\xd8\x02\xde'
# 对UCS中的字符进行UTF-16be编码，发现字节序反过来了
>>> us.encode('utf-16be')
'\xd8=\xde\x02'
# 对UCS中的字符进行UTF-16编码，发现默认使用小端序，添加BOM。
>>> us.encode('utf-16')
'\xff\xfe=\xd8\x02\xde'
# 对UCS中的字符进行UTF-32le编码，小端序。
>>> us.encode('utf-32le')
'\x02\xf6\x01\x00'
# 对UCS中的字符进行UTF-32le编码，大端序。
>>> us.encode('utf-32be')
'\x00\x01\xf6\x02'
# 对UCS中的字符进行UTF-32编码，默认小端序，添加BOM
>>> us.encode('utf-32')
'\xff\xfe\x00\x00\x02\xf6\x01\x00'
# Duang！编码失败，因为这个字符根本不是GBK字符集中的字符。
>>> us.encode('gbk')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'gbk' codec can't encode character u'\ud83d' in position 0: illegal multibyte sequence
# 现在我输入的是Unicode字面值。确实是一个UCS字符哟。而且也属于GBK字符集。
>>> u'蛤'
u'\u86e4'
# 这个属于GBK字符集的字符成功进行了GBK编码，变成了GBK CES的字节序列。
>>> u'蛤'.encode('gbk')
'\xb8\xf2'
# 编码完了，又解码回原来的UCS字符了。
>>> u'蛤'.encode('gbk').decode('gbk')
u'\u86e4'
```

## 传输编码语法(Transfer Encoding Syntax)
通过CES，我们已经可以将一个字符表示为一个字节序列。
但是有时候，字节序列表示还不够。比如在HTTP协议中，在URL里，一些字符是不允许出现的。这时候就需要再次对字节流进行编码。

著名的Base64编码，就是把字节流映射成了一个由64个安全字符组成字符集所表示的字符流。从而使字节流能够安全地在Web中传输。
不过这一块的内容已经离我们讨论的主题太远了。

# Python2中的编码问题
回到这个问题本身说白了，出现各种编码问题，无非就是哪里的编码设置出错了（好像是废话）
常见编码错误的原因有：
* Python解释器内码
* Python源文件文件编码
* Terminal使用的编码

## Python解释器内码
Python2解释器的内码是ascii（这是何等的卧槽）。
Java，C#，Python3, Javascript等语言内部的内码都使用UTF-16，Go语言的内码使用UTF-8。与之相比，默认使用ascii作为内码的python2简直是骨骼清奇。

python的字符串类型`str`实际上叫字符串，不如叫**字节串**，用下标去访问的每一个元素都是一个字节。
而其中`unicode`类型才是真正意义上的**字符串**，用下标去访问的每一个元素都是一个**字符**(虽然底下可能每个字符长度不同)。

根据上面的分析，对**字符串**(unicode,UCS字符组成的串)进行**编码** 得到**字节串**(str,字节流)，对**字节串**(str)进行**解码**得到**字符串**(unicode)。

所以，当Python的解释器内码是ASCII时，默认进行编码与解码的CES都是ASCII。
ASCII字符集范围为0~127而且码元固定为一字节，而普通的字节流也是码元一字节，但范围为0~255，这就麻烦了。

现在我想输入一个中文汉字(str)，并把它转成字符串(unicode)。 我输入的其实是一串UTF-8编码的字节流，因为我的终端是UTF-8编码的。
```python
>>> unicode('蛤蛤')
# unicdoe(<str>) 实质上是 <str>.decode('<PythonDefaultEncoding>')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8 in position 0: ordinal not in range(128)
```
因为我发送的中文实质上是utf-8编码的字节流，所以当decode时，ascii发现了超出127的字节，ASCII怎么可能编码出>127的字节呢？就认为这是是非法字节流从而报错。


现在反过来，我想把一个字符串(unicode)变成字节串(str), 我输入了一个unicode字面值蛤蛤，然而，Ops
```python
# str(<unicode>) 实质上是 <unicode>.encode('<PythonDefaultEncoding>')
>>> str(u'蛤蛤')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```
这里当我们对汉字Unicode进行Decode时，因为`蛤`并不属于US-ASCII字符集，所以自然不可能找到对应的编码，不能成功转换成字节。

这些问题都是因为Python默认的内码，不知道坑了多少人。
有一种粗暴的解决方案，就是reload(sys);sys.setdefaultencoding('utf-8')
这段代码的工作机理是修改Python解释器的默认内码为utf-8。因为很多情况下，特别是互联网上的数据基本以utf-8编码最为常见。所以很多问题就这么‘巫毒’的解决了。不过我个人非常反对这种方法，有一些难以察觉的副作用。

## Python源代码文件
Python源代码文件默认的编码也是ASCII（也是醉了）。
所以Python源代码文件中如果出现其它字符集的字符……嗯……，就会报错。
解决方案是在源代码头上加上#coding: xxx表明我这个文件到底是用什么编码存的。

## Terminal使用的编码
终端呢，它向shell发送的是字节流，收到的也是字节流。如何解释这些字节流，依赖于终端自己的编码设置。
中文Windows下的CMD好像用的是GBK。而Mac和Linux的Terminal基本都是UTF-8。

与此同时，Python向stdout输出时，还会根据sys.stdout.encoding以及一系列的环境变量等决定如何把内部的字符串(Unicode)编码成字节流发送回终端。

如果手贱改了那些LOCALE设置，环境变量之类的，或者sys.stdout.encoding与终端的编码不匹配，那么Python的输出当然会是一堆乱码了。