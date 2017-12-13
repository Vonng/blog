---
title: "如何渲染Markdown与MathJax"
date: "2017-11-23"
author: "Vonng"
description: "修改Markdown编译器，提供MathJaX支持"
categories: ["Dev"]
tags: ["LaTeX", "Go", "Compiler"]
featured: ""
featuredalt: ""
featuredpath: "/img/blog/latex.jpg"
linktitle: ""
type: "post"
---



最近重修了一遍个人博客，从自己撸的动态站点改成了静态生成器。期间最为困扰的一个问题，就是如何让Markdown与LaTeX和平共处。网上的开源方案多少有不尽如意之处，所以最后还是自己造了轮子。

<!--more-->



## 需求

​	有相当数量的本地Markdown编辑器提供了对LaTeX的支持，包括[Typora](https://www.typora.io/)，MWeb等等，在线的有StackEdit等。使用体验相当好。平时我在本地主要用Typora写笔记、邮件、文章，非常好用。我就想能不能把个人博客也改成静态Markdown博客？这样用Typora写的带公式的笔记，就可以无缝发布为博客，非常方便。

​	目前Markdown站点静态生成器比较知名的主要有 hugo(go)，hexo(node)，Jekyll(ruby)。ruby不熟忽略；node.js用着感觉太挫，go用的比较顺手，所以准备试试[hugo](http://gohugo.io/)。一个还算挺有名的静态生成器，作者是google的spf13，有一些知名的go项目：cobra和viper。所以第一感觉，质量还是应该比较信得过的。

​	不过实际用起来就会发现它的巨大的蛋疼之处了：对于数学公式非常不友好。正常的LaTeX公式使用`$`作为行内公式界定符，`$$`作为块公式界定符。而hugo要求使用`<div>`或者反引号把公式包起来，这就破坏了公式在本地编辑器的显示效果。在本地编辑器显示良好的文档，一旦使用hugo渲染就变得一塌糊涂。虽然说可以写个hook脚本在build静态站点前做自动转换，这无疑要逼死强迫症和代码洁癖患了。

​	我提了个Issue但没人鸟，几个Contributor觉得这算Feature不算Bug。好吧，拥抱开源一定要有自己撸起袖子下场干的觉悟，我来亲自来Fix它！



## 目标

​	绝大多数MD编辑器，在线也好，离线也罢，LaTeX支持都是通过MathJax实现的。也有一些使用KaTeX的，例如Editor.md。不过KaTeX的功能不全，例如矩阵就没法很好的渲染。所以这里只考虑MathJax。

目前能够完美渲染带公式Markdown的Render，首推Pandoc，一行命令解决烦恼：

```bash
pandoc mydoc.md --mathjax --to=html > mydoc.html
```

只要在渲染出的HTML中简单引入`MathJax.js`和`Highlight.js`，用CSS微调一下格式，就是一篇相当美观的文档了。引入的JS可以由CDN提供：

```
"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS_CHTML-full"
"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"
```

Pandoc也有美中不足的地方，它是用haskell写的，语言都没有很好的binding可用。直接用shell命令来调用虽然不是不可以，但实在是过于土鳖。

但是，Pandoc的输出格式可以作为很好的生成目标。



## 定位问题

`hugo`使用 [blackfriday](https://github.com/russross/blackfriday)作为Markdown渲染后端。经过定位，问题的根源在于 blackfriday 。

blackfriday是一个Markdown编译器，将Markdown文本编译为HTML文档。其根本问题在于：

* 前端Parser没有识别出`$`界定的公式元素，所以LaTeX语法在处理中会受到Markdown和其他一些扩展功能（例如 Smartypants）的侵入与干扰：最典型的问题就是LaTeX中遍地都是的下划线`_`，就被解释成了Markdown中的下标。生成了`<em>`标签破坏了公式。又比如Smartypants扩展会对普通文本做一些自作聪明的处理，例如自动将(r)生成®，一些公式也因此不知不觉变样了。
* 后端Render对于数学公式元素只是使用简单的`<p>`元素渲染，没有标记`class="math display/inline"`，所以无法被MathJaX精准识别。导致样式显示出现一些问题。


那么这个问题就变为修改Markdown编译器的问题了。具体修改内容可以参考：[Commit: Add MathJax Support](https://github.com/Vonng/blackfriday/commit/4e5da679f1a83b9cafd86daa94e646142482ef72)。



## 解决问题

这个问题可以分成四个子任务：

* 修改API，添加新的选项，包括新Extension选项`MathJaxSupport`和渲染选项`MathJaxFromCDN`。


* 为AST添加两种新的节点类型：`inlineMath`和`blockMath`，分别表示行内公式和块级公式两种元素。
* 修改Parser逻辑，识别`$`和`$$`并生成AST上相应的`inlineMath`,`blockMath`节点。
* 修改Renderer逻辑，合适地渲染`inlineMath`与`blockMath`节点。

其中，主要是修改Parser和Render

### 修改Parser

首先修改的是Parser，扩展的Markdown语法已经有现成的标准，只要为现成的Parser加上两种新节点的解析逻辑即可。

Handler的函数签名为：

```go
func Handler(p *Markdown, data []byte, offset int) (int, *Node)
```

其中`data`是输入的全部Markdown文本，`offset`是当前游标指向输入的偏移量。处理函数需要根据接下来的文本生成AST中的相应元素，如果生成了元素，返回值中的`int`就包含了吞掉的文本数量，`*Node`就是新生成的元素节点。

`inline math parser`由行内的`$`触发，如果发现这个`$`其实是`$$`，就什么都不做，交给`block math parser`来处理。如果后向探查到配对的`$`，就吞掉这一段Token流，生成一个`inline math`节点。

```go
// math handle inline math wrapped with '$'
func math(p *Markdown, data []byte, offset int) (int, *Node) {
	data = data[offset:]

	// too short, or block math
	if len(data) <= 2 || data[1] == '$' {
		return 0, nil
	}

	// find next '$'
	var end int
	for end = 1; end < len(data) && data[end] != '$'; end++ {
	}

	// $ not match
	if end == len(data) {
		return 0, nil
	}

	// create inline math node
	math := NewNode(Math)
	math.Literal = data[1:end]
	return end + 1, math
}
```

`block math parser`属于块级元素，由行首（允许若干先导空白字符）的`$$`触发，如果后向探查到配对的`$$`，同理也生成一个`block math`节点。

```go
// blockMath handle block surround with $$
func (p *Markdown) blockMath(data []byte) int {
	if len(data) <= 4 || data[0] != '$' || data[1] != '$' || data[2] == '$' {
		return 0
	}

	// find next $$
	var end int
	for end = 2; end+1 < len(data) && (data[end] != '$' || data[end+1] != '$'); end++ {
	}

	// $$ not match
	if end+1 == len(data) {
		return 0
	}

	// render the display math
	container := p.addChild(MathBlock, 0)
	container.Literal = data[2:end]

	return end + 2
}
```

### 修改Renderer

渲染器的修改相对简单的多。只要为两种数学公式节点配置相应的HTML Tag即可。MathJaX渲染会使用CSS类`.math`，行内公式额外使用`.inline`，块级公式额外使用`.display`

```go
mathTag            = []byte(`<span class="math inline">\(`)
mathCloseTag       = []byte(`\)</span>`)
blockMathTag       = []byte(`<p><span class="math display">\[`)
blockMathCloseTag  = []byte(`\]</span></p>`)
...
case Math:
   r.out(w, mathTag)
   escapeHTML(w, node.Literal)
   r.out(w, mathCloseTag)
case MathBlock:
   r.out(w, blockMathTag)
   escapeHTML(w, node.Literal)
   r.out(w, blockMathCloseTag)
```



### hugo的修改

修改后的blackfriday fork地址为：[Vonng/blackfriday](https://github.com/Vonng/blackfriday)， 默认Master分支是v2。

给原Repo提了PR，不过看上去作者已经失联很久了……

hugo默认使用blackfriday第一版，所以这里顺便就fork一份做了升级适配。里面全换成我的blackfriday fork了，所以我也没好意思提PR给hugo。地址在：[Vonng/hugo](https://github.com/Vonng/hugo)下载下来得改名成原repo才能用，即github.com/gohugoio/hugo。

终于，绕了一大圈之后，Hugo终于能完美渲染MathJax公式啦，本博客就是用自制版hugo和blackfriday搞的。说起来这还是学完编译原理后第一次直接用来解决现实问题，还是蛮爽的。
