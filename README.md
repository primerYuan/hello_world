# hello_world

the 1st repository, used to get used to it.
//to test 'pull requests'.

---

## sort_algo —— Python 排序算法包

纯标准库实现，无第三方依赖（Python >= 3.9，用到 `from __future__ import annotations`）。

| 函数 | 实现 | 时间复杂度 | 额外空间 | 稳定 |
|---|---|---|---|---|
| `quick_sort` | 三路切分快排（原地） | 平均 O(n log n)，最坏 O(n²) | O(log n) 递归栈 | ❌ |
| `merge_sort` | 自顶向下归并 | 最坏 O(n log n) | O(n) | ✅ |

### 安装 / 引入

仓库根目录直接可用，无需打包安装：

```python
from sort_algo import quick_sort, merge_sort
```

### 用法

```python
from sort_algo import quick_sort, merge_sort

nums = [3, 1, 2]
quick_sort(nums)                  # 原地排序，返回 [1, 2, 3]
# nums == [1, 2, 3]

quick_sort([3, 1, 2], in_place=False)   # 不改入参，返回新列表 -> [1, 2, 3]

merge_sort([5, 2, 9, 2])          # -> [2, 2, 5, 9]
merge_sort([3, 1, 2], reverse=True)        # -> [3, 2, 1]
merge_sort(["bb", "a", "ccc"], key=len)    # -> ['a', 'bb', 'ccc']
```

### API

#### `quick_sort(seq, *, in_place=True) -> list`

- 三路切分（Dutch National Flag），大量重复元素时不退化
- pivot 取中间元素，已排序输入不会退化成 O(n²)
- 只对较短一侧递归，递归深度 O(log n)
- 小数组（<= 16）走插入排序
- **不稳定**：相等元素相对顺序不保证

#### `merge_sort(seq, *, key=None, reverse=False) -> list`

- **稳定**：相等 key 的元素保持原始相对顺序
- 两段已整体有序时短路跳过合并
- 辅助缓冲全程只分配一次
- 支持 `key` / `reverse`，语义同内置 `sorted`

### 测试

```bash
python -m unittest discover -s tests -v
```

20 个用例，覆盖随机数据、空/单元素、全等值、已排序、逆序、字符串、
`key`/`reverse`、稳定性，以及与内置 `sorted()` 的交叉验证。

### 目录结构

```
.
├── README.md
├── sort_algo/
│   ├── __init__.py
│   ├── quick_sort.py
│   └── merge_sort.py
└── tests/
    └── test_sort.py
```
