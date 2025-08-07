---
title: "Overview of Sorting Algorithms"
date: 2016-09-23
author: vonng
summary: |
  Sorting algorithms are the most fundamental, widely applicable, and frequently tested algorithms in interviews. This article summarizes classic sorting algorithms: selection sort, insertion sort, bubble sort, shell sort, counting sort, quicksort, merge sort, and heap sort - their principles and implementations.
---


> Sorting algorithms are the most fundamental, widely applicable, and frequently tested algorithms in interviews.

A **sorting algorithm** is an algorithm that can arrange a string of data in a specific order. Where:

* Output result is an ascending sequence
* Output result is a permutation or reorganization of the original input

Two basic operations required for sortable objects are: Compare and Swap


## Classification of Sorting Algorithms

| Category   | Subcategories                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Exchange Sort | [Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort) [Cocktail Sort](https://en.wikipedia.org/wiki/Cocktail_shaker_sort) [Odd-even Sort](https://en.wikipedia.org/wiki/Odd%E2%80%93even_sort) [Comb Sort](https://en.wikipedia.org/wiki/Comb_sort) [Gnome Sort](https://en.wikipedia.org/wiki/Gnome_sort) [Quicksort](https://en.wikipedia.org/wiki/Quicksort) [Stooge Sort](https://en.wikipedia.org/wiki/Stooge_sort) [Bogosort](https://en.wikipedia.org/wiki/Bogosort) |
| Selection Sort | [Selection Sort](https://en.wikipedia.org/wiki/Selection_sort) [Heapsort](https://en.wikipedia.org/wiki/Heapsort) [Smoothsort](https://en.wikipedia.org/wiki/Smoothsort) [Cartesian Tree Sort](https://en.wikipedia.org/wiki/Cartesian_tree) [Tournament Sort](https://en.wikipedia.org/wiki/Tournament_sort) [Cycle Sort](https://en.wikipedia.org/wiki/Cycle_sort)                                  |
| Insertion Sort | [Insertion Sort](https://en.wikipedia.org/wiki/Insertion_sort) [Shellsort](https://en.wikipedia.org/wiki/Shellsort) [Splay Sort](https://en.wikipedia.org/wiki/Splay_tree) [Binary Search Tree Sort](https://en.wikipedia.org/wiki/Binary_search_tree) [Library Sort](https://en.wikipedia.org/wiki/Library_sort) [Patience Sort](https://en.wikipedia.org/wiki/Patience_sorting)                                                                                                                                                                           |
| Merge Sort | [Merge Sort](https://en.wikipedia.org/wiki/Merge_sort) [Cascade Merge Sort](https://en.wikipedia.org/wiki/Merge_sort) [Oscillating Merge Sort](https://en.wikipedia.org/wiki/Merge_sort) [Polyphase Merge Sort](https://en.wikipedia.org/wiki/Merge_sort) [Strand Sort](https://en.wikipedia.org/wiki/Strand_sort)                                                           |
| Concurrent Sort | [Bitonic Sorter](https://en.wikipedia.org/wiki/Bitonic_sorter) [Batcher Odd-even Mergesort](https://en.wikipedia.org/wiki/Batcher_odd%E2%80%93even_mergesort) [Pairwise Sorting Network](https://en.wikipedia.org/wiki/Sorting_network)                                                                                                                                                                                                                                                                                                                       |
| Hybrid Sort | [Block Sort](https://en.wikipedia.org/wiki/Block_sort) [Timsort](https://en.wikipedia.org/wiki/Timsort) [Introsort](https://en.wikipedia.org/wiki/Introsort) [Spreadsort](https://en.wikipedia.org/wiki/Spreadsort) [UnShuffle Sort](https://en.wikipedia.org/wiki/UnShuffle_sort)                                                                                                                                                                                    |
| Other   | [Topological Sort](https://en.wikipedia.org/wiki/Topological_sorting) [Pancake Sort](https://en.wikipedia.org/wiki/Pancake_sorting) [Spaghetti Sort](https://en.wikipedia.org/wiki/Spaghetti_sort)                                                                                                                                                                                                                                                                                                                                                   |

* Stable/Unstable: **Stable sorting algorithms** maintain the **relative order** of records with equal keys. That is, if a sorting algorithm is **stable**, when there are two records *R* and *S* with equal keys, and *R* appears before *S* in the original list, *R* will also appear before *S* in the sorted list.
* Adaptive/Non-adaptive: **Non-adaptive** algorithms execute the same sequence of operations independent of data order. **Adaptive** sorting executes different operation sequences.
* Internal/External sorting: Internal sorting allows random access, while external sorting algorithms must access elements sequentially (at least within large data blocks)
* Applicability to linked lists.
* Whether it's in-place sorting. In-place sorting algorithms don't need extra space to save copies except for a few variables.


## Sorting Algorithm Performance Quick Reference


| Category   | Sorting Method | Average Time Complexity           | Best Time Complexity           | Worst Time Complexity           | Space Complexity             | Stability |
|------|------|-------------------|-------------------|-------------------|-------------------|-----|
| Insertion Sort | Direct Insertion | $O(n^2)$          | $O(n)$            | $O(n^2)$          | $O(1)$            | Stable  |
|      | Shell Sort | $O(n^{1.3})$      | $O(n)$            | $O(n^2)$          | $O(1)$            | Unstable |
| Selection Sort | Direct Selection | $O(n^2)$          | $O(n^2)$          | $O(n^2)$          | $O(1)$            | Unstable |
|      | Heap Sort  | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(1)$            | Unstable |
| Exchange Sort | Bubble Sort | $O(n^2)$          | $O(n^2)$          | $O(n^2)$          | $O(1)$            | Stable  |
|      | Quicksort | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(n^2)$          | $O(n\log_{2}{n})$ | Unstable |
| Merge Sort | Merge Sort | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ | $O(1)$            | Stable  |

### Memory Techniques
* Four major basic sorts: insertion, selection, exchange, merge.
* Advanced version of insertion is shell, selection is heap sort, bubble is quicksort.
* Only simple sorting methods are stable, but selection sort is unstable. Direct insertion, bubble, and merge are stable.
* Only heap sort and merge sort guarantee worst-case time complexity
* For small-scale data, basic sorting algorithms actually have certain advantages.


### Analysis Framework

Any elements to be sorted need to implement two operations: compare and swap.

Here are Python examples, including functions to generate random arrays, verify if arrays are sorted, and verify sorting function correctness.

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



## Selection Sort

**Selection sort** is one of the simplest basic sorting algorithms. It works by continuously **selecting** the smallest element from the remaining elements.

The core idea of selection sort is: divide data into (ordered region, unordered region), each time select the smallest element from the unordered region and place it at the end of the ordered region. For an array with n elements, it performs `n-1` selections, because the last remaining element must be the largest.

Selection sort's disadvantage is that its runtime has little dependency on already ordered parts in the file - it finds the minimum element every time without fully utilizing existing ordered portions in the original sequence. Conversely, selection sort is insensitive to initial input order, with little difference between worst and best cases.

Its advantage is that selection sort has more comparisons but the fewest swaps among all sorting algorithms. For element types where swap cost is much greater than comparison cost (large elements with small keys), selection sort can be used. For elements with high comparison costs (like string comparisons), insertion sort is a better choice.

Its advanced version is Heap Sort.

### Analysis

```
i ∈ [0, N)
    swap(A[i], A[min_index(A[i:N])] )
```

* Loop invariant: At the start of each loop, the front segment `A[0:i]` is ordered, the back segment `A[i:N]` is unordered.
* Initial condition: Before sorting begins `i=0`, front segment empty array `A[0:0]` is ordered, back segment full array `A[0:N]` is unordered.
* Termination condition: When iteration ends `i=N`, at this time front segment full array `A[0:N]` is ordered, back segment empty array `A[N:N]` is unordered, entire array is ordered.
* Maintenance property:
  * Each iteration end causes the minimum element in unordered region `A[i:N]` to swap positions with `A[i]`. This element becomes the maximum element in the ordered region.
  * Each iteration adds `A[i]` to the ordered region, front ordered region grows to `A[0:i+1]`, back unordered region shrinks to `A[i+1:N]`.
  * Next iteration begins with `i=i+1`, loop invariant is maintained.

### Implementation

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

### Characteristics

* Unstable sorting
* In-place operation
* Non-adaptive sorting: insensitive to initial input order, little difference between worst and best cases.
* Fewest swaps among all basic sorting algorithms, but more comparisons
* During execution, the ordered region at the front remains unchanged.
* Suitable for linked list sorting.

| Item\Case | Average Case           | Worst Case           | Best Case           |
|-------|:------------------:|:------------------:|:------------------:|
| Time Complexity | $O(n^2)$      | $O(n^2)$      | $O(n^2)$      |
| Comparisons  | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ |
| Swaps  | $n-1$        | $n-1$        | $n-1$        |


## Insertion Sort

Insertion sort is a simple and intuitive basic sorting algorithm that pulls an element from the unordered region's head and places it in the appropriate position in the ordered region. Similar to organizing playing cards. It's a stable in-place sorting algorithm with good locality.

The core idea of insertion sort is: divide data into (ordered region, unordered region), take the first element from the unordered region and insert it into the correct position in the ordered region. Usually implemented by continuously moving forward to the appropriate position.

Unlike selection sort, insertion sort is an adaptive algorithm whose runtime is closely related to the degree of order in the original sequence. It's also stable sorting and in-place sorting.

### Analysis

```
i ∈ [1, N)
    A[0:i+1] = put_properly( A[0,i) , A[i] )
```

* Loop invariant: At the start of each loop, front segment `A[0:i]` is ordered, back segment `A[i:N]` is unordered.
* Initial condition: Before sorting begins `i=1`, front single-element array `A[0:1]` is ordered, back array `A[1:N]` is unordered.
* Termination condition: When iteration ends `i=N`, at this time front full array `A[0:N]` is ordered, back empty array `A[N:N]` is unordered, entire array is ordered.
* Maintenance property:
  * Each iteration end places element `A[i]` in the appropriate position in the front ordered array,
  * Each iteration adds `A[i]` to the ordered region, front ordered region grows to `A[0:i+1]`, back unordered region shrinks to `A[i+1:N]`.
  * Next iteration begins with `i=i+1`, loop invariant is maintained.

### Implementation

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

If the previous element of the current element is smaller than the current element, swap the two elements.

If the selected `A[i]` is smaller than all elements in the ordered region, it should be placed at position `A[0]`. At this time, the loop condition needs additional checking if the index has reached the end `j>0`. If it has reached the end, the previous loop already executed `swap(A,0,1)`, placing the element in the appropriate position, and should break the loop to avoid index overflow.

Insertion sort can be simplified by using sentinel keys, but it's not always useful - for example, when minimum values are hard to define or there's no extra space. A clever approach is to perform one bubble or selection sort in the first iteration, placing the smallest element at the array head as a sentinel. Improved implementation:

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

The improved implementation mainly includes using reverse bubbling first to generate the minimum element sentinel at `A[0]`, incidentally eliminating some inverse pairs. In subsequent loops, the iteration condition no longer needs to check if the index is out of bounds. Also changing iteration swaps to assignments can reduce half the assignment operations.

### Characteristics

* Stable sorting
* In-place sorting
* Adaptive sorting algorithm, executes quickly when initial sequence is largely ordered.
* Fewer comparisons but many swaps.
* Only accesses elements in the ordered part, and sequentially, with good locality. But the ordered region changes during sorting.

| Item\Case | Average Case           | Worst Case               | Best Case   |
| ----- | -------------- | ------------------ | ------ |
| Time Complexity | $O(n^2)$       | $O(n^2)$           | $O(n)$ |
| Space Complexity | $O(n^2)$       | $O(n^2)$           | $O(1)$ |
| Comparisons  | $\frac{n^2}{4}$ | $\frac{n(n-1)}{2}$ | $n-1$  |
| Swaps  | $\frac{n^2}{4}$ | $\frac{n(n-1)}{2}$ | 0      |




## Bubble Sort

Bubble sort is an **exchange sort** that works by continuously correcting inverse pairs in the sequence. Each round of bubbling causes the largest element from the front unordered region to float up to the back ordered region. It has the simplest implementation.

The core idea of bubble sort is: divide data into (unordered region, ordered region), find the largest element from the unordered region through swaps and place it at the front of the ordered region. Repeat n-1 times to ensure array is sorted.

### Analysis

```
i ∈ [0, N-1)
    j ∈ [0, N-i-1）
        if less( A[j+1], A[j] ):
            swap(A, j+1, j) 
```

* Loop invariant: At the start of each loop, front segment `A[0:N-i]` is unordered, back segment `A[N-i:N]` is ordered.
* Initial condition: Before sorting begins `i=0`, front full array `A[0:N]` is unordered, back empty array `A[N:N]` is ordered, entire array is unordered.
* Termination condition: When iteration ends `i=N`, at this time front empty array `A[0:0]` is unordered, back full array `A[0:N]` is ordered, entire array is ordered.
* Maintenance property:
  * Each iteration end causes the largest element in `A[0:N-i]` to float up to `A[N-i]`, and this element is smaller than all elements in the back ordered region.
  * Each iteration shrinks the unordered region to `A[0:N-i-1]` and grows the ordered region to `A[N-i-1:N]`.
  * Next iteration begins with `i=i+1`, front segment `A[0:N-(i+1)]` is unordered, back segment `A[N-(i+1):N]` is ordered, loop invariant is maintained.

### Implementation

```python
def bubble_sort(A):
    n = len(A)
    for i in range(n-1):
        for j in range(0, n-1-i):
            if less(A[j+1], A[j]):
                swap(A, j, j+1)
    return A
```

### Characteristics

* Belongs to exchange sorting
* Stable sorting
* In-place sorting, space complexity $O(1)$ 
* Extremely simple implementation. Two iterations, outer `range(n-1)`, inner `range(n-1-i)`.

| Item\Case |        Average Case        |        Worst Case        |        Best Case        |
|-------|:------------------:|:------------------:|:------------------:|
| Time Complexity |      $O(n^2)$      |      $O(n^2)$      |      $O(n^2)$      |
| Comparisons  | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ | $\frac{n(n-1)}{2}$ |
| Swaps  |        Number of inversions         | $\frac{n(n-1)}{2}$ |         0          |




## Shell Sort

Shell sort is insertion sort with specified step sizes. Also called **diminishing increment sort algorithm**, it's an improved version of insertion sort.

Insertion sort runs inefficiently because it performs swaps only between adjacent elements, so each element moves at most one position per swap. In extreme cases like the smallest element at the array's tail, insertion sort needs N swaps to move it to the array's front. Shell sort significantly improves execution efficiency by allowing swaps between non-adjacent elements.

Shell sort's essence is rearranging the file so it has the property that taking every h-th element produces a sorted sequence. For example, h=3 requires sequences `[0,3,6,...,3n,...]` in the array to be sorted. Such files are called **h-sorted**. Sorting files with larger h makes smaller h sorting easier. When h=1, it becomes ordinary insertion sort. Therefore, using a step sequence ending with 1, continuously performing h-sorting can produce a sorted file.

### Analysis

Shell sort's key is using appropriate steps. When step is 1, it becomes insertion sort. So any step sequence should end with 1. Knuth's step sequence is commonly used: $h_{i+1} = 3h_i +1$, i.e., `1,4, 13,40,121,364,...`.

### Implementation

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

First generate the step sequence, with maximum step around one-tenth of array length. Then execute h-insertion sort according to step sequence `...,40,13,4,1`, the difference being replacing all `1`s in original insertion sort with `h`.

### Characteristics

* Best known shell step sequence is: 1, 5, 19, 41, 109


* Belongs to advanced insertion sort
* Unstable sorting
* Adaptive sorting.
* In-place sorting, space complexity $O(1)$ 



## Counting Sort

Counting sort, also called key-indexed counting sort, doesn't belong to comparison sorting. When the key range is determined and relatively small, counting sort can efficiently perform sorting.

Counting sort uses ideas similar to computing percentiles. First obtain the data's distribution CDF. Then query each element's rank() in the original array and place that element at the position specified by `rank()`.

### Implementation

```python
def count_sort(A):
    M, N = max(A) + 2, len(A)  # If max element in A is M, need 0 and M two extra spaces.
    buf = [0 for i in range(N)]  # Rearranged copy of A

    # Construct CDF, cnt[i] returns count of elements less than i
    cnt = [0 for i in range(M)]
    for i in range(N): cnt[A[i] + 1] += 1  # Count current i occurrences, add to next position.
    for j in range(1, M): cnt[j] += cnt[j - 1]  # Change PDF to CDF

    for i in range(0, N):  # Traverse all elements in A, prepare to assign new positions.
        # shortcut: res[ cnt[A[i]]++ ] = A[i]
        index = cnt[A[i]]  # Check CDF, find this element's sorting percentile.
        cnt[A[i]] += 1  # If A[i] is duplicate, next query should be +1
        buf[index] = A[i]

    for i in range(N): A[i] = buf[i]
    return A
```




## Quicksort

Quicksort is an advanced exchange sort, also called partition-exchange sort. Quicksort is the most widely applied sorting algorithm. Belongs to generalized selection sort, uses divide-and-conquer.

Quicksort's core idea is: partition the array into two parts, then sort both parts separately. The partitioning process is key, it must ensure:

* For some `i`, `a[i]` is in its final position in the array.
* Elements in `a[0],...,a[i-1]` are all smaller than `A[i]`.
* Elements in `a[i+1],...a[N-1]` are all larger than `A[i]`.

### Analysis

Recursive version of qsort can be briefly expressed as follows (Fired version)

```python
def qsort(A):
    if len(A) <= 1: return A
    return qsort([i for i in A[1:] if i<A[0]]) + [A[0]] + qsort([i for i in A[1:] if i>=A[0]])
```

How to choose `pivot` is a big problem. Usually the last element can be chosen as pivot, but a better approach is randomly selecting an element.

### Implementation

A more reasonable and concise implementation is as follows:

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

Boundary condition analysis: when exiting the `while` loop, we have `i>j`. At this time we need to prove the array satisfies:

* $k∈ [lo,j) , A_k < pivot$
* $k∈ (j,i) , A_k = pivot$
* $k∈ [i,hi) , A_k > pivot$

Don't want to prove this anymore.

### Characteristics

* Unstable sorting algorithm
* In-place sorting, recursive version needs space complexity $O(\log n)$ to save call information, which is relatively small.
* Average sorting complexity is $O(n\log n)$, with very small inner loops, can be efficiently implemented on most architectures. Usually faster than other $O(n \log n)$ sorting algorithms.
* Worst case complexity is $O(n^2)$
* For large files, quicksort performance is 5-10 times that of shell sort. But for small files, shell might be better. A common optimization is using other sorting methods like shell sort when `hi-lo` is smaller than a specific value like 12. This is also the approach used in GO's standard library `sort`. Sedgewick gives a small file threshold of 9.

| Item\Case |          Average Case          |        Worst Case        |       Best Case       |
|-------|:----------------------:|:------------------:|:-----------------:|
| Time Complexity | $O(1.39 n\log_{2}{n})$ | $O(n\log_{2}{n})$  | $O(n\log_{2}{n})$ |
| Space Complexity |      $O(\log n)$       |       $O(n)$       |    $O(\log n)$    |
| Comparisons  |      $O(n\log n)$      | $\frac{n(n-1)}{2}$ |   $O(n\log n)$    |




## Merge Sort

**Merging** is combining two sorted files into one larger ordered file.

* Merge implementation


Merging is the core of merge sort. The core idea is: if a subarray has reached the end, continue with elements from the other subarray; if neither has reached the end, compare the current elements of both subarrays.

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

For linked list merging, it's slightly more complex. Here considering linked lists without head nodes, ending with nil, the merge logic is:

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

With the merge method, merge sort implementation is quite simple:

```python
def msort(A, lo, hi):
    if lo >= hi: return
    mid = lo + ((hi - lo) >> 1)
    msort(A, lo, mid)
    msort(A, mid + 1, hi)
    merge(A, lo, mid, hi)
    return
```

* Stable sorting


* Space complexity $O(n)$, needs basically equivalent additional storage space.
* If the merge method used is stable, then merge sort is stable.
* Uses divide-and-conquer, proposed by von Neumann.
* Can run in parallel
* Can be conveniently applied to linked lists, slow external storage, external sorting.

| Item\Case |       Average Case        |       Worst Case        |         Best Case         |
|-------|:-----------------:|:-----------------:|:--------------------:|
| Time Complexity | $O(n\log_{2}{n})$ | $O(n\log_{2}{n})$ |  $O(n\log_{2}{n})$   |
| Comparisons  |   $O(n\log n)$    | $n\log_2n - n+1$  | $\frac{n\log_2n}{2}$ |




## Heap Sort & Priority Queue

Heap sort is a special sorting method that utilizes priority queue properties. Well-implemented priority queues can achieve logarithmic-level insert element/delete maximum(minimum) element operations. Therefore, for n elements to be sorted, just build a priority queue and continuously extract the maximum (minimum) element to complete sorting.

Binary heaps are usually used to implement priority queues.

When each node of a binary tree is greater than or equal to its two children, it's called heap-ordered. At this time, the root node is the root of the heap-ordered binary tree.

A binary heap is a set of elements that can be sorted using heap-ordered complete binary trees and stored in arrays by level.

How to represent a complete binary tree in an array: a simple way is to leave the first element empty, then place the binary tree root in `A[1]`, `A[2],A[3]` are the root's two children, and `A[4],A[5],A[6],A[7]` are the third level nodes.

This representation of complete binary trees has excellent properties: for a node at position `k`, its parent is at position `floor(n/2)` (which is `n/2` in computation), and its two children are at positions `2k` and `2k+1`. A complete binary tree of size N has height `floor(lgN)`.

Key heap operations are sink and swim operations. Inserting an element actually adds an element to the heap's tail and makes it swim to the appropriate position. Deleting the maximum element essentially deletes the first array element, takes an element from the array's tail to fill the gap, and makes it sink to the appropriate position.

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

Correspondingly, heap sort uses similar mechanisms. First create a heap from the array, then successively extract the maximum elements from the heap and place them at the array's end.

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

### Characteristics

* Heap sort can guarantee $O(n\log n)$ time complexity in the worst case while using constant extra space.
* Heap sort implementation is simple.
* Heap sort has poor access locality, frequently causing cache misses.
* Using dummy elements helps simplify heap sort code