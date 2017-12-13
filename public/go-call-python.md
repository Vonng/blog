---
title: "Go Call Python"
date: "2017-07-03"
author: "Vonng"
description: "Python是时髦的机器学习御用开发语言，Golang是大红大紫的新时代后端开发语言。Python很适合让搞算法的写写模型，而Golang很适合提供API服务，两位同志都红的发紫，这里就介绍一下正确搅基的办法。"
categories: ["Dev"]
featured: ""
featuredalt: ""
featuredpath: "/img/blog/go-python.png"
linktitle: ""
type: "post"
---



Python是时髦的机器学习御用开发语言，Golang是大红大紫的新时代后端开发语言。Python很适合让搞算法的写写模型，而Golang很适合提供API服务，两位同志都红的发紫，这里就介绍一下正确搅基的办法。

<!--more-->

![干他一炮.jpg](/img/blog/italy-canon.jpg)

## 原理

Python提供了丰富的[C-API](https://docs.python.org/2/c-api/)。而C和Go又可以通过cgo无缝集成。所以，直接通过Golang调用libpython，就可以实现Go调Python的功能了。确实没啥神奇，只要会用C调Python，马上就知道怎么用了。但问题是，如果有的选择，这个年代还有多少人愿意去裸写C和C++呢？诚心默念Golang大法好。



## 准备工作

* Python ：确保Python正确安装，所谓正确安装，就是在系统中能找到`libpython.so(dylib)`，找到`Python.h`。一般linux直接安装`python-devel`，mac直接用homebrew安装就可以。
* Golang安装：Golang不需要什么特殊的处理，能找到`go`即可。



## 安装libpython-go-binding

虽然直接用cgo调用libpython也不是不可以，但是有native-binding用起来肯定要爽的多。Github上有一个现成的Binding库[go-python](https://github.com/sbinet/go-python)。

```bash
 go get github.com/sbinet/go-python
```

如果Python安装正确，这里会自动编译并显示提示，事就这样成了。

## Have a try

首先写一个测试Python脚本

```python
import numpy
import sklearn

a = 10

def b(xixi):
    return xixi + "haha"
```

然后写一个Go脚本：


```go
package main

import (
	"github.com/sbinet/go-python"
	"fmt"
)

func init() {
	err := python.Initialize()
	if err != nil {
		panic(err.Error())
	}
}

var PyStr = python.PyString_FromString
var GoStr = python.PyString_AS_STRING

func main() {
	// import hello
	InsertBeforeSysPath("/Users/vonng/anaconda2/lib/python2.7/site-packages")
	hello := ImportModule("/Users/vonng/Dev/go/src/gitlab.alibaba-inc.com/cplus", "hello")
	fmt.Printf("[MODULE] repr(hello) = %s\n", GoStr(hello.Repr()))

	// print(hello.a)
	a := hello.GetAttrString("a")
	fmt.Printf("[VARS] a = %#v\n", python.PyInt_AsLong(a))

	// print(hello.b)
	b := hello.GetAttrString("b")
	fmt.Printf("[FUNC] b = %#v\n", b)

	// args = tuple("xixi",)
	bArgs := python.PyTuple_New(1)
	python.PyTuple_SetItem(bArgs, 0, PyStr("xixi"))

	// b(*args)
	res := b.Call(bArgs, python.Py_None)
	fmt.Printf("[CALL] b('xixi') = %s\n", GoStr(res))

	// sklearn
	sklearn := hello.GetAttrString("sklearn")
	skVersion := sklearn.GetAttrString("__version__")
	fmt.Printf("[IMPORT] sklearn = %s\n", GoStr(sklearn.Repr()))
	fmt.Printf("[IMPORT] sklearn version =  %s\n", GoStr(skVersion.Repr()))
}

// InsertBeforeSysPath will add given dir to python import path
func InsertBeforeSysPath(p string) string {
	sysModule := python.PyImport_ImportModule("sys")
	path := sysModule.GetAttrString("path")
	python.PyList_Insert(path, 0, PyStr(p))
	return GoStr(path.Repr())
}

// ImportModule will import python module from given directory
func ImportModule(dir, name string) *python.PyObject {
	sysModule := python.PyImport_ImportModule("sys") // import sys
	path := sysModule.GetAttrString("path")                    // path = sys.path
	python.PyList_Insert(path, 0, PyStr(dir))                     // path.insert(0, dir)
	return python.PyImport_ImportModule(name)            // return __import__(name)
}
```

打印输出为：

```bash
repr(hello) = <module 'hello' from '/Users/vonng/Dev/go/src/gitlab.alibaba-inc.com/cplus/hello.pyc'>
a = 10
b = &python.PyObject{ptr:(*python._Ctype_struct__object)(0xe90b1b8)}
b('xixi') = xixihaha
sklearn = <module 'sklearn' from '/Users/vonng/anaconda2/lib/python2.7/site-packages/sklearn/__init__.pyc'>
sklearn version =  '0.18.1'
```

这里简单解释一下。首先将这个脚本的路径添加到`sys.path`中。然后调用`PyImport_ImportModule`导入包

使用`GetAttrString`可以根据属性名获取对象的属性，相当于python中的`.`操作。调用Python函数可以采用`Object.Call`方法，，列表参数使用Tuple来构建。返回值用`PyString_AS_STRING`从Python字符串转换为C或Go的字符串。

更多用法可以参考[Python-C API文档](https://docs.python.org/2/c-api/object.html)。

但是只要有这几个API，就足够 Make python module rock & roll。充分利用Golang和Python各自的特性，构建灵活而强大的应用了。