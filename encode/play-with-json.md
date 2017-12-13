# 玩弄JSON

JSON(JavaScript Object Notation)[RFC 4627](http://www.ietf.org/rfc/rfc4627.txt)是目前Web数据交换的事实标准。本文记叙JSON的格式，Javascript与Python的JSON库使用实践，以及直接在数据库(PostgreSQL)中玩弄JSON的方式。



## 1. JSON标准

### 1.1 JSON的语法

JSON语法可以表述以下三种类型的值：

* ** 简单值**  使用JavaScript相同的语法，可以表示字符串、数值、布尔值、null、（没有undefined）。例如`5`,`"Hello World"`,`null`，都属于简单值。
* **对象** 复杂数据类型，一组无序的键值对，每个键值对的键必须是双引号括起的字符串，值可以是简单值也可以是复杂数据类型。例如
```JSON
{
	"name": "haha"
	"age": 74
}
```
* **数组** 复杂数据类型，表示有序的值的列表，可通过数值索引访问，数组的值可以是简单值也可以是复杂数据类型，且同一数组内可以同时出现任意类型的值。例如
```JSON
["a", 2, {"b":3},[4, 5, 6] ]
```

JSON对象中的键应当是独一无二的，但在JSON表示中没有强制这一点，通常的做法都是取最后一次出现的value作为重复key的值。

### 1.2 JSON的编码

RFC规定了JSON**必须**使用UTF-8,UTF-16,UTF-32中的编码来表示。一般使用UTF-8编码。在JSON的字符串中最好不要使用unicode字面值，使用\uxxxx的形式表示能有效降低乱码的可能性。

RFC**禁止**JSON的字符表示前出现BOM标记。

RFC**没有明确禁止**JSON的string中出现非法Unicode字节序列，比如“unpaired UTF-16 surrogates”。



## 2. 玩弄JSON (PostgreSQL)

在PostgreSQL中玩弄JSON有个大好处：可以直接在数据库中编写业务逻辑，从原始数据表中生成所需的JSON。

（后端会不会失业啊好怕怕~）





## 3. 玩弄JSON(Javascript)

早期的JSON解析器基本上就是使用`eval()`函数进行的。
但这样做存在安全隐患，所以在浏览器或者Node中定义有全局模块`JSON`。

#### 序列化： `JSON.stringify`
`JSON.stringify(value[, replacer[, space]])`

`JSON.stringify`方法会忽略所有原型成员，以及所有值为`undefined`的属性。
该方法可以指定两个可选参数：过滤器函数与缩进字符。

##### 过滤器函数
* If you return a `Number`, the string corresponding to that number is used as the value for the property when added to the JSON string.
* If you return a `String`, that string is used as the property's value when adding it to the JSON string.
* If you return a `Boolean`, "true" or "false" is used as the property's value, as appropriate, when adding it to the JSON string.
* If you return `any other object`, the object is recursively stringified into the JSON string, calling the replacer function on each property, unless the object is a function, in which case nothing is added to the JSON string.
* If you return `undefined`, the property is not included in the output JSON string.

```javascript
function replacer(key, value) {
  if (typeof value === "string") {
    return undefined;
  }
  return value;
}

var foo = {foundation: "Mozilla", model: "box", week: 45, transport: "car", month: 7};
var jsonString = JSON.stringify(foo, replacer);
```
可以在过滤器函数中滤除不必要的属性

##### space参数
如果指定为数字，使用空格作为indent，最大为10.
也可以指定为其他字符。
```js
JSON.stringify({ uno: 1, dos: 2 }, null, '\t');
// returns the string:
// '{
//     "uno": 1,
//     "dos": 2
// }'
```

#### `toJSON`
`JSON.stringify`的解析顺序如下
* 如果存在`toJSON`方法且能通过该方法取得有效值，调用该方法，否则返回对象本身。
* 如果提供第二个参数：函数过滤器，使用它，传入第一步的返回值。
* 对第二步返回的每个值进行相应的序列化。
* 执行格式化。

```js
var obj = {
  foo: 'foo',
  toJSON: function() {
    return 'bar';
  }
};
JSON.stringify(obj);        // '"bar"'
JSON.stringify({ x: obj }); // '{"x":"bar"}'
```

#### 解析`JSON.parse()`
`JSON.parse(text[, reviver])`
从字符串中解析JSON，可以选定一个reviver函数作为Hooki。

```js
JSON.parse('{}');              // {}
JSON.parse('true');            // true
JSON.parse('"foo"');           // "foo"
JSON.parse('[1, 5, "false"]'); // [1, 5, "false"]
JSON.parse('null');            // null
```
##### Reviver函数
```js
JSON.parse('{"p": 5}', function(k, v) {
  if (typeof v === 'number') {
    return v * 2;  // return v * 2 for numbers
  }
  return v;        // return everything else unchanged
});
```



## 4. 玩弄JSON(Python)

python的JSON模块基本与Js类似。

### 类型映射

| JSON   | PYTHON          |
| ------ | --------------- |
| JSON   | Python          |
| object | dict            |
| array  | list            |
| string | unicode         |
| number | (int)	int, long |
| numbe  | (real)	float    |
| true   | True            |
| false  | False           |
| null   | None            |

### JSON序列化
```python
>>> import json
>>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]'
>>> print json.dumps("\"foo\bar")
"\"foo\bar"
>>> print json.dumps(u'\u1234')
"\u1234"
>>> print json.dumps('\\')
"\\"
>>> print json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
{"a": 0, "b": 0, "c": 0}
>>> print json.dumps(None)'
null
```
其格式可以通过indent参数控制。
```
>>> import json
>>> json.dumps([1,2,3,{'4': 5, '6': 7}], separators=(',',':'))
'[1,2,3,{"4":5,"6":7}]'

>>> import json
>>> print json.dumps({'4': 5, '6': 7}, sort_keys=True,
...                  indent=4, separators=(',', ': '))
{
    "4": 5,
    "6": 7
}
```
### JSON解析
```python
>>> import json
>>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
[u'foo', {u'bar': [u'baz', None, 1.0, 2]}]
>>> json.loads('"\\"foo\\bar"')
u'"foo\x08ar'
```

### JSON格式化工具 （Shell）
```sh
$ echo '{"json":"obj"}' | python -mjson.tool
{
    "json": "obj"
}
```