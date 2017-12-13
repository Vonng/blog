# 如何用Go执行ODPS SQL

想在集团内愉快地使用Go语言，一些基础设施的支持不能少。不过无论是HSF，Diamond，或者ODPS，都没有Go的SDK，路漫漫兮呀。

使用Shell命令直接调odpscmd的方式，任何语言都可以执行ODPS SQL，但这种方式实在是太土鳖了。毕竟ODPS本身也是通过HTTP API提供服务的，能不能直接解析这个协议，包装一个SDK呢？

好在ODPS有一个Python SDK，Python藏不住源码，通过研究pyodps的实现，就可以逆向出ODPS的协议来。这里功能不贪多，只要执行ODPS SQL就好。我写了一个简单的Wrapper，放在Gitlab和Github上。



## 1. Short Ver

### Install

```bash
 go get github.com/Vonng/goodps
```
[Github Repo](http://github.com/Vonng/goodps)

集团内部也有一个分支：

```bash
 go get gitlab.alibaba-inc.com/ruohang.frh/goodps
```

[Gitlab Repo](http://gitlab.alibaba-inc.com/ruohang.frh/goodps)

### Usage

```go
package main

import (
    "fmt"
	log "github.com/Sirupsen/logrus"
	. "github.com/Vonng/goodps"
)

func main() {
	log.SetLevel(log.InfoLevel)
	odps := NewODPS(
		"l****************l",
		"g***************************0",
		"c*******dev",
		"http://service-corp.odps.aliyun-inc.com/api",
	)

	// CREATE
	odps.ExecSQL("CREATE TABLE xixi(id string);")

	// INSERT
	odps.ExecSQL(`INSERT INTO xixi SELECT "haha";`)

	// DESC
	ins, _ := odps.ExecSQL("DESC xixi;")
	ins.FetchResult()
	fmt.Println(ins.Result.Raw)

	// SELECT
	ins2, _ := odps.ExecSQL("SELECT * FROM xixi LIMIT 20;")
	result, _ := ins2.FetchResult()
	records, _ := result.CsvReader().ReadAll()
	for _, r := range records {
		fmt.Println(r)
	}

	// DROP
	odps.ExecSQL("DROP TABLE xixi;")
}

```

在NewODPS中填入你自己的AccessKey和AccessSecret即可。
使用Go来实现这个有什么好处呢？最大的好处当然是无依赖！一个ODPS SQL的工作流，可以用Go编写命令，实现诸如一键上传，一键下载，一键启动指定工作流之类的效果。然后编译成二进制，分发出去执行。不需要安装什么Python啊，Java运行时啊，拿着二进制就可以跑。



## 2. 实现原理

实际上阿里云的一系列产品对外提供的都是HTTP API，使用HMAC认证。关键是解决两个问题，第一个是认证，第二个是协议。

### 2.1 API的认证

认证一直是API对接里比较蛋疼的事情，尤其是很多时候大家都爱造轮子，弄一些自己的认证协议。总体而言，阿里云的认证方式还是比较蛋疼的。通过解析Python中的认证逻辑，还原出了认证的具体算法，简单说包括以下几个Point：

* 使用复杂的方式构造一个待签名消息msg，使用AccessSecret对其签名，与AccessID一起按指定格式填入Authorization首部。
* 待签名消息包括：固定MagicString：`ODPS`，首部`Content-MD5`, `Content-Type`,`Date`，以`x-odps`开头的首部。以`x-odps`开头的参数，标准化的`resource`（就是url path后面去掉`/api`的部分）。
* 细节是魔鬼，show you the code:

```go
// Sign will add necessary operations to make request valid for odps server
func (client *Client) Sign(r *http.Request) {
	var canonPath, msg, auth bytes.Buffer
	var signKeyList []string = []string{"content-md5", "content-type", "date"}
	signParams := make(map[string]string, len(r.Header)+3)

	// fill date header in RFC1123
	if dateStr := r.Header.Get("Date"); dateStr == "" {
		gmtTime := time.Now().In(location).Format(time.RFC1123)
		r.Header.Set("Date", gmtTime)
	}

	// build canonical resource.
	canonPath.WriteString(r.URL.Path)
	if urlParams := r.URL.Query(); len(urlParams) > 0 {
		canonPath.WriteByte('?')
		var paramKeys []string
		for k, _ := range urlParams {
			paramKeys = append(paramKeys, k)
		}
		sort.Strings(paramKeys)
		for i, k := range paramKeys {
			if i > 0 {
				canonPath.WriteByte('&')
			}
			canonPath.WriteString(k)
			if v := urlParams.Get(k); v != "" {
				canonPath.WriteByte('=')
				canonPath.WriteString(v)
			}
		}
	}
	canonPathStr := strings.TrimPrefix(canonPath.String(), "/api")

	// add headers to signParamsMap
	for k, v := range r.Header {
		lk := strings.ToLower(k)
		switch {
		case lk == "content-md5":
			signParams["content-md5"] = v[0]
		case lk == "content-type":
			signParams["content-type"] = v[0]
		case lk == "date":
			signParams["date"] = v[0]
		case strings.HasPrefix(lk, "x-odps"):
			signKeyList = append(signKeyList, lk)
			signParams[lk] = v[0]
		}
	}

	// add url query params with prefix "x-odps-" to singParamsMap
	for k, v := range r.URL.Query() {
		lk := strings.ToLower(k)
		if strings.HasPrefix(lk, "x-odps-") {
			signKeyList = append(signKeyList, lk)
			signParams[lk] = v[0]
		}
	}

	// build signing message
	msg.WriteString(r.Method)
	sort.Strings(signKeyList)
	for _, k := range signKeyList {
		msg.WriteByte('\n')
		v := signParams[k]
		if strings.HasPrefix(k, "x-odps-") {
			msg.WriteString(k)
			msg.WriteByte(':')
		}
		msg.WriteString(v)
	}
	msg.WriteByte('\n')
	msg.WriteString(canonPathStr)

	// calculate hmac-sha1 of msg
	hasher := hmac.New(sha1.New, []byte(client.AccessKey))
	hasher.Write(msg.Bytes())

	// build authorization header: `ODPS <access_id>:<signature>`
	auth.WriteString("ODPS ")
	auth.WriteString(client.AccessID)
	auth.WriteByte(':')
	auth.WriteString(base64.StdEncoding.EncodeToString(hasher.Sum(nil)))

	log.Debugf("[Client.Sign] Authorization: %s", auth.String())
	r.Header.Set("Authorization", auth.String())
}
```

这是一个通用的认证方式，发往ODPS任何请求都需要这样签名。当我意识到这一点的时候突然想到OSS里说不定也是这样签名的……? 

### 2.2 协议

发往ODPS的请求都使用XML格式，`Instance`里面套着`Job`，`JOB`里面套着`Task`。大概长这样

```xml
<?xml version="1.0" ?>
<Instance>
    <Job>
        <Priority>1</Priority>
        <Tasks><SQL>
                <Name>AnonymousSQLTask</Name>
                <Query><![CDATA[SELECT 1;]]></Query>
                <Config>
                    <Property>
                        <Name>settings</Name>
                        <Value>{"odps.sql.udf.strict.mode": "true"}</Value>
                    </Property>
                </Config>
            </SQL></Tasks>
        <DAG><RunMode>Sequence</RunMode></DAG>
    </Job>
</Instance>
```

其中`//Instance/Job/Tasks/SQL/Query/text()`里面填的是要执行的SQL。就是这么简单……。



而ODPS的响应也是一个XML。比较恍惚的是执行SELECT查询出来的结果竟然是放在XML里面的CSV。而且没有双引号扩起转义，这实在是让人无比头大……



### 3. 后续

这是一个半成品啊半成品。执行SQL是够用了。

不过还没有很好的处理CSV返回结果的问题，对于上传和下载我觉得也很有必要弄一弄，其他要做的事包括

* 设计一种与`database/sql`兼容的ODPS SQL接口
* 实现Instance的其他相关功能: List, Get Kill
* 尝试实现与`go-pg`类似的表结构定义功能。
* `CSV Parser`
* 一种利用ODPS Endpoint一万条一万条下数据，而不是用Tunnel来下载数据的方法。

有时间继续搞一下吧。