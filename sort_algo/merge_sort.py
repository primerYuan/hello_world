"""归并排序 / Merge sort.

自顶向下（top-down）归并，时间复杂度稳定 O(n log n)，额外空间 O(n)。

与快排相比的两个特点
--------------------
* **稳定（stable）**：相等元素的原始相对顺序被保留，可用于多关键字排序。
* **最坏也是 O(n log n)**：不存在快排的 pivot 退化问题，实时性可预测。

实现要点
--------
1. **稳定合并**：合并两段时用 ``<=`` 判断取左段，相等元素优先取左边。
   稳定性由"下标作为最终 tie-breaker"在代理对象里显式保证。
2. **有序短路**：若 ``a[mid] <= a[mid + 1]``，两段已整体有序，跳过合并。
   对部分有序数据可退化为 O(n)。
3. **小数组走插入排序**：子区间长度 <= ``INSERTION_THRESHOLD`` 时用插入
   排序，减少递归层数和函数调用开销。
4. **辅助缓冲只分配一次**：整个排序复用同一块 ``buf``，避免每层递归都
   新建列表（Python 里这是主要常数开销）。
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")

INSERTION_THRESHOLD = 16


class _Item:
    """排序代理：把 ``(key, index, value)`` 打包成可比较对象。

    相等 key 时用 ``index`` 兜底，从而在升序/降序遍历中都保持稳定性。
    """

    __slots__ = ("key", "index", "value", "reverse")

    def __init__(self, key: Any, index: int, value: Any, reverse: bool) -> None:
        self.key = key
        self.index = index
        self.value = value
        self.reverse = reverse

    def __lt__(self, other: "_Item") -> bool:
        if self.key == other.key:
            return self.index < other.index  # 稳定：保持原始顺序
        return other.key < self.key if self.reverse else self.key < other.key

    def __le__(self, other: "_Item") -> bool:
        if self.key == other.key:
            return self.index <= other.index
        return other.key <= self.key if self.reverse else self.key <= other.key


def merge_sort(
    seq: Sequence[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> List[T]:
    """返回 ``seq`` 排序后的新列表，不修改入参。

    :param seq: 任意序列 / 可迭代对象。
    :param key: 排序键函数，语义同 :func:`sorted` 的 ``key``。
    :param reverse: ``True`` 为降序（降序时仍保持稳定性）。
    :return: 排序后的新列表。

    >>> merge_sort([3, 1, 2])
    [1, 2, 3]
    >>> merge_sort([])
    []
    >>> merge_sort([5, 2, 9, 2])
    [2, 2, 5, 9]
    >>> merge_sort([3, 1, 2], reverse=True)
    [3, 2, 1]
    >>> merge_sort(["bb", "a", "ccc"], key=len)
    ['a', 'bb', 'ccc']
    >>> merge_sort([(1, "a"), (0, "b"), (1, "c")], key=lambda t: t[0])
    [(0, 'b'), (1, 'a'), (1, 'c')]
    """
    items = list(seq)
    if len(items) < 2:
        return items

    # 快速路径：无 key、非降序，直接对原值排序（少一层间接访问）
    if key is None and not reverse:
        buf: List[Any] = [None] * len(items)
        _sort(items, buf, 0, len(items) - 1)
        return items

    proxies = [
        _Item(key(x) if key else x, i, x, reverse)
        for i, x in enumerate(items)
    ]
    buf = [None] * len(proxies)
    _sort(proxies, buf, 0, len(proxies) - 1)
    return [p.value for p in proxies]


def _sort(a: List[Any], buf: List[Any], lo: int, hi: int) -> None:
    """对闭区间 ``a[lo..hi]`` 归并排序，``buf`` 为复用的辅助缓冲。"""
    if lo >= hi:
        return

    if hi - lo + 1 <= INSERTION_THRESHOLD:
        _insertion_sort(a, lo, hi)
        return

    mid = (lo + hi) // 2
    _sort(a, buf, lo, mid)
    _sort(a, buf, mid + 1, hi)

    if a[mid] <= a[mid + 1]:  # 已经整体有序，跳过合并
        return

    _merge(a, buf, lo, mid, hi)


def _merge(a: List[Any], buf: List[Any], lo: int, mid: int, hi: int) -> None:
    """合并 ``a[lo..mid]`` 与 ``a[mid+1..hi]``（各自已有序）。"""
    buf[lo : hi + 1] = a[lo : hi + 1]
    i, j = lo, mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = buf[j]
            j += 1
        elif j > hi:
            a[k] = buf[i]
            i += 1
        elif buf[j] < buf[i]:  # 严格小于才取右边 => 稳定
            a[k] = buf[j]
            j += 1
        else:
            a[k] = buf[i]
            i += 1


def _insertion_sort(a: List[Any], lo: int, hi: int) -> None:
    """对闭区间 ``a[lo..hi]`` 做插入排序。"""
    for i in range(lo + 1, hi + 1):
        cur = a[i]
        j = i - 1
        while j >= lo and cur < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur


if __name__ == "__main__":
    import random

    data = [random.randint(-100, 100) for _ in range(20)]
    print("before:", data)
    print("after :", merge_sort(data))
