"""快速排序 / Quicksort.

原地（in-place）排序，平均时间复杂度 O(n log n)，最坏 O(n^2)。

实现要点
--------
1. **pivot 选择**：取 ``a[(lo + hi) // 2]``（中间元素），规避"已排序输入 +
   首元素 pivot"退化成 O(n^2) 的经典陷阱。
2. **三路切分**（Dutch National Flag）：把区间切成
   ``< pivot`` / ``== pivot`` / ``> pivot`` 三段。重复元素多的数据（如大量
   相同 key 的记录）不会被反复搬移，最坏情况显著改善。
3. **小数组插入排序**：子区间长度 <= ``INSERTION_THRESHOLD`` 时改用插入
   排序，减少递归与调用开销。
4. **尾递归消除**：每轮只对较短的一半递归，另一半用 while 循环继续，
   递归深度上界从 O(n) 降到 O(log n)。

注意：快排是**不稳定**排序，相等元素的相对顺序不保证保持。
需要稳定性时用 :func:`sort_algo.merge_sort.merge_sort`。
"""

from __future__ import annotations

from typing import List, MutableSequence, TypeVar

T = TypeVar("T")

# 子区间长度小于等于该阈值时改用插入排序
INSERTION_THRESHOLD = 16


def quick_sort(seq: MutableSequence[T], *, in_place: bool = True) -> List[T]:
    """对序列做快速排序。

    :param seq: 待排序序列。``in_place=True`` 时应传入可变序列（list）。
    :param in_place: ``True`` 原地修改 ``seq``；``False`` 时不动入参。
    :return: 排序后的列表快照（``in_place=True`` 时内容与 ``seq`` 一致）。
    :raises TypeError: 元素之间不可比较时，由 Python 的比较运算抛出。

    >>> quick_sort([3, 1, 2])
    [1, 2, 3]
    >>> quick_sort([])
    []
    >>> data = [5, 2, 9, 2, 8]
    >>> quick_sort(data)          # 原地排序
    [2, 2, 5, 8, 9]
    >>> data
    [2, 2, 5, 8, 9]
    >>> quick_sort([3, 1, 2], in_place=False)
    [1, 2, 3]
    """
    target: MutableSequence[T] = seq if in_place else list(seq)
    if len(target) > 1:
        _quick_sort(target, 0, len(target) - 1)
    return list(target)


def _quick_sort(a: MutableSequence[T], lo: int, hi: int) -> None:
    """对闭区间 ``a[lo..hi]`` 排序。"""
    while lo < hi:
        if hi - lo + 1 <= INSERTION_THRESHOLD:
            _insertion_sort(a, lo, hi)
            return

        lt, gt = _partition_three_way(a, lo, hi)

        # 只递归较短的一侧，较长的一侧继续循环 => 递归深度 O(log n)
        if lt - lo < hi - gt:
            _quick_sort(a, lo, lt - 1)
            lo = gt + 1
        else:
            _quick_sort(a, gt + 1, hi)
            hi = lt - 1


def _partition_three_way(a: MutableSequence[T], lo: int, hi: int) -> tuple[int, int]:
    """三路切分，返回相等段的闭区间边界 ``(lt, gt)``。

    完成后满足：

    - ``a[lo..lt-1] <  pivot``
    - ``a[lt..gt]  == pivot``
    - ``a[gt+1..hi] >  pivot``
    """
    pivot = a[(lo + hi) // 2]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        cur = a[i]
        if cur < pivot:  # type: ignore[operator]
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif cur > pivot:  # type: ignore[operator]
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def _insertion_sort(a: MutableSequence[T], lo: int, hi: int) -> None:
    """对闭区间 ``a[lo..hi]`` 做插入排序。"""
    for i in range(lo + 1, hi + 1):
        cur = a[i]
        j = i - 1
        while j >= lo and a[j] > cur:  # type: ignore[operator]
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur


if __name__ == "__main__":
    import random

    data = [random.randint(-100, 100) for _ in range(20)]
    print("before:", data)
    print("after :", quick_sort(data))
