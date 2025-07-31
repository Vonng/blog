---
title: "排序算法通览"
date: 2016-09-23
hero: /hero/sort.jpg
summary: |
  排序算法是最基础、应用最广泛、也是面试最常考的算法。这里总结了经典的排序算法：选择排序，插入排序，冒泡排序，希尔排序，计数排序，快速排序，归并排序，堆排序的原理与实现。
menu:
  sidebar:
    parent: note
---


> 排序算法是最基础、应用最广泛、也是面试最常考的算法。

一个**排序算法**（Sorting algorithm）是一种能将一串数据依照特定排序方式进行排列的一种算法。其中：

* 输出结果为递增序列
* 输出结果是原输入的一种排列或重组

可排序对象所需的两个基本操作为：比较（Compare）与交换（Swap）


## 排序算法分类

| 大类   | 细分                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 交换排序 | [冒泡排序](https://zh.wikipedia.org/wiki/%E5%86%92%E6%B3%A1%E6%8E%92%E5%BA%8F) [鸡尾酒排序](https://zh.wikipedia.org/wiki/%E9%B8%A1%E5%B0%BE%E9%85%92%E6%8E%92%E5%BA%8F) [奇偶排序](https://zh.wikipedia.org/wiki/%E5%A5%87%E5%81%B6%E6%8E%92%E5%BA%8F) [梳排序](https://zh.wikipedia.org/wiki/%E6%A2%B3%E6%8E%92%E5%BA%8F) [侏儒排序](https://zh.wikipedia.org/w/index.php?title=%E4%BE%8F%E5%84%92%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [快速排序](https://zh.wikipedia.org/wiki/%E5%BF%AB%E9%80%9F%E6%8E%92%E5%BA%8F) [臭皮匠排序](https://zh.wikipedia.org/wiki/%E8%87%AD%E7%9A%AE%E5%8C%A0%E6%8E%92%E5%BA%8F) [Bogo排序](https://zh.wikipedia.org/wiki/Bogo%E6%8E%92%E5%BA%8F) |
| 选择排序 | [选择排序](https://zh.wikipedia.org/wiki/%E9%80%89%E6%8B%A9%E6%8E%92%E5%BA%8F) [堆排序](https://zh.wikipedia.org/wiki/%E5%A0%86%E6%8E%92%E5%BA%8F) [平滑排序](https://zh.wikipedia.org/w/index.php?title=%E5%B9%B3%E6%BB%91%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [笛卡尔树排序](https://zh.wikipedia.org/w/index.php?title=%E7%AC%9B%E5%8D%A1%E5%B0%94%E6%A0%91%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [锦标赛排序](https://zh.wikipedia.org/w/index.php?title=%E9%94%A6%E6%A0%87%E8%B5%9B%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [圈排序](https://zh.wikipedia.org/w/index.php?title=%E5%9C%88%E6%8E%92%E5%BA%8F&action=edit&redlink=1)                                  |
| 插入排序 | [插入排序](https://zh.wikipedia.org/wiki/%E6%8F%92%E5%85%A5%E6%8E%92%E5%BA%8F) [希尔排序](https://zh.wikipedia.org/wiki/%E5%B8%8C%E5%B0%94%E6%8E%92%E5%BA%8F) [伸展排序](https://zh.wikipedia.org/wiki/%E4%BC%B8%E5%B1%95%E6%A8%B9) [二叉查找树排序](https://zh.wikipedia.org/wiki/%E4%BA%8C%E5%85%83%E6%90%9C%E5%B0%8B%E6%A8%B9) [图书馆排序](https://zh.wikipedia.org/wiki/%E5%9B%BE%E4%B9%A6%E9%A6%86%E6%8E%92%E5%BA%8F) [耐心排序](https://zh.wikipedia.org/wiki/%E8%80%90%E5%BF%83%E6%8E%92%E5%BA%8F)                                                                                                                                                                           |
| 归并排序 | [归并排序](https://zh.wikipedia.org/wiki/%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F) [梯级归并排序](https://zh.wikipedia.org/w/index.php?title=%E6%A2%AF%E7%BA%A7%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [振荡归并排序](https://zh.wikipedia.org/w/index.php?title=%E6%8C%AF%E8%8D%A1%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [多相归并排序](https://zh.wikipedia.org/w/index.php?title=%E5%A4%9A%E7%9B%B8%E5%BD%92%E5%B9%B6%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [列表排序](https://zh.wikipedia.org/w/index.php?title=%E4%B8%B2%E5%88%97%E6%8E%92%E5%BA%8F&action=edit&redlink=1)                                                           |
| 并发排序 | [双调排序器](https://zh.wikipedia.org/w/index.php?title=%E5%8F%8C%E8%B0%83%E6%8E%92%E5%BA%8F%E5%99%A8&action=edit&redlink=1) [Batcher归并网络](https://zh.wikipedia.org/wiki/Batcher%E5%BD%92%E5%B9%B6%E7%BD%91%E7%BB%9C) [两两排序网络](https://zh.wikipedia.org/w/index.php?title=%E4%B8%A4%E4%B8%A4%E6%8E%92%E5%BA%8F%E7%BD%91%E7%BB%9C&action=edit&redlink=1)                                                                                                                                                                                                                                                                                                       |
| 混合排序 | [块排序](https://zh.wikipedia.org/w/index.php?title=%E5%A1%8A%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [Tim排序](https://zh.wikipedia.org/w/index.php?title=Tim%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [内省排序](https://zh.wikipedia.org/wiki/Introsort) [Spread排序](https://zh.wikipedia.org/w/index.php?title=Spread%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [J排序](https://zh.wikipedia.org/w/index.php?title=J%E6%8E%92%E5%BA%8F&action=edit&redlink=1)                                                                                                                                                                                                    |
| 其他   | [拓扑排序](https://zh.wikipedia.org/wiki/%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F) [煎饼排序](https://zh.wikipedia.org/w/index.php?title=%E7%85%8E%E9%A4%85%E6%8E%92%E5%BA%8F&action=edit&redlink=1) [意粉排序](https://zh.wikipedia.org/w/index.php?title=%E6%84%8F%E7%B2%89%E6%8E%92%E5%BA%8F&action=edit&redlink=1)                                                                                                                                                                                                                                                                                                                                                   |

* 稳定/不稳定：**稳定排序算法**会让原本有相等键值的纪录维持**相对次序**。也就是如果一个排序算法是**稳定**的，当有两个相等键值的纪录*R*和*S*，且在原本的列表中*R*出现在*S*之前，在排序过的列表中*R*也将会是在*S*之前。
* 适应性/非适应性：**非适应性**的算法执行的操作序列独立于数据的顺序。**自适应**的排序执行不同的操作序列。
* 内部排序/外部排序：内部排序允许随机访问，而外部排序算法必须顺序访问元素（至少在大数据块内）
* 可否应用于链表。
* 是否为原地排序（in-place），原地排序的算法除了少量变量不需要使用额外的空间保存副本。


## 排序算法性能速查


| 类别   | 排序方法 | 平均时间复杂度           | 最好时间复杂度           | 最坏时间复杂度           | 空间复杂度             | 稳定性 |
|------|------|-------------------|-------------------|-------------------|-------------------|-----|
| 插入排序 | 直接插入 | $O(n^2)$          | $O(n)$            | $O(n^2)$          | $O(1)$            | 稳定  |
|      | 希尔排序 | $O(n^{1.3})$      | $O(n)$            | $O(n^2)$          | $O(1)$            | 不稳定 |
| 选择排序 | 直接选择 | $O(n^2)$          | $O(n^2)$          | $O(n^2)$          | $O(1)$            | 不稳定 |
|      | 堆排序  | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(1)$            | 不稳定 |
| 交换排序 | 冒泡排序 | $O(n^2)$          | $O(n^2)$          | $O(n^2)$          | $O(1)$            | 稳定  |
|      | 快速排序 | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(n^2)$          | $O(n\log_{2}{n})$ | 不稳定 |
| 归并排序 | 归并排序 | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(1)$            | 稳定  |

### 速记方法
* 四大类基本排序：插入，选择，交换，归并。
* 插入进阶版本为希尔，选择进阶版本为堆排，冒泡进阶版本为快排。
* 只有简单的排序方法才是稳定的，但选择排序是不稳定的。直接插入，冒泡和归并是稳定的。
* 只有堆排序和归并排序能保证最坏情况下的时间复杂度
* 对于小规模的数据，基本排序算法反而具有一定优势。


### 分析框架

任何待排序的元素，都需要实现两种操作，比较与交换。

这里给出了Python的例子，包括生成随机数组，检验数组是否有序，检验排序函数是否正确的函数。

```python
# Auxiliary Functions
def swap(A,i,j):
     A[i],A[j] = A[j],A[i]
    
def less(i,j):
  	 return i < j

# generate random data
import random
def random_data(size=1000):
    data = range(size)
    random.shuffle(data)
    return data

# test array is sorted
def is_sorted(data, cmp=None):
    if not cmp: cmp = less
    for i in range(1, len(data)):
        if cmp(data[i], data[i - 1]) < 0: return False
    return True
  
def test_sort(func=sorted):print(is_sorted(func(random_data())))
```



## 选择排序 Selection Sort

**选择排序**是一种最简单的基本排序算法，它通过不断**选择**出剩余元素中的最小元素实现。

插入排序的核心思路是：将数据分为（有序区，无序区），每次选择无序区的最小元素，放入有序区的末尾。对于有n个元素的数组，它会执行`n-1`次选择，因为最后一次剩下的肯定是最大的元素。

选择排序的缺点是，它的运行时间对文件中已有序的部分依赖较少，每一次都会找最小元素，没有充分利用原有序列中的有序部分。反过来讲，选择排序对输入的初始次序不敏感，最坏情况和最好情况区别不大。

其优点在于，选择排序比较次数较多，但交换次数是所有排序算法中最少的。对于交换的开销远大于比较的元素类型（大元素小关键字），可以使用选择排序。但对于比较的开销较大（例如字符串类型比较）的元素，插入排序是更好的选择。

其进阶版本是堆排序(Heap Sort)

### 分析

```
i ∈ [0, N)
    swap(A[i], A[min_index(A[i:N])] )
```

* 循环不变量：每次循环开始时，前段`A[0:i]`有序，后段`A[i:N]`无序。
* 初始条件：排序开始前`i=0`，前段空数组`A[0:0]`有序，后段全数组`A[0:N]`无序。
* 结束条件：迭代结束时`i=N`，此时前段全数组`A[0:N]`有序，后段空数组`A[N:N]`无序，整个数组有序。
* 保持性质：
  * 每轮迭代结束，会使无序区`A[i:N]`内最小元素与`A[i]`互换位置。该元素为有序区内最大元素。
  * 每轮迭代使得`A[i]`加入有序区，前段有序区增长为`A[0:i+1]`，后段无序区收缩为`A[i+1:N]`。
  * 下一轮迭代开始时`i=i+1`，循环不变量得到保持。

### 实现

```python
def selection_sort(A):
    n = len(A)
    for i in range(0,n):
        min_index = i
        for j in range(i,n):
            if less(A[j], A[min_index]): min_index = j
        swap(A,i , min_index)
    return A
```

### 特性

* 不稳定的排序
* 原地操作
* 非适应性排序：对输入的初始次序不敏感，最坏情况和最好情况区别不大。
* 交换次数在所有基本排序算法中最少，但比较次数较多
* 选择排序在执行中，有序区域前段保持不变。
* 适合对链表排序。

| 项目\情况 |        平均情况        |        最差情况        |        最好情况        |
|-------|:------------------:|:------------------:|:------------------:|
| 时间复杂度 |      $O(n^2)$      |      $O(n^2)$      |      $O(n^2)$      |
| 比较次数  | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ |
| 交换次数  |       $n-1$        |       $n-1$        |       $n-1$        |


## 插入排序 Insertion Sort

插入排序是一种简单直观的基本排序算法，它从无序区首部拉取一个元素，放入有序区的恰当位置。类似扑克牌理牌的操作。它是稳定的原地排序算法，而且具有较强的局部性。

插入排序的核心思路是：将数据分为（有序区，无序区），把无序区的第一个元素插入到有序区中的正确位置中。通常是通过不断前移至合适的位置实现的。

与选择排序不同，插入排序是适应性算法，其运行时间与原始序列的有序程度密切相关。同时它还是稳定的排序算法，也是原地排序。

### 分析

```
i ∈ [1, N)
    A[0:i+1] = put_properly( A[0,i) , A[i] )
```

* 循环不变量：每次循环开始时，前段`A[0:i]`有序，后段`A[i:N]`无序。
* 初始条件：排序开始前`i=1`，前段单元素数组`A[0:1]`有序，后段数组`A[1:N]`无序。
* 结束条件：迭代结束时`i=N`，此时前段全数组`A[0:N]`有序，后段空数组`A[N:N]`无序，整个数组有序。
* 保持性质：
  * 每轮迭代结束，会使元素`A[i]`位于前段有序数组中的合适位置，
  * 每轮迭代使得`A[i]`加入有序区，前段有序区增长为`A[0:i+1]`，后段无序区收缩为`A[i+1:N]`。
  * 下一轮迭代开始时`i=i+1`，循环不变量得到保持。

### 实现

```python
def insertion_sort(A):
    n = len(A)
    for i in range(1,n):
        j = i
        while less(A[j-1], A[j]) and j > 0:
            swap(A, j-1, j)
            j -= 1
    return A
```

如果当前元素的前一个元素比当前元素还要小，那么就交换两个元素。

如果选择的`A[i]`比有序区的所有元素都要小，它就应当放到`A[0]`的位置，这时候在循环条件中还需要额外检查索引是否到头`j>0`，如果已经到头，则上一次循环已经执行了`swap(A,0,1)`，将元素放在了合适的位置，就应当跳出循环避免索引越界。

可以通过观察哨关键字来简化插入排序，但并不是所有的时候都好用，例如最小值难以定义，没有额外的空间。一种取巧的办法是在第一次迭代中执行一次冒泡或选择排序，将最小的元素放在数组首部，当做观察哨。改进实现：

```python
def insertion_sort2(A):
    n = len(A)
    for i in range(n-1, 0, -1):
        if less(A[i], A[i-1]):
            swap(A, i , i-1)
            
    for i in range(1, n):
        j = i
        v = A[j]
        while less( v , A[j-1]):
            A[j] = A[j-1]
            j -= 1
        A[j] = v
    return A
```

改进实现主要包括，第一次使用逆向冒泡，在`A[0]`处生成最小元素观察哨，顺便消除一些逆序对。在后续的循环中，迭代条件就不需要判断索引是否越界了。同时将迭代中的交换改为赋值，可以减少一倍的赋值操作。

### 特性

* 稳定的排序
* 原地排序
* 适应性排序算法，初始序列大量有序的情况下执行很快。
* 比较次数少，但交换次数多。
* 只访问有序部分的元素，而且是顺序访问，局部性较强。但有序区域在排序过程中会发生变化。

| 项目\情况 | 平均情况           | 最差情况               | 最好情况   |
| ----- | -------------- | ------------------ | ------ |
| 时间复杂度 | $O(n^2)$       | $O(n^2)$           | $O(n)$ |
| 空间复杂度 | $O(n^2)$       | $O(n^2)$           | $O(1)$ |
| 比较次数  | $\frac{n^2} 4$ | $\frac{n(n-1)}{2}$ | $n-1$  |
| 交换次数  | $\frac{n^2} 4$ | $\frac{n(n-1)}{2}$ | 0      |





## 冒泡排序 Bubble Sort

冒泡排序是一种**交换排序**，它通过不断修正序列中的逆序对实现，每一轮冒泡都会使前面无序区的最大元素上浮至后段有序区。它的实现是最简单的。

冒泡排序的核心思路是：将数据分为（无序区，有序区），从无序区通过交换找出最大元素放到有序区前端。重复n-1次后即可保证数组有序。

### 分析

```
i ∈ [0, N-1)
    j ∈ [0, N-i-1）
        if less( A[j+1], A[j] ):
            swap(A, j+1, j) 
```

* 循环不变量：每次循环开始时，前段`A[0:N-i]`无序，后段`A[N-i:N]`有序。
* 初始条件：排序开始前`i=0`，前段全数组`A[0:N]`无序，后段空数组`A[N:N]`有序，整个数组无序。
* 结束条件：迭代结束时`i=N`，此时前段空数组`A[0:0]`无序，后段全数组`A[0:N]`有序，整个数组有序。
* 保持性质：
  * 每轮迭代结束，会使`A[0:N-i]`中最大元素上浮至`A[N-i]`，且该元素小于后段有序区中所有元素。
  * 每轮迭代使得无序区收缩为`A[0:N-i-1]`，有序区增长为`A[N-i-1:N]`。
  * 下一轮迭代开始时`i=i+1`，前段`A[0:N-(i+1)]`无序，后段`A[N-(i+1):N]`有序，循环不变量得到保持。

### 实现

```python
def bubble_sort(A):
    n = len(A)
    for i in range(n-1):
        for j in range(0, n-1-i):
            if less(A[j+1], A[j]):
                swap(A, j, j+1)
    return A
```

### 特性

* 属于交换排序
* 稳定排序
* 原地排序，空间复杂度 $O(1)$ 
* 实现极其简单。两层迭代，外侧` range(n-1)`，内侧`range(n-1-i)`。

| 项目\情况 |        平均情况        |        最差情况        |        最好情况        |
|-------|:------------------:|:------------------:|:------------------:|
| 时间复杂度 |      $O(n^2)$      |      $O(n^2)$      |      $O(n^2)$      |
| 比较次数  | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ |
| 交换次数  |        逆序数         | $\frac{n(n-1)}{2}$ |         0          |





## 希尔排序 Shell Sort

希尔排序是一种指定步长的插入排序。也称为**递减增量排序算法**，是插入排序的改良版本。

插入排序运行效率低的原因在于，它所执行的交换操作都是近邻元素，所以每次元素至多移动一位。所以例如最小的元素在数组尾端的极端情况，插入排序就需要N次交换才能把它放回到数组的最前端。希尔排序通过允许非相邻元素之间的交换，能够显著提高执行效率。

希尔排序的本质是将文件重排列，使得文件具有如下性质：每第h元素产生一个排好序的序列。例如h=3

则要求数组中序列`[0,3,6,...,3n,...]是有序的。这样的文件称为**h-排序**的。通过较大的h排序文件会使小h排序更加容易。当h=1时，就是普通的插入排序。因此通过一个最后为1的步长序列，不断进行h-排序，就可以得到一个排好序的文件。

### 分析

希尔排序的的关键是使用合适的步长。当步长为1时，就是插入排序。所以任何步长序列都应当以1结束。通常可以使用knuth的步长序列。$h_{i+1} = 3h_i +1 $，即`1,4, 13,40,121,364,...`。

### 实现

```python
def shell_sort(A):
    n = len(A)
    steps = []
    h = 1
    while h <= n / 9:
        steps.insert(0,h)
        h = h * 3 + 1
        
    for h in steps:
        for i in range(h, n, h):
            j = i
            while less( A[j-h], A[j] ) and j - h >= 0:
                swap(A, j - h, j)
                j -= h
    return A
```

首先生成步长序列，最大的步长取数组长度的十分之一左右为宜。然后按照`...,40,13,4,1`的步长序列，依次执行h-插入排序，区别就在于原来插入排序中的`1`都用`h`替代即可。

### 特性

* 已知的最好希尔步长序列为：1, 5, 19, 41, 109


* 属于高级插入排序
* 不稳定排序
* 适应性排序。
* 原地排序，空间复杂度 $O(1)$ 



## 计数排序

计数排序又称为关键词索引统计排序，它不属于比较排序。当关键字的范围是确定而且比较小时，可以通过计数排序高效的进行排序。

计数排序用到的思想与计算百分位点类似。首先求得数据的分布CDF。然后依次查询原数组每个元素的rank()，并将该元素放入`rank()`指定的位置上。

### 实现

```python
def count_sort(A):
    M, N = max(A) + 2, len(A)  # 若A中最大元素为M，则还需要0和M两个额外空间。
    buf = [0 for i in range(N)]  # A的重排列副本

    # 构造CDF, cnt[i]返回小于i的元素个数
    cnt = [0 for i in range(M)]
    for i in range(N): cnt[A[i] + 1] += 1  # 统计当前i出现次数,加到后面去。
    for j in range(1, M): cnt[j] += cnt[j - 1]  # 变PDF为CDF

    for i in range(0, N):  # 对A中所有元素执行遍历，准备分配新位置。
        # shortcut: res[ cnt[A[i]]++ ] = A[i]
        index = cnt[A[i]]  # 查阅CDF，找到该元素的排序分位点。
        cnt[A[i]] += 1  # 如果A[i]是重复的元素，下次查询分位数应当+1
        buf[index] = A[i]

    for i in range(N): A[i] = buf[i]
    return A
```





## 快速排序 Quick Sort

快速排序是一种高级的交换排序，又称为 划分-交换排序(partition-exchange sort)。快排是应用最广泛的排序算法。属于广义的选择排序，运用了分治法。

快排的核心思想是：将数组划分为两个部分，然后分别对两个部分进行排序。划分的过程是关键，它需要保证：

* 对于某个`i`, `a[i]`在数组的最终位置上。
* `a[0],...,a[i-1]`中的元素都比`A[i]`小。
* `a[i+1],...a[N-1]`中的元素逗比`A[i]`大。

### 分析

递归版本的qsort可以简要表示如下(Fired version)

```python
def qsort(A):
    if len(A) <= 1: return A
    return qsort([i for i in A[1:] if i<A[0]]) + [A[0]] + qsort([i for i in A[1:] if i>=A[0]])
```

如何选取`pivot`是一个大问题。通常来说可以选取最后一个元素作为pivot，但更好的方式是随机选择一个元素

### 实现

一个更为合理且简洁的实现如下：

```python
def qsort(A, lo, hi):
    # hi is the last index of A. so it's n-1 not n
    if lo >= hi:  # 0 or 1 element: do nothing
        return

    pivot = A[random.randint(lo, hi)] 
    i, j = lo, hi
    while i <= j:
        while less(A[i], pivot): i += 1
        while less(pivot, A[j]): j -= 1
        if i <= j:
            swap(A, i, j)
            i, j = i + 1, j - 1
    qsort(A, lo, j)
    qsort(A, i, hi)
```

边界条件分析，当退出`while`循环时有`i>j`，这时候需要证明数组满足以下条件：

* $k∈ [lo,j) , A_k < pivot$
* $k∈ (j,i) , A_k = pivot$
* $k∈ [i,hi) , A_k > pivot$

实在不想证明了。

### 特性

* 不稳定的排序算法
* 原位排序，递归版本需要空间复杂度$O(\log n)$保存调用信息，相比很小。
* 平均排序复杂度为$O(n\log n)$，内部循环很小，可以高效地在大多数架构上实现。通常比其他的$O(n \log n)$排序算法要快。
* 最坏情况下复杂度为$O(n^2)$
* 对大型文件，快排的性能是希尔排序的5~10倍。但对于小文件，希尔反而可能更胜一筹。一种常见的优化方式是，当`hi-lo`小于某个特定值，例如12时，使用其他排序方法，例如希尔排序。这也是GO标准库`sort`中使用的方式。Sedgewick给出的一个小文件阈值是9。

| 项目\情况 |          平均情况          |        最差情况        |       最好情况ß       |
|-------|:----------------------:|:------------------:|:-----------------:|
| 时间复杂度 | $O(1.39 n\log_{2}{n})$ | $O(n\log_{2}{n})$  | $O(n\log_{2}{n})$ |
| 空间复杂度 |      $O(\log n)$       |       $O(n)$       |    $O(\log n)$    |
| 比较次数  |      $O(n\log n)$      | $\frac{n(n-1)}{2}$ |   $O(n\log n)$    |




## 归并排序 Merge Sort

归并（merging）是将两个排好序的文件组合成一个较大的有序文件

* 归并的实现


归并是归并排序的核心，核心思想是，如果某子数组已经到头，则续以另一个子数组的元素，如果都没有到头，再比较两个子数组当前元素的大小。

```c
def merge_ab(a, b):
    na, nb, nc = len(a), len(b), len(a) + len(b)
    c = [0] * nc
    i, j = 0, 0
    for k in range(nc):
        if i == na:
            c[k] = b[j]
            j += 1
            continue
        if j == nb:
            c[k] = a[i]
            i += 1
            continue
        if a[i] < b[j]:
            c[k] = a[i]
            i += 1
        else:
            c[k] = b[j]
            j += 1
    return c
```

对于链表的归并，稍微复杂一点，这里考虑没有链表头节点，以nil结尾的链表，则合并链表的逻辑如下：

```go
type Node struct {
	Val  int
	Next *Node
}

func MergeLinkList(a *Node, b *Node) *Node {
	var head Node
	cursor := &head

	for a != nil && b != nil {
		if a.Val < b.Val {
			cursor.Next = a
			cursor = cursor.Next
			a = a.Next
		} else {
			cursor.Next = b
			cursor = cursor.Next
			b = b.Next
		}
	}

	if a == nil {
		cursor.Next = b
	} else {
		cursor.Next = a
	}
	return head.Next
}
```

在有归并方法的基础上，归并排序实现相当简单：

```python
def msort(A, lo, hi):
    if lo >= hi: return
    mid = lo + ((hi - lo) >> 1)
    msort(A, lo, mid)
    msort(A, mid + 1, hi)
    merge(A, lo, mid, hi)
    return
```

* 稳定排序


* 空间复杂度$O(n)$，需要基本等量的额外存储空间。
* 如果使用的归并方法是稳定的，则归并排序是稳定的。
* 采用分治法，由冯·诺依曼提出。
* 可以并行运行
* 可以方便地应用于链表，慢速外部存储，外部排序。

| 项目\情况 |       平均情况        |       最差情况        |         最好情况         |
|-------|:-----------------:|:-----------------:|:--------------------:|
| 时间复杂度 | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ |  $O(n\log_{2}{n})$   |
| 比较次数  |   $O(n\log n)$    | $n\log_2n - n+1$  | $\frac{n\log_2n}{2}$ |




## 堆排序 Heap Sort 与优先队列

堆排序是特殊的排序方式，利用了优先队列的性质。实现良好的优先队列可以实现对数级别的插入元素/删除最大(最小)元素操作。因此对于待排序的n个元素，只要构建一个优先队列，并不断取出最大（最小）元素即可完成排序。

通常使用二叉堆来实现优先队列。

当一颗二叉树的每个节点都大于等于它的两个子节点时，称之为堆有序。这时根节点就是堆有序二叉树的根节点。

二叉堆是一组能够用堆有序的完全二叉树排序的元素，并且在数组中按照层级存储。

如何在数组中表示一颗完全二叉树，一种简单的方式是，首元素置空，然后`A[1]`放置二叉树的根，`A[2],A[3]`是根节点的两个子节点，而`A[4],A[5],A[6],A[7]`则是第三层的节点。

这样表示完全二叉树有一些优良的性质：位置为`k`的节点，其父节点位置为`floor(n/2)`，在计算中就是`n/2`，而其两个儿子的位置分别为`2k`与`2k+1`。一颗大小为N的完全二叉树，高度为`floor(lgN)`

 堆的关键操作在于上浮和下沉操作的实现。插入元素其实是在堆尾添加一个元素，并使之上浮至合适的位置。删除最大元素，实质上是删除数组首元素，从数组尾部取元素填空，并使之下沉至合适位置。

```python
class Heap(object):
	def __init__(self):
		self.N = 0
		self.A = [0]
	

	def sink(k):
		while 2*k <= self.N:
			son = 2*k
			# choose big son
			if son + 1 <= self.N and A[son+1]>A[son]:son += 1
			# big son fight papa
			if A[son] > A[k]: swap(A, son, k)
			# history never change
k = son  


	def swim(k):
		while k >= 1 and A[k>>1] < A[k]:
			swap(A, papa, k)
			k >>= 1


	def insert(e):
		self.A.append(e)
		self.N += 1
		self.swim(self.N)


	def delmax(e):
		max_item = self.A[1]
		spare = self.A.pop()
		self.N -= 1
		self.A[1] = spare
		self.sink(1)
return max_item
		
```

 相应的，堆排序使用类似的机制。首先从数组中创建一个堆，然后依次取出堆中的最大元素。放在数组末尾。

```python
def sink(A, k, N):
    """assume A has a dummy head, N is heap element count"""
    while 2 * k <= N:
        son = 2 * k
        if son + 1 <= N and A[son + 1] > A[son]:
            son += 1
        if A[son] > A[k]:
            A[son], A[k] = A[k], A[son]
        k = son
 
def heap_sort(A):
	if not A or len(A) == 1: return A
	n = len(A)
	A.insert(0,0)	# add dummy head make head operation a lot more easy
	
	# heap creation
	for i in range(n>>1, 0 , -1):
		sink(A, i , n)

	# heap destruction
	while n > 1:
		# first ele of heap is the max item, move to tail
		swap(A, 1, n)
		# adjust heap by sink head element down, with heap size down by 1
		n -= 1
		sink(A, 1, n)
		
	A.pop(0)	# pop out the dummy head
	return A
```

### 特性

* 堆排序在最坏情况下也能保证$O(n\log n)$的时间复杂度，并使用恒定的额外空间。
* 堆排序实现简单。
* 堆排序的访问局部性很差，经常出现缓存miss。
* 使用哑元有助于简化堆排序的代码
