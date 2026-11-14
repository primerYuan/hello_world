"""sort_algo 单元测试（仅用标准库 unittest，无需额外依赖）。

运行方式::

    python -m unittest discover -s tests -v
    # 或
    python -m unittest tests.test_sort -v
"""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sort_algo import merge_sort, quick_sort  # noqa: E402


def _random_cases(seed: int = 42, n_cases: int = 50):
    rng = random.Random(seed)
    for _ in range(n_cases):
        size = rng.randint(0, 200)
        yield [rng.randint(-1000, 1000) for _ in range(size)]


class QuickSortTest(unittest.TestCase):
    def test_against_builtin_random(self):
        for data in _random_cases():
            with self.subTest(size=len(data)):
                expected = sorted(data)
                self.assertEqual(quick_sort(list(data), in_place=False), expected)

    def test_in_place_mutates(self):
        data = [3, 1, 2]
        out = quick_sort(data)
        self.assertEqual(data, [1, 2, 3])
        self.assertEqual(out, [1, 2, 3])

    def test_not_in_place_keeps_input(self):
        data = [3, 1, 2]
        quick_sort(data, in_place=False)
        self.assertEqual(data, [3, 1, 2])

    def test_edge_cases(self):
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(quick_sort([1]), [1])
        self.assertEqual(quick_sort([2, 2, 2]), [2, 2, 2])

    def test_already_sorted(self):
        data = list(range(500))
        self.assertEqual(quick_sort(list(data), in_place=False), data)

    def test_reverse_sorted(self):
        data = list(range(500, 0, -1))
        self.assertEqual(quick_sort(list(data), in_place=False), sorted(data))

    def test_many_duplicates(self):
        # 三路切分的关键场景：大量重复值，不应退化
        data = [1, 2] * 5000 + [3] * 100
        self.assertEqual(quick_sort(list(data), in_place=False), sorted(data))

    def test_strings(self):
        data = ["pear", "apple", "banana"]
        self.assertEqual(quick_sort(list(data), in_place=False), sorted(data))

    def test_incomparable_raises(self):
        with self.assertRaises(TypeError):
            quick_sort([1, "a"], in_place=False)


class MergeSortTest(unittest.TestCase):
    def test_against_builtin_random(self):
        for data in _random_cases(seed=7):
            with self.subTest(size=len(data)):
                self.assertEqual(merge_sort(data), sorted(data))

    def test_does_not_mutate_input(self):
        data = [3, 1, 2]
        merge_sort(data)
        self.assertEqual(data, [3, 1, 2])

    def test_edge_cases(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([1]), [1])
        self.assertEqual(merge_sort([2, 2, 2]), [2, 2, 2])

    def test_already_sorted(self):
        data = list(range(500))
        self.assertEqual(merge_sort(data), data)

    def test_reverse_sorted(self):
        data = list(range(500, 0, -1))
        self.assertEqual(merge_sort(data), sorted(data))

    def test_reverse_flag(self):
        data = [3, 1, 2, 5, 4]
        self.assertEqual(merge_sort(data, reverse=True), [5, 4, 3, 2, 1])

    def test_key_function(self):
        data = ["bb", "a", "ccc", "dd"]
        self.assertEqual(merge_sort(data, key=len), ["a", "bb", "dd", "ccc"])

    def test_stability(self):
        # 相同 key 的元素必须保持原始相对顺序（快排不保证，归并要求保证）
        data = [(1, "a"), (0, "x"), (1, "b"), (0, "y"), (1, "c")]
        out = merge_sort(data, key=lambda t: t[0])
        self.assertEqual(out, [(0, "x"), (0, "y"), (1, "a"), (1, "b"), (1, "c")])

    def test_stability_reverse(self):
        data = [(1, "a"), (1, "b"), (0, "x"), (0, "y")]
        out = merge_sort(data, key=lambda t: t[0], reverse=True)
        self.assertEqual(out, [(1, "a"), (1, "b"), (0, "x"), (0, "y")])

    def test_incomparable_raises(self):
        with self.assertRaises(TypeError):
            merge_sort([1, "a"])


class CrossCheckTest(unittest.TestCase):
    def test_both_agree(self):
        for data in _random_cases(seed=2024, n_cases=20):
            with self.subTest(size=len(data)):
                self.assertEqual(
                    quick_sort(list(data), in_place=False),
                    merge_sort(data),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
