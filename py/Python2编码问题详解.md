# Python2字符串问题详解

## Python2的字节串
`Python2`使用`'xxx'`作为**字节串字面值**，其类型为`<str>`，但`<str>`本质上是**字节串**

我的终端是UTF-8编码，所以在终端键入字面值😂 ，实质输入的是字面值的字节序列`\xf0\x9f\x98\x82`。

`Python2`解释器接收到这个字节序列，并原样存储到变量s中。

```python
s='😂'
```

当我们打印`repr(s)`时，会打印变量s的内部表示，即**字节串**`\xf0\x9f\x98\x82`。它的类型为`<str>`，即**字节流**

当我们使用print打印一个字节串`<str>`本身时，`python2`会原封不动地将这个字节串输出到stdout。

因为我的终端编码为UTF-8，所以这个UTF-8编码的字节串`s`会被终端使用`utf-8`解码，打印出原样的抽象字符😂

```python
print repr(s), type(s), s
```
```
'\xf0\x9f\x98\x82' <type 'str'> 😂
```

# Python2的字符串
`Python2`使用`u'xxx'`作为**字符串字面值**，其类型为`<unicode>`，`<unicode>`是真正意义上的**字符串**，每一个字符都属于UCS。

输入字面值的字节序列`\xf0\x9f\x98\x82`，但因为表明了这是一个**字符串字面值**，`python2`会将其自动解码为Unicode，存储入变量`us`中。

```python
us = u'😂'
```

当我们打印`repr(us)`时，会打印变量`us`的内部表示，即**字符串**`u'\U0001f602'`。它的类型为`<unicode>`，包括了一个`<unicode>`字符。

当我们使用`print`打印一个`<unicode>`字符串本身时，`python2`会使用系统调用，将这个**字符串**直接写回到控制台窗口，原样打印出😂

```python
print repr(us), type(us), us
```
```
u'\U0001f602' <type 'unicode'> 😂
```


## 字符串和字节串的关系
`s`是一个**字节串**，其内容为`utf-8`编码的字符😂 ,即`\xf0\x9f\x98\x82`
`us`是一个**字符串**，其内容为字符😂 本身。所以`s != us`。
但如果我们对`s`这个字节流进行**`utf-8`解码**，就可以得到字符串`us`。
同理，对`us`这个字符串进行**`utf-8`编码**，就可以得到字节串`s`

```python
s.decode('utf-8') == us, us.encode('utf-8') == s,s == us
```
```
UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal      
(True, True, False)
```


## 字符串和字节串的转换

这个地方是问题最多的地方了。

### 1. 字符串 to 字节流

我们有一个字符串😂 ，现在我想把它转换成字节流，怎么办？

大多数新手想当然的想到的第一个办法自然是`str(us)`，来个“强制类型转换”吼不吼啊？

可惜`str(us)`并不是那么简单的，在背后，实际执行的是：

```python
us.encode(sys.getdefaultencoding())  
# Which is 
us.encode('ascii')
```

当字符串中只有ASCII字符时，这样做是可以的。但一旦含有其他非ASCII字符，就会出错！因为非ASCII字符无法进行ASCII编码。


```python
print str(u'a'), repr(str(u'a')), type(str(u'a'))
print str(us)
```
```
    a 'a' <type 'str'>
    UnicodeEncodeErrorTraceback (most recent call last)

    <ipython-input-6-d1193c5a8063> in <module>()
          1 print str(u'a'), repr(str(u'a')), type(str(u'a'))
    ----> 2 print str(us)
    

    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```

### 2. 字符串 to 字节流

我们有一个字节流`\xf0\x9f\x98\x82`，当然就是😂 的utf-8编码。现在我想把它转成一个**真正的字符**，怎么办？

同理，很多人想当然的也准备来一个“强制类型转换”：`unicode(s)`。

在背后，实际执行的是：

```python
s.decode(sys.getdefaultencoding())  
# Which is 
s.decode('ascii')
```

当字节流中只有0~127的字节时，也就是原来的字符串中只有ASCII字符，这样做是可以的。如若不然，ASCII解码器会认为这是个非法ASCII编码字节流而报错。


```python
print unicode('a'), repr(unicode('a')), type(unicode('a'))
print unicode(s)
```
```
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xf0 in position 0: ordinal not in range(128)
```

所以，当我们需要对字符串和字节串进行相互转换时，不要使用这种方式，而应当使用更科学的方法，也就是`decode`与`encode`方法。

## 对字节串的解码(Decode)

**解码(Decode)**是定义在字节串`<str>`上的操作。

使用正确的**编码方案(CES)**对**字节串**解码可以获得对应的**字符串**，但如果使用了错误的CES进行**解码** ，就会出现**乱码** 甚至直接报错。

例1中，使用`gbk`编码对字节串`s`解码，因为GBK为双字节编码，所以s正好四个字节，瞎猫碰上死耗子，解码成功。可惜解出来的是没有意义的乱码。

例2中，这回我们换一个字符，`'蛤'`在`utf-8`下编码成三个字节`\xe8\x9b\xa4`,在GBK编码看来，每个GBK字符都会编码成两个字节，出现单个的字节需要解码，一定是哪里出错了，所以就报了解码错误

例3中，使用另一种编码`ascii`对字节串`s`解码，因为`\xe8\x9b\xa4`中出现了大于0x7F的字节，ASCII认为这不是一个合法的ASCII编码字节串应该出现的字节，所以也报了解码错误。


```python
print repr(s),s.decode('gbk')
```
```
'\xf0\x9f\x98\x82' 馃槀
```

```python
print repr('蛤'),'蛤'.decode('gbk')
```

```
'\xe8\x9b\xa4'
    
UnicodeDecodeError: 'gbk' codec can't decode byte 0xa4 in position 2: incomplete multibyte sequence
```


```python
print repr(s),s.decode('ascii')
```
```
'\xf0\x9f\x98\x82'
UnicodeDecodeError: 'ascii' codec can't decode byte 0xf0 in position 0: ordinal not in range(128)
```

### 对字符串`<unicode>`的'解码'

**解码(Decode)**只能对**字节串`<str>`**进行。对**字符串`<unicode>`**解码毫无意义。
虽然这么做也是可以的……
例如

```python
>>> u'abc'.decode('utf-8')  # 对unicode字符串去解码，简直有毛病。但在纯ascii环境下也没什么问题。
u'abc'
>>> us.decode('utf-8')      # 可惜一旦出现非ASCII字符，这种行为就会付出代价……

Traceback (most recent call last):
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
```

为什么会发生这个问题呢？因为对字符串`<unicode>`进行解码前，`python2`会认为这是一个愚蠢的动作，自作聪明的帮你先把这个字符串使用Python默认的编码方案转成**字节流`<str>`**，然后再进行解码。

```python
<unicode>.decode(<encoding>) = 
<unicode>.encode(<PythonDefaultEncoding>).decode(<encoding>)
```

# 对字符串的编码(Encode)
考察了**解码**之后，我们来考察一下**编码(Encode)**。**编码**是发生在**字符串`<unicode>`**上的操作。

这里我们对字符串`us`：😂  使用不同的CES进行编码，我们会得到一系列不同的字节流。当然，这些CES都是Unicode标准定义的CES。


```python
for encoding in ['utf-8','utf-16be','utf-16le','utf-16','utf-32be','utf-32le','utf-32']:
    print "%-10s\t%s"%(encoding,repr(us.encode(encoding)))
```

     utf-8     	'\xf0\x9f\x98\x82'
    utf-16be  	'\xd8=\xde\x02'
    utf-16le  	'=\xd8\x02\xde'
    utf-16    	'\xff\xfe=\xd8\x02\xde'
    utf-32be  	'\x00\x01\xf6\x02'
    utf-32le  	'\x02\xf6\x01\x00'
    utf-32    	'\xff\xfe\x00\x00\x02\xf6\x01\x00'


我们不禁好奇，如果使用其他的CES进行编码，会发生什么。首先试一试对字符串😂 进行GBK编码。

因为字符😂 并不属于GBK字符集，所以GBK编码器一脸懵逼，我怎么可能对不属于自己字符集的字符进行编码呢？


```python
us.encode('gbk')
```
```
UnicodeEncodeError: 'gbk' codec can't encode character u'\ud83d' in position 0: illegal multibyte sequence
```

但是换句话说，如果一个UCS字符集中的字符同时也属于GBK字符集，比如说汉字“蛤”，那么就可以使用GBK编码了！


```python
uha =  u'蛤'
print uha,type(uha),repr(uha.encode('gbk'))   #可以，这很GBK！
print uha.encode('gbk')                       #不行，虽然GBK编码成功，但是我的终端是UTF-8的，认不出GBK编码的字节流来。
```

    蛤 <type 'unicode'> '\xb8\xf2'
    ��


### 对字节串`<str>`的'编码'
另一方面，我说过**编码(Encode)**只能对**字符串`<unicode>`**进行。但是有的同学不服，看，我对`<str>`也可以解码成功哟~


```python
'abc'.encode('utf-8'),'abc'.encode('utf-16be'),'abc'.encode('gbk')
```




    ('abc', '\x00a\x00b\x00c', 'abc')



之所以可以这样，是因为当`python2`对`<str>`进行**编码(Encode)**操作时，会首先对**字节流<str>**进行**解码**

解码时使用的编码乃是Python2内部默认编码方案，也就是`US-ASCII`` （卧槽！！！）

也就是说，如果这个**字节流<str>**中只有ASCII字符，其实是可以对`<str>`直接**'编码'**的。

但如果这个字节流并不只有ASCII字符，在**编码**之前的**解码**中，就会出错！

因为同“对字符串`<unicode>`解码”这个问题一样，对字节串`<str>`编码实质上是：

```python
<str>.encode(<encoding>) = 
<str>.decode(<PythonDefaultEncoding>).encode(<encoding>)
```


```python
'续命'.encode('utf-8')
```
```
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 0: ordinal not in range(128)
```

# 坑爹的Python内部默认编码

但是！如果我们修改Python内部的默认CES为`utf-8`，同样的问题竟然不报错了！

这说明了，当对`<str>`进行编码时，`python2`首先会使用内部默认的CES，也就是`ASCII`进行解码后再进行编码！。

所以当我们修改了`python2`解释器的内部默认CES为`utf-8`后，这个`字节串<str>`竟然可以直接'编码'了。

这种巫毒编程方式可以“解决”很多编码问题，因为互联网上很多数据都是UTF-8编码的。但是不！要！这！样！做！

```python
In [1]: import sys;reload(sys);sys.setdefaultencoding('utf-8')  # Dirty Hack !!!

In [2]: '续命'.encode('utf-8')      # 本来应该报错的！
'\xe7\xbb\xad\xe5\x91\xbd'

In [3]: u'续命'.decode('utf-8')     # 无法直视！
u'\u7eed\u547d'
```

# 坑爹的Python源文件默认编码

在上面一个例子中，可能有同学会尝试把代码放到文件里运行。例如：

```bash
echo "import sys;reload(sys);sys.setdefaultencoding('utf-8')" >> shit.py
echo "'续命'.encode('utf-8')" >> shit.py
python shit.py
```

结果编码错误出没出还不知道，竟然先给我报了个语法错误！

```
  File "shit.py", line 2
SyntaxError: Non-ASCII character '\xe7' in file shit.py on line 2, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
```
这是因为**Python源文件**默认的编码J竟然也是`US-ASCII`。现在里面竟然出现了中文字符！不行，这不ASCII，得报错！

解决方案是在源文件头部加上一句

```
# -*- coding: utf-8 -*-
```
当然你也可以用别的编码，比如中文windows下很可能你就会写

```
# -*- coding: gbk -*-
```

```python
for encoding in ['utf-8','utf-16be','utf-16le','utf-16','utf-32be','utf-32le','utf-32']:
    print "%-10s\t%s"%(encoding,repr(us.encode(encoding)))
```

    utf-8     	'\xf0\x9f\x98\x82'
    utf-16be  	'\xd8=\xde\x02'
    utf-16le  	'=\xd8\x02\xde'
    utf-16    	'\xff\xfe=\xd8\x02\xde'
    utf-32be  	'\x00\x01\xf6\x02'
    utf-32le  	'\x02\xf6\x01\x00'
    utf-32    	'\xff\xfe\x00\x00\x02\xf6\x01\x00'


UTF8将😂 编码成了四个字节`0xF0 0x9F 0x98 0x82`。

UTF-16BE是大端编码，所以被编码为`0xD8 0x3D 0xDE 0x02`

UTF-16LE是小端编码，所以每个二字节的码元内大小字节排列次序正好相反，编码为`0x3D 0xD8 0x02 0xDE`

UTF-16默认采用小端编码且带BOM，所以编码为`0xFF 0xFE 0x3D 0xD8 0x02 0xDE`。 `0xFFFE`是BOM，代表小端序。

UTF-32与UTF-16基本同理。





