"""ab-test-calc：两比例 A/B 显著性检验。

纯标准库：
- 合并比例下的两比例 z 检验（two-proportion z-test）；
- p 值（双侧，用 math.erf 近似正态 CDF）；
- 两组转化率差的 95% 置信区间；
- 给出是否显著、方向与提升幅度的中文结论。
"""

from __future__ import annotations

import math


def _normal_cdf(z: float) -> float:
    """标准正态分布 CDF。"""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_proportion_ztest(conv_a: int, n_a: int,
                         conv_b: int, n_b: int) -> dict:
    """对 A、B 两组做两比例 z 检验。

    conv_* : 转化数；n_* : 样本量。
    """
    if n_a <= 0 or n_b <= 0:
        raise ValueError("样本量必须为正")
    if conv_a < 0 or conv_b < 0:
        raise ValueError("转化数不能为负")

    p_a = conv_a / n_a
    p_b = conv_b / n_b
    p_pool = (conv_a + conv_b) / (n_a + n_b)

    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se_pool if se_pool else 0.0
    p_value = 2 * (1 - _normal_cdf(abs(z)))

    # 差值的 95% CI（用非合并 SE）
    se_diff = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    diff = p_b - p_a
    ci_low = diff - 1.96 * se_diff
    ci_high = diff + 1.96 * se_diff

    lift = (p_b - p_a) / p_a if p_a else float("inf")

    significant = p_value < 0.05
    return {
        "rate_a": p_a,
        "rate_b": p_b,
        "z": z,
        "p_value": p_value,
        "diff": diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "lift": lift,
        "significant": significant,
    }


def interpret(result: dict) -> str:
    """生成中文结论。"""
    if result["significant"]:
        direction = "B 优于 A" if result["diff"] > 0 else "A 优于 B"
        return (f"显著（p={result['p_value']:.4f} < 0.05），"
                f"{direction}，相对提升约 {result['lift']*100:.1f}%。")
    return (f"不显著（p={result['p_value']:.4f} ≥ 0.05），"
            "当前数据不足以判断两组有真实差异。")
