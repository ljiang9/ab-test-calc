# ab-test-calc

零依赖的 **A/B 显著性计算器**：输入两组的转化数与样本量，做两比例 **z 检验**，给出 p 值、差值 95% 置信区间、相对提升，以及是否显著的中文结论。纯标准库（用 `math.erf` 算正态 CDF），无需任何 API。

## 功能简介

- **两比例 z 检验**（合并比例标准误）。
- 双侧 **p 值**（< 0.05 判显著）。
- 转化率差的 **95% 置信区间**（百分点 pp）。
- 自动计算相对提升（lift）并给中文结论。

## 快速开始

```bash
python3 cli.py --a-conv 48 --a-n 1000 --b-conv 60 --b-n 1000
```

输出示例：

```
A 组转化率：4.80%  (48/1000)
B 组转化率：6.00%  (60/1000)
z = 1.211
p 值（双侧）= 0.2259
差值 95% CI = [-0.78pp, 3.18pp]
结论：不显著（p=0.2259 ≥ 0.05），当前数据不足以判断两组有真实差异。
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地统计计算。

## 目录说明

```
ab-test-calc/
├── ab_test.py   # two_proportion_ztest / interpret
├── cli.py    # 命令行入口
├── tests/
│   └── test_ab.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
