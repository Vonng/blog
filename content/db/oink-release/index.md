---
title: "OINK：文档框架这件事，折腾了六年，终于靠 Codex 毕业了"
linkTitle: "OINK 文档框架"
date: 2026-08-10
authors: [vonng]
summary: >
  在八套方案之间折腾六年后，我终于用 Codex 把 Docsy 的工程能力、Fumadocs 的现代体验和 Hugo 的简单交付合成了 OINK。
tags: [Codex, 文档, 开源]
---

> 做一个文档网站并不难，难的是让它五年之后依然好用。

最初，你只想把几份 Markdown 放到网上。

后来，需求开始自己生长：全文检索、深色模式、多语言、多版本、API 文档、流程图、终端录像、移动端适配、SEO、RSS、评论、访问统计、打印导出……

再往后抬头一看，你已经在维护一套前端工程了：Node.js、npm、PostCSS、几十个依赖包，还有一堆不知道哪天会失效的 CDN 链接。

**文档本来是用来降低项目维护成本的，最后自己却变成了一个需要维护的项目。**

这就是我做 [Oink](https://oink.pgsty.com/zh/) 的原因。

![OINK 中文文档首页](oink-docs.webp)

![OINK 项目首页](oink-home.webp)

![OINK 博客页面](oink-blog.webp)


## 一、六年，八个方案，没一个满意的

这些年，我在文档框架上花的时间可不少。文档是一个开源项目的门面——用户在下载你的软件之前，往往先看到它的文档站。门面这个东西，你可以说它不重要，但不能让它难看。而我试过的方案，大概能列出一份考古清单：

- **[Docsy](https://www.docsy.dev/)**：功能最全面的一个，Google 基于 Hugo 开发的主题框架。许多耳熟能详的云原生项目都在使用它，几乎可以算 CNCF 项目的标准选择。五六年前，我第一次给 Pigsty 搭文档站，用的就是它。
- **Docsify**：纯 JavaScript 加 Markdown，轻量到几乎没有构建步骤，代价是 SEO 和首屏体验。
- **Docusaurus**：React 生态的标配，功能齐全，但你从此接手了一整个 Node.js 项目。
- **Hugo + Hextra**：足够快，也足够简单，小站不错，但功能面不太够大型工程文档站使用。
- **Mintlify 等 SaaS**：审美与设计拉满而且省事，但是要钱也不便宜，而且你的文档从此托在别人手里，没法离线交付。
- **[Next.js + Fumadocs](https://fumadocs.dev/)**：极佳的前端审美，接近 Mintlify。但问题是全文检索慢，构建慢，内容使用 MDX 而不是纯 Markdown，想做成纯静态站也颇费周折，还依赖一大坨 Node.js 和 Next.js 的东西。

![采用 Fumadocs 的 Pigsty 文档站](fumadocs.webp)

其他很多方案，我也都尝试过，Ruby 的 jekyll，Python 的 sphinx，还有 Pelican，甚至是用 editor.js 自己糊的版本。很多方案都有自己独特的优点，但是没有一个让我真正感到满意。折腾来，折腾去，大把时间花在了没用的地方。

最后兜兜转转绕了好几圈，老冯还是回来继续用最开始选择的 Docsy。这个文档框架功能是最完备的，导航，编辑，打印，博客，多语言，多版本，SEO，全文检索，离线交付

然而，它也有缺点 —— 太丑了，而且依赖繁多。

![采用 Docsy 的旧版 Pigsty 文档站](docsy.webp)

为了在 Hugo 上支持这么多功能，Docsy 硬生生塞进了一整套前端工具链：npm、`node_modules` 全家桶、用 PostCSS 预处理 SCSS，还有 Autoprefixer。Hugo 本来主打的是 “一个二进制就能跑”，被这么一套下来，构建、预览和维护全都变得复杂了 —— 甚至你都没法用 Cloudflare Pages 来自动构建，得先在 GitHub Actions 里跑一遍 CD 构建完才行 —— 就为了一个静态文档站。

所以这就很尴尬，最好看的缺胳膊少腿，功能最全的那个又丑又麻烦。

So，为什么不自己写一个？我确实多次有过这种想法，但真的是没空。前端这些东西非常耗费精力，折腾起来费劲，而且跟我的主业没啥关系。我是数据库老司机，不是前端工程师。为了一个文档主题去折腾 CSS JS  JavaScript，这笔账我算了六年，每次都算不过来。






## 二、直到前端交付变成了可以按需购买的商品

从上个月开始，这笔账突然算得过来了。

顶级的前端设计与实现能力，变成了一种按 token 计费的通用商品。我不需要成为前端工程师，只需要 **清楚地知道自己想要什么** ——而这件事我想了六年，早已想得非常清楚。

于是，我第一次可以用“许愿”的方式把它做出来：

> 我要 Docsy 的完整功能集，缝上 Fumadocs 和 Nextra 的前端审美，加上工程文档真正需要的那些能力，再把乱七八糟的依赖统统扔掉——一个干净的 Hugo Extended 二进制就能构建、就能运行。

诚实地说，这是我借助 Codex 和其他 AI 工具完成的。但它和那些玩票性质的 vibe coding 不一样：**AI 没有替我制造这个需求，需求已经在那里摆了六年。AI 做的事情，是把“值得动手”的门槛大幅降低。**

前几天有人问我，你那七个 AI 订阅每天烧掉那么多 token，到底烧出什么来了？

这就是其中一个。整套框架加上六七个文档站，前后大概只花了两三天——甚至因为真正的大活儿太多，我一直没抽出时间写这篇文章。


## 三、为什么叫 OINK？

OINK 在英语里是猪叫声。

我的主力开源项目叫 Pigsty，也就是“猪圈”。这两年围绕它长出来的一系列组件，也都跟猪脱不了关系：

- **Pig** —— 包管理器，小猪；
- **Sow** —— 仓库管理器，母猪，同时也有“播种”的意思；
- **Boar** —— 图形管控平台，野猪；
- **Silo** —— 对象存储，农场里的谷仓。

猪圈里已经有三头猪了。文档项目总不能再抓一头猪进来，那就让这几头猪 **叫出来** ——它们的内容，最后都通过 OINK 表达出去。

另一层双关是，OINK 里面藏着 **ink**，也就是墨水，和文档的关系正合适。

再正经一点，这四个字母还真能凑出一个说得过去的缩写：

> **Open · Indexed · Navigable · Knowledge**
>
> 开放、可索引、可导航的知识。

![OINK 的工具与组件展示](toolkit.webp)


## 四、砍掉的部分：消费端只依赖 Hugo

OINK 最重要的设计决定，是把 **消费端站点的构建边界收缩到 Hugo Extended**。

一个站点的生产构建命令只有这一条：

```bash
hugo
```

没有 `npm install`，没有 PostCSS，没有 `node_modules`，构建时也不需要从公共 CDN 拉取运行时。

Bootstrap、Font Awesome、字体、Lunr 搜索、Mermaid、KaTeX、Markmap、Swagger UI、Redoc、Asciinema、ECharts 和 Infographic，这些资源全部跟随主题源码本地交付。

好处很朴素：构建可复现，供应链可审计，内网和网络隔离环境也容易交付。我自己做离线文档分发时，文档需要在断网环境中能翻、能查——对我来说，这是必备能力，不是加分项。

拿到完整主题后，Hugo 会把内容、配置、布局和资源一次性编译到 `public/` 目录。之后，无论扔到对象存储、GitHub Pages、Cloudflare Pages、Nginx 还是内网文件服务器上，托管层都不需要知道 OINK 是什么。


## 五、加上的部分：一套现代文档外壳

传统 Hugo 主题经常给人一种“能用，但像十年前”的感觉。OINK 想在保留 Hugo 简单交付的同时，把现代文档产品该有的东西补齐：

- 全局导航、面包屑、可折叠并且可调整宽度的侧栏；
- 页面目录、阅读元数据、上下页导航、编辑与反馈入口；
- 深浅色模式、版本选择器、打印视图和移动端操作面板；
- RSS、SEO、canonical、`hreflang` 与 Open Graph 元数据；
- 本地全文检索（`⌘K`），以及可选的 Algolia 和 Google 托管搜索；
- 博客、分类、标签、评论、特色图片与多语言信息架构。

[OINK 0.2.0](https://oink.pgsty.com/zh/blog/release/0.2.0/) 的首页也不再是一份“必须复制出来才能修改”的 HTML 模板。它提供了 **12 种可组合分区**：Hero、指标、能力叙事、原则、卡片、Logo 墙、画廊、用户评价、贡献者、FAQ、自由 Markdown 与 CTA。站点只需在 `data/home/<language>.yaml` 中声明顺序和内容，就能重排、复用甚至删掉首页模块。

这条边界很重要：**配置应该表达站点想要什么，而不是暴露主题内部是怎么拼装的。**

顺便说一个我特别在意的优化。站点变大后，全文检索索引可能有十几兆。以前，我有一个网站每月产生八百多 GB 流量，其中一大半就是被这个索引吃掉的。现在，首页加载时不再下载索引，只有等用户真正按下搜索框时才首次加载。流量账单和用户体验，居然成了同一个方向的优化。

![使用 Hugo 构建 OINK 双语站点](build.webp)


## 六、工程内容，不该退化成截图

工程文档不只有文字和代码块。

一个数据库或基础设施项目，经常需要终端演示、架构图、时序图、性能图表、数学公式、API 参考、信息图，以及可交互的参数说明。过去，这些能力散落在各个站点自己的短代码中，复制到下一个项目后再改一遍。

OINK 把已经证明通用的组件整理成了稳定的创作接口：

- **Asciinema** 终端录像；

![OINK 的 Asciinema 终端录像组件](terminal.webp)

- **Apache ECharts** 数据图表与 **AntV Infographic** 信息图；
- **Mermaid**、**KaTeX**、**Markmap**、PlantUML 和 Diagrams.net；
- **Swagger UI** 与 **Redoc** API 文档；
- 步骤、标签页、折叠块、卡片、卡片组和文档轮播；
- Docsy 原有的 alert、include、readfile、image 和 blocks 等能力。

评论系统还支持读者使用 GitHub 账号登录。

![使用 GitHub 账号登录的评论区](comments.webp)

关键在于：**这不是把一整套前端运行时塞进每个页面。** 短代码渲染时会在 Hugo 的页面状态中标记自己，资源组装阶段再检查标记。只有用到 ECharts 的页面才加载 ECharts，同一页出现十张图也只加载一次。一篇纯文字文章，不会因为主题“支持很多功能”就背上所有运行时。

这也是我对“功能丰富”的理解：不是让每个页面都携带全部能力，而是让作者随时可用，让读者只为当前页面真正需要的能力付出下载成本。

![OINK 在移动端的文档导航](mobile.webp)


## 七、多语言不是复制一个 `/zh` 目录

OINK 的语言模型直接建立在 Hugo 的多语言页面对象上，不从域名或硬编码 URL 猜测语言。

只有一种语言时，语言选择器会自动隐藏；配置两种或更多语言时，按钮按照权重切换，完整菜单列出所有语言。当前页面缺少目标译文时，链接会回退到目标语言首页，而不是给你造一个看起来很合理、点进去却 404 的地址。

每种语言拥有独立的本地检索索引，英文结果不会混入中文搜索。HTML `lang`、书写方向、canonical、`hreflang` 和 Open Graph locale 都来自同一组翻译对象，避免“界面已经切成中文，SEO 还说自己是英文”的漂移。

![OINK 的中文全文检索](search.webp)


## 八、自产自用

做文档框架有个大忌：光顾着搭架子，结果却没有内容往里放。**能用上才是本事。**

所以，我很快把自己这一摊子网站全都统一到了 OINK 上：

- **pigsty.io / pigsty.cc** —— Pigsty 这个 PostgreSQL 发行版的英文站与中文站，也是目前最大的用例。

![采用 OINK 的 Pigsty 中文文档](pigsty.webp)

- **silo.pgsty.com** —— 刚刚发布的 Silo，也就是 MinIO 的社区分支。

![采用 OINK 的 Silo 项目站](silo.webp)

- **pig.pgsty.com** —— PostgreSQL 包管理器，用来安装扩展。

![采用 OINK 的 Pig 项目站](pig.webp)

- **sow.pgsty.com** —— APT / DNF 仓库管理器，正好和 Pig 凑成一对。

![采用 OINK 的 Sow 项目站](sow.webp)

- **exp.pgsty.com** —— 很早以前做的 PG Exporter，现在终于有了自己的网站。

![采用 OINK 的 PG Exporter 项目站](exporter.webp)

- **pgsty.com** —— GitHub 组织与公司官网主页。

![采用 OINK 的 PGSTY 官网](pgsty.webp)

- **oink.pgsty.com** —— OINK 自己的文档站，当然也使用自己的主题。

![OINK 项目站的功能介绍](oink-features.webp)

虽然 OINK 是为开源项目和工程文档设计的，但拿来做别的也没问题。我翻译的那几本书，现在也在陆续迁移到这个框架，大概有六七本。

![采用 OINK 的书籍站点](book-design.webp)

![采用 OINK 的数据系统书籍站点](book-data.webp)


## 九、三分钟开始使用

OINK 0.2.0 要求 Git、Go 和 Hugo Extended 0.160.1 或更高版本，当前项目站使用 Hugo Extended 0.164.0 验证。

在 Hugo 站点根目录初始化模块并固定版本：

```bash
hugo mod init github.com/example/product-docs
hugo mod get github.com/pgsty/oink@v0.2.0
```

在 `hugo.yaml` 中导入主题：

```yaml
module:
  imports:
    - path: github.com/pgsty/oink
```

然后启动预览：

```bash
hugo server
```

完整的双语站点结构、配置和部署方式，可以直接参考 [OINK 开始使用指南](https://oink.pgsty.com/zh/docs/tutorial/)。想先看效果，可以浏览 [OINK 项目站](https://oink.pgsty.com/zh/)；主题源码位于 [`pgsty/oink`](https://github.com/pgsty/oink)，完整项目站与测试则位于 [`pgsty/oink.pgsty.com`](https://github.com/pgsty/oink.pgsty.com)。

手上已经有 Docsy 站点的，可以直接走迁移路线——理论上，任何 Docsy 站点都可以换过来。上面有这么多样例站点，任选一个下载下来改一改，就可以开始使用。


## 十、OINK 适合谁，不适合谁？

**适合**：你维护的是开源项目、数据库、基础设施、内部平台，或者其他需要长期演进的工程产品；你需要多语言、离线交付、可审计依赖、丰富的技术内容和稳定的静态部署。

**不适合**：你要的是多人在线协作 CMS、用户登录后的动态内容、实时数据后台，或者一整套前端应用框架。OINK 是一款 Hugo 主题，不是 SaaS，不是应用服务器，也不打算把一个静态文档站伪装成万能平台。

我喜欢 Hugo，恰恰是因为它足够 **无聊**：一个二进制、一棵内容树、一条构建命令，以及一份可以扔到任何地方的静态产物。OINK 想做的，不是用一个复杂框架重新包装这份简单，而是把现代工程文档真正需要的能力，压回这条简单的路径里。

一套好的文档框架，不应该让作者意识到它每天都在工作。

它只应该让内容更容易写，让答案更容易被找到，让知识在几年之后仍然 **能构建、能阅读、能迁移**。

这就是 OINK。
