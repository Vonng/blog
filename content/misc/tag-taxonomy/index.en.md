---
title: "Tag Classification Theory"
date: 2016-11-03
author: vonng
summary: |
  Recently, I needed to design a tag management system for a business. During the process of organizing existing tags, I developed this theoretical framework.
---


Recently, I needed to design a tag management system for a business. During the process of organizing existing tags, I developed this theoretical framework.


## 0. Tag Definition: Tag Taxonomy

For **tags**, it's difficult to provide a universally accepted definition that specifies the difference and genus of this concept.
So to grasp this concept, we need to adopt another approach: **classification** and **enumeration**.

The first question to solve is: what types of tags exist? How do we classify tags?
First, let's classify "how to classify" itself: examining tag classification from both "form" and "content" perspectives.


## 1. Formal Classification of Tags

Tag form is the primary basis for tag classification.
We can list some common or uncommon "tag" examples:

```
Gender tag: Female
Age tag: 23
Weight tag: 90.6
Idol tag: Asimov

Recent cities visited tag: ['Beijing','Qingdao','Chengdu']
Interest tag: ['skiing','travel','eating']
Measurements tag: [100,100,100]
Last year's consumption tag: [5250.12,6873.23,1232.12,3231.23,...,2321.24]

Website browsing preference tag: {"Q&A":0.55, "Social":0.75, "Travel":0.82, "Group buying":0.32,"E-commerce":0.78,...}
Phone brand preference tag: {"iphone7":0.99, "iphone5":0.35, "Xiaomi3":0.12,...}
Predicted game score tag: {0 : 0.2, ..., 100 : 0.003, ..., 198 : 0.01, 199 : 0.01, 2100 : 0.005,...}

Predicted age tag: 30 : <confidence 0.72>
```


Through observation, we can discover some patterns:

### 1.1 From Tag Organization Structure

* Common tags are **single-value tags**, also called **atomic tags**. Their values are independent values like `Female`, `23`, `90.6`.
* Some tags are **multi-value tags**, where **multiple atomic tags** form a unit as one tag. For example, keywords people use to describe themselves on Weibo: `['90s','Virgo','cutie']`.
* Adding **associated weights** to each **atomic tag** in **multi-value tags** creates **weighted tags**. For example, preference levels for different phone brands: `{"iphone7":0.99, "iphone5":0.35, "Xiaomi3":0.12,...}`
* Single atomic tags with weights are also common, like providing a predicted age with confidence. Using weighted tag structure for this single kv structure would seem strange and cumbersome. Therefore, this should be a separate category called **single-weight tags**. For example: `[30, 0.72]` can represent predicted age of 30 with confidence 0.72.

#### Conclusion:

From tag organization structure, tags can be classified into four types: **single-value tags**, **single-weight tags**, **multi-value tags**, **multi-weight tags**.
This gives us two basically orthogonal dimensions: **whether multi-value tag**, **whether with weights**.
These four tag structure types, **single-value tags**, **multi-value tags**, **multi-weight tags**, correspond exactly to JSON's three Primitive Types: `atomic`, `array`, `object`. The special **single-weight tags** can be mapped to length-2 `array`.



### 1.2 From Tag Atomic Types

We know that computer (x86, general-purpose computer) implementations essentially only provide two atomic data types: **integer** and **floating-point**. Pointers, single characters, booleans, floating-point numbers all belong to **numeric types**, and the extremely common **character arrays** can be seen as **string types**, so logically we actually only have two atomic data types: `Numeric` and `String`.

The idea that all atomic tags only have two simple classifications of `numeric` and `string` is certainly appealing. But considering realistic demand constraints (like the distinction between discrete tags and continuous value tags, ODPS distinguishing BIGINT and DOUBLE), we still subdivide **numeric** into **integer** and **floating-point**, so atomic tag types become three: `integer`, `floating-point`, `string`.

On the other hand, for **weighted tags** (single-weight or multi-weight), besides the atomic tag **value** having a type, its **weight** should also have an appropriate type. Forcing its type to be **numeric** is a reasonable and appropriate constraint. More specifically, implementing **weights** as `Double` is quite reasonable.

Tag **atomic types** and **structure types** are not completely orthogonal due to some technical constraints. Many languages' associative arrays (Map) can use various types as keys (`int`, `string`, `double`). However, in JSON specification, only `string` can be object keys. This isn't an irreconcilable problem: integers can safely be serialized as `string` keys. But `floating-point` imprecision during serialization causes many unexpected troubles, so **multi-value tags** cannot have floating-point atomic types.

#### Conclusion:

From atomic type classification: tags can be classified as `integer`, `floating-point`, `string`.



### 1.3 From Integer Atomic Type Interpretation Methods

In section 2.1.2, we classified tag atomic types. But we must consider another most common tag classification in production practice: **enumeration tags**. Enumeration tags are usually represented by an integer in form, while providing an **enumeration dictionary** mapping integer values to strings for interpretation.

For example:

```
# Gender tag dictionary
gender_dict = {0:'Male', 1:'Female', 2: 'Other'....}
# Gender tag value
0                        # Single-value enumeration tag representing male
[0, 0, 1, 0]             # Multi-value enumeration tag representing family gender composition
{0 : 0.1, 1: 0.4}        # Multi-value enumeration tag representing predicted gender+confidence or sexual orientation+tendency
```

Another example:

```
# Province mapping dictionary
province_dict = {11:'Beijing',12:'Tianjin',13:'Hebei',......}
# Province value tag
13                             # Single-value enumeration tag, I came to Hebei Province!
{'11': 0.76, '13':0.1}         # Multi-value enumeration tag, e.g., user's predicted next crime location probability+feasibility
```

Additionally, in some sense, boolean tags are special enumeration tags with enumeration dictionary: `{0:False, 1:True}`, which can naturally fit into the enumeration tag system. Through enumeration tags, we can even implement so-called `Nullable boolean`, adding more semantics to boolean tags.

So, the interpretation method for integer atomic types can also be a tag classification dimension: `whether enumeration tag`. But this dimension is highly related to the atomic tag type dimension in section 2.1.3 (because this dimension is only valid when atomic type is integer). So these two dimensions should be combined.

#### FAQ:

*   What's the difference between enumeration and integer, i.e., when to use integer vs enumeration?
    Simple: use enumeration when values **can be exhausted, reasonable in number, infrequent changes**. For example, city codes are suitable enumeration tags: exhaustible, acceptable scale, though may change, probability and correction cost are acceptable. On the other hand, **a person's hair count** can certainly be represented by an integer, but it's neither exhaustible nor reasonable in number, clearly unsuitable as enumeration tags.

*   Difference between enumeration and string?
      For example, user's phone brand seems representable by single-value string tag or enumeration. But it's more suitable as `string` rather than `enumeration`. Because phone brands aren't fixed in number, brands constantly emerge and disappear. In this situation, frequent enumeration dictionary changes would bring many inconveniences to tag usage.

*   What's special about enumeration tags?
      Enumeration tags need maintaining a tag dictionary table for **enumeration item ID** to **enumeration item name** mappings. Multiple enumeration tags' dictionaries can be maintained in the same table. Also, enumeration tags can have hierarchical relationships. For example, "city enumeration tags" can have upper-level tags: "province enumeration tags". Enumeration tags with hierarchical relationships can easily implement roll-up and drill-down through **enumeration item mapping**.

*   Why not use strings as **enumeration item IDs**?
      Enumerations in most languages default to integer implementation. Integer IDs have huge performance advantages and simplicity over string IDs.

#### Conclusion:

Classifying by **atomic tag value type and interpretation method**, we get one dimension: `tag atomic type`.
This dimension has 4 values: `enumeration`, `integer`, `floating-point`, `string`


###  1.4 Formal Classification Summary

From above, we get two main, basically orthogonal classification dimensions from tag form:
* Organization structure: { `single-value tag`, `single-weight tag`, `multi-value tag`, `multi-weight tag` }
* Atomic type: { `enumeration tag`, `integer tag`, `text tag`, `floating-point tag` }

Excluding `floating-point multi-weight tags` as unreasonable combinations, we have `4 x 4 -1 = 15` combinations.
So tags can be formally classified into 15 types, fitting exactly within 4-bit representation.

According to tag atomic type frequency, we can assign earlier encodings to most common tag types.
Since most common tags are single-value tags, placing tag structure type bit field before tag atomic type bit field is reasonable design.
Enumeration tags are most numerous, integer second, some string tags, floating-point tags relatively rare.
So, we can assign encodings for tag formal types as follows:


#### 1.4.1 Tag Structure Type Field

| Structure | Code | Description |
|------|------|---------------------------------------------|
| Single-value tag | 0x00 | Value is single atomic type corresponding value |
| Single-weight tag | 0x01 | Value is single atomic type with weight, represented as length-2 array |
| Multi-value tag | 0x10 | Value is list of same atomic type |
| Weight tag | 0x11 | Value is dictionary of same atomic type, key can only be string or string(bigint) |

#### 1.4.2 Tag Atomic Type Field

| Structure | Code | Description |
|------|------|------------------------------|
| Enumeration tag | 0x00 | Actually Bigint type, default type, needs type dictionary for interpretation |
| Integer tag | 0x01 | Integer numeric atomic tag |
| Text tag | 0x10 | String atomic tag |
| Floating-point tag | 0x11 | Floating-point numeric atomic tag |

#### 1.4.3 Tag Formal Classification Overview

| Type ID | English Code | Name | Structure ID | Structure Name | Atomic ID | Atomic Name | Storage |
|------|------------|------|------|-----|------|------|-------|
| 0 | atom-enum | Single-value enumeration | 0 | Single-value | 0 | Enumeration | int |
| 1 | atom-int | Single-value integer | 0 | Single-value | 1 | Integer | int |
| 2 | atom-text | Single-value text | 0 | Single-value | 2 | Text | text |
| 3 | atom-float | Single-value floating-point | 0 | Single-value | 3 | Floating-point | float |
| 4 | pair-enum | Single-weight enumeration | 1 | Single-weight | 0 | Enumeration | json |
| 5 | pair-int | Single-weight integer | 1 | Single-weight | 1 | Integer | json |
| 6 | pair-text | Single-weight text | 1 | Single-weight | 2 | Text | json |
| 7 | pair-float | Single-weight floating-point | 1 | Single-weight | 3 | Floating-point | json |
| 8 | list-enum | Multi-value enumeration | 2 | Multi-value | 0 | Enumeration | json |
| 9 | list-int | Multi-value integer | 2 | Multi-value | 1 | Integer | json |
| 10 | list-text | Multi-value text | 2 | Multi-value | 2 | Text | json |
| 11 | list-float | Multi-value floating-point | 2 | Multi-value | 3 | Floating-point | json |
| 12 | dict-enum | Multi-weight enumeration | 3 | Multi-weight | 0 | Enumeration | json |
| 13 | dict-int | Multi-weight integer | 3 | Multi-weight | 1 | Integer | json |
| 14 | dict-text | Multi-weight text | 3 | Multi-weight | 2 | Text | json |

Note the relationship between tag formal classification and storage types:

For storage, single-value tags use `Bigint`, `Double`, `String` storage. Single-weight tags use fixed-length-2 arrays `[value,weight]`, multi-value tags use arrays `[value1,value2,...]`, multi-weight tags use objects `{value1: weight1,...}`, and when atomic type is integer or enumeration, `value` should store its string serialized form to comply with JSON key type requirements.

Resultingly, all single-value tags store directly in their corresponding types. All other tags use JSON serialization storage.

Here are examples for each tag type:

#### 1.4.4 Tag Formal Classification Examples

| id | title | storage | sample |
|----|-------|---------|--------|
| 0 | Single-value enumeration | int | Gender tag: 1 {"0":"Male", "1":"Female"} |
| 1 | Single-value integer | int | Age: 23 |
| 2 | Single-value text | text | Favorite novel: "One Hundred Years of Solitude" |
| 3 | Single-value floating-point | float | Weight: 60.13 |
| 4 | Single-weight enumeration | json | Predicted gender: [1, 0.99] |
| 5 | Single-weight integer | json | Predicted age: [23, 0.99] |
| 6 | Single-weight text | json | TV show preference: ["Star Trek", 9.8] |
| 7 | Single-weight floating-point | json | Predicted weight: [60.13, 0.78] |
| 8 | Multi-value enumeration | json | Alarm settings: [1, 2, 3, 4, 5] |
| 9 | Multi-value integer | json | Measurements: [100, 100, 100] |
| 10 | Multi-value text | json | Favorite TV shows: ["Star Trek", "Breaking Bad", "Yes, Minister!"] |
| 11 | Multi-value floating-point | json | Monthly consumption records: [6379.13, 6378.24, 6356.12] |
| 12 | Multi-weight enumeration | json | Alarm settings probability distribution: {"1":0.98, "2":0.75, "3":0.75, "4":0.5, "5":0.3} |
| 13 | Multi-weight integer | json | Lucky numbers preference: {"7":0.32, "5":0.63} |
| 14 | Multi-weight text | json | Website browsing preference tags: {"Q&A":0.55, "Social":0.75} |




## 2. Content Classification of Tags

Tag classification by **content nature**, compared to **formal classification**, appears much more diverse. Can classify purely by tag value characteristics (Nullable, whether weights normalized, etc...), or by tag source scenarios (mobile, PC), tag ownership (private, internal, group, company), tag scale, tag dependencies, tag ID types, or frontend display hierarchical categories, etc. many dimensions.

Formal classification determines tag presentation, but content classification doesn't have this effect. So **content classification results are more suitable as descriptive fields rather than type fields.** In other words, rather than calling content classification **classification**, it's better called **dynamically addable enumeration attributes**.

But for content classification, we still need further examination. Tag content classification can be further subdivided into: classification by **tag inherent attributes** and by **artificial usage**. Those belonging to tag inherent attributes are suitable for tag metadata tables as fields. Those belonging to artificial usage division may frequently change requirements. So we need a mechanism supporting dynamic classification system addition without changing database schema. This article suggests using WordPress-like Taxonomy concepts to implement such dynamic classification systems.


### 2.2 Tag Dynamic Classification System Design

To provide flexibility adapting to changing requirements, consider building a **classification system table (tag_taxonomy)**, a **classification item table (tag_term)**, and a **classification table (tag_classification)**. Dynamically implement classification system addition. If implementing hierarchical classification systems, just maintain **parent entry** fields for each **classification item** in the **classification item table**.

For example, if we need to dynamically add a "public/private" classification. First register this classification system in the **classification system table**: "Tag Public/Private Classification System". Then add "Public", "Private" two **classification items** in the **classification item table**, referencing the **Tag Public/Private Classification System** in the **classification system table** through foreign keys. Finally in the **tag classification table**, associate specific tags with **classification items** through foreign keys.


### 2.3 Content Summary

For tag content classification:
* Tag **inherent properties** are suitable as **tag table** fields
* Tag **artificial classification** suits using dynamic classification systems through foreign key introduction.

A feasible dynamic classification implementation schema: [WordPress Database Description](https://codex.wordpress.org/Database_Description)
