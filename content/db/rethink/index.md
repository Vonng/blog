---
title: 正本清源：技术反思录
date: 2023-05-29
hero: /hero/rethink.jpg
author: |
  [冯若航](https://vonng.com)（[@Vonng](https://vonng.com/en/)） | [微信公众号](https://mp.weixin.qq.com/s/Q0OtrpEhF24XN7gwMjbSRA)
summary: >
  降本增效的主旋律触发了所有技术的价值重估，当然也包括 —— 数据库。本系列将评述 DB领域 热点技术，并对其在当下的利弊权衡发出灵魂拷问。 
tags: [数据库]
---

最近在技术圈有一些热议的话题，[云数据库是不是智商税？](/zh/blog/cloud/rds/)？[公有云是不是杀猪盘](/zh/blog/cloud/ebs/)？[分布式数据库是不是伪需求](/zh/blog/db/distributive-bullshit/)？[微服务是不是蠢主意](/zh/blog/db/microservice-bad-idea/)？[你还需要运维和DBA吗](https://mp.weixin.qq.com/s/Gk9bG_EOIv0IAkim41XRHg)？[中台是不是一场彻头彻尾的自欺欺人](https://mp.weixin.qq.com/s/VgTU7NcOwmrX-nbrBBeH_w)？在Twitter与HackerNews上也有大量关于这类话题的讨论与争辩。

在这些议题的背后的脉络是大环境的改变：**降本增效压倒其他一切，成为绝对的主旋律**。开发者体验，架构可演化性，研发效率这些属性依然重要，但在 **ROI** 面前都要让路 —— **社会思潮与根本价值观的变化会触发所有技术的重新估值。**

有人说，互联网公司砍掉一半人依然可以正常运作，只不过老板不知道是哪一半。现在收购推特的马斯克刷新了这个记录：截止到2023年5月份，推特已经从8000人一路裁员 **90%** 到现在的不足千人，而依然不影响其平稳运行。**这个结果彻底撕下大公司病冗员问题的遮羞布，其余互联网大厂早晚会跟进，掀起新一轮大规模裁员的血雨腥风**。

在经济繁荣期，大家可以有余闲冗员去自由探索，也可以使劲儿吹牛造害铺张浪费炒作。但在经济萧条下行阶段，所有务实的企业与组织都会开始重新审视过往的利弊权衡。同样的事情不仅会发生在人上，也会发生在技术上，这是实体世界的危机传导到技术界的表现：**泡沫总会在某个时刻需要出清，而这件事已正在发生中。**

公有云，Kubernetes，微服务，云数据库，分布式数据库，大数据全家桶，Serverless，HTAP，Microservice，等等等等，所有这些技术与理念都将面临拷问：**有些事不上秤没有四两，上了秤一千斤也打不住**。这个过程必然伴随着怀疑、痛苦，伤害与毁灭，但也孕育着希望，喜悦，发展与新生。花里胡哨华而不实的东西会消失在历史长河里，大浪淘沙能存留下来的才是真正的好技术。

在这场技术界的惊涛骇浪中，需要有人透过现象看本质，脚踏实地的把各项技术的好与坏，适用场景与利弊权衡讲清楚。而我本人愿意作为一个亲历者，见证者，评叙者，参与者躬身入局，加入其中。这里拟定了一个议题列表集，名为《**正本清源：技术反思录**》，将依次撰文讨论评论业界关心的热点与技术：

- [国产数据库是大炼钢铁吗？](https://mp.weixin.qq.com/s/aLXC7f2iYUfATNWsnyotkA)
- [中国对PostgreSQL的贡献约等于零吗？](https://mp.weixin.qq.com/s/79_PnX-a5iSfDMgz_VUx5A)
- [MySQL的正确性为何如此拉垮？](https://mp.weixin.qq.com/s/gQZ3Q5JKV8gaBNhc1puPcA)
- [没错，数据库确实应该放入 K8s 里！](https://mp.weixin.qq.com/s/rpyNczx0AD_iseMMLioVjw)（转载SealOS）
- [数据库应该放入K8S里吗？](https://mp.weixin.qq.com/s/4a8Qy4O80xqsnytC4l9lRg)
- [把数据库放入Docker是一个好主意吗？](https://mp.weixin.qq.com/s/kFftay1IokBDqyMuArqOpg)
- [向量数据库凉了吗？](https://mp.weixin.qq.com/s/0eBZ4zyX6XjBQO0GqlANnw)
- [阿里云的羊毛抓紧薅，五千的云服务器三百拿](https://mp.weixin.qq.com/s/Nh28VahZkQMdR8fDoi0_rQ)
- [数据库真被卡脖子了吗？](https://mp.weixin.qq.com/s/vh1JE_BdaLetWtt5vvPDDw)
- [EL系操作系统发行版哪家强？](https://mp.weixin.qq.com/s/xHG8OURTYlmnQTorFkzioA)
- [基础软件到底需要什么样的自主可控？](https://mp.weixin.qq.com/s/hWbcc9cMM9qTjPJ0m6G0Kg)
- [如何看待 MySQL vs PGSQL 直播闹剧](https://mp.weixin.qq.com/s/tRNedHlXmp7YfCqd21e5PA)
- [驳《MySQL：这个星球最成功的数据库》](https://mp.weixin.qq.com/s/7UvQulQGt9SIhUQasxuEZw)
- [向量是新的JSON](https://mp.weixin.qq.com/s/BJkbtwl_SPx99GBOzPsJiA) 【译评】
- [【译】微服务是不是个蠢主意？](https://mp.weixin.qq.com/s/mEmz8pviahEAWy1-SA8vcg)
- [分布式数据库是伪需求吗？](https://mp.weixin.qq.com/s/-eaCoZR9Z5srQ-1YZm1QJA)
- [数据库需求层次金字塔](https://mp.weixin.qq.com/s/1xR92Z67kvvj2_NpUMie1Q)
- [StackOverflow 2022数据库年度调查](https://mp.weixin.qq.com/s/xcORYy2suzOw50SOaOCodw)
- [DBA还是一份好工作吗？](https://mp.weixin.qq.com/s/Py3o31w3db5E9FsviAZeCA)
- [PostgreSQL会修改开源许可证吗？](https://mp.weixin.qq.com/s/qNcqGHL-wVTSB7Kxko2eNw)
- [Redis不开源是“开源”之耻，更是公有云之耻](https://mp.weixin.qq.com/s/W5kOLxeJCIHjnWbIHc1Pzw)
- [PostgreSQL正在吞噬数据库世界](https://mp.weixin.qq.com/s/8_uhRH93oAoHZqoC90DA6g)
- [RDS阉掉了PostgreSQL的灵魂](https://mp.weixin.qq.com/s/EH7RPB6ImfMHXhOMU7P5Qg)
- [技术极简主义：一切皆用Postgres](https://mp.weixin.qq.com/s/yI06zdqnW5uWnqvKmgM-9g)


[![](rethink.jpg)](https://mp.weixin.qq.com/s/Q0OtrpEhF24XN7gwMjbSRA)

----------------

## 写作计划

《[云数据库是不是智商税](https://mp.weixin.qq.com/s/LefEAXTcBH-KBJNhXNoc7A)》

《[云盘是不是杀猪盘？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485391&idx=1&sn=4cec9af2b58160eb345a6b12411f0b68&chksm=fe4b3214c93cbb023c13a89133c75bf1e88e1543de9359df7447498e4a9d5ec555313a954566&scene=21#wechat_redirect)》

《[分布式数据库是不是伪需求](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485549&idx=1&sn=7c34439d82431129c57aba211202b5ca&chksm=fe4b3db6c93cb4a0423daf3a226e04867821e34ba3c6b5a8145bd5319c728fb08d63b2544a43&scene=21#wechat_redirect)？》

《国产数据库是不是大跃进？》

《TPC-C打榜是不是放卫星？》

《信创数据库是不是恰烂钱？》

《谁卡住了中国数据库的脖子？》

《[微服务是不是蠢主意](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485566&idx=1&sn=640f4441fddbfe889d98d715af0a1cad&chksm=fe4b3da5c93cb4b30839bc2e65f40983c7e881768c908a4a38ffe3565543b56090244d38f63e&scene=21#wechat_redirect)？》

《Serverless是不是榨钱术？》

《RCU/WCU计费是不是阳谋杀猪？》

《数据库到底要不要放入K8S?》

《HTAP是不是纸上谈兵？》

《单机分布式一体化是不是脱裤放屁？》

《你真的需要专用向量数据库吗？》

《你真的需要专用时序数据库吗？》

《你真的需要专用地理数据库吗？》

《APM时序数据库选型姿势指北》

《202x数据库选型指南白皮书》

《开源崛起：商业数据库还能走多远？》

《[范式转移：云原生能否干翻公有云？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485301&idx=1&sn=2fb038f8b9f26c095d97eb0d87e8b262&chksm=fe4b32aec93cbbb81fbb1d7dfadba404ff7015d2b83f590bbe46a7372b55ac0aac076a71a76b&scene=21#wechat_redirect)》

《[本地优先：你是否真的需要 XaaS？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247484735&idx=1&sn=4bd01a8268411de05fdea1d68c429f43&chksm=fe4b30e4c93cb9f27fe36ce24040df71bbe0f1035c4a1db6676cae6e10274c7daf4cdc899072&scene=21#wechat_redirect)》

《云厂商的 SLA 到底靠不靠得住？》

《大厂技术管理思想真的先进吗？》

《卷数据库内核还有没有出路？》

《用户到底需要什么样的数据库？》

《再搞 MySQL 还有没有前途？》

《 [炮打 RDS —— 我的一张大字报](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485349&idx=1&sn=96fde26dd9efd399ef7ae11e52e05843&chksm=fe4b327ec93cbb688e2708ff4e709a7ba32eee2be9d8637e9b941f47e6600dc7fcd2710a42c4&scene=21#wechat_redirect) 》

《[为什么 PostgreSQL 是最成功的数据库？](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247485216&idx=1&sn=1b59c7dda5f347145c2f39d2679a274d&chksm=fe4b32fbc93cbbed574358a3bcf127dd2e4f458638b46efaee1a885a5702a66a5d9ca18e3f90&scene=21#wechat_redirect)》



如果您有任何认为值得讨论的话题，也欢迎在评论区中留言提出，我将视情况加入列表中。