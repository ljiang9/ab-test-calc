"""ab-test-calc 命令行入口。

用法示例：
    python3 cli.py --a-conv 48 --a-n 1000 --b-conv 60 --b-n 1000
"""

from __future__ import annotations

import argparse
import sys

from ab_test import interpret, two_proportion_ztest


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ab-test-calc",
        description="两比例 A/B 显著性检验（z 检验 + 置信区间）",
    )
    p.add_argument("--a-conv", type=int, required=True, help="A 组转化数")
    p.add_argument("--a-n", type=int, required=True, help="A 组样本量")
    p.add_argument("--b-conv", type=int, required=True, help="B 组转化数")
    p.add_argument("--b-n", type=int, required=True, help="B 组样本量")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    r = two_proportion_ztest(args.a_conv, args.a_n, args.b_conv, args.b_n)
    print(f"A 组转化率：{r['rate_a']*100:.2f}%  "
          f"({args.a_conv}/{args.a_n})")
    print(f"B 组转化率：{r['rate_b']*100:.2f}%  "
          f"({args.b_conv}/{args.b_n})")
    print(f"z = {r['z']:.3f}")
    print(f"p 值（双侧）= {r['p_value']:.4f}")
    print(f"差值 95% CI = [{r['ci_low']*100:.2f}pp, "
          f"{r['ci_high']*100:.2f}pp]")
    print(f"结论：{interpret(r)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
