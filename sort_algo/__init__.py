"""排序算法包 / Sorting algorithms package.

提供两种经典 O(n log n) 排序实现：

- :func:`sort_algo.quick_sort.quick_sort` —— 原地快速排序（in-place）
- :func:`sort_algo.merge_sort.merge_sort` —— 稳定归并排序（stable）

用法::

    from sort_algo import quick_sort, merge_sort

    nums = [3, 1, 2]
    quick_sort(nums)          # 原地排序 -> [1, 2, 3]
    assert merge_sort(nums) == [1, 2, 3]
"""

from .merge_sort import merge_sort
from .quick_sort import quick_sort

__all__ = ["quick_sort", "merge_sort"]
__version__ = "0.1.0"
