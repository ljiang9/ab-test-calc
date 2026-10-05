import unittest

from ab_test import interpret, two_proportion_ztest


class TestAB(unittest.TestCase):
    def test_known_example_significant(self):
        # 教科书已知算例：A=48/1000, B=60/1000
        r = two_proportion_ztest(48, 1000, 60, 1000)
        self.assertAlmostEqual(r["rate_a"], 0.048, places=3)
        self.assertAlmostEqual(r["rate_b"], 0.060, places=3)
        # z 约 1.21（经典例题）
        self.assertAlmostEqual(r["z"], 1.21, delta=0.1)

    def test_more_extreme_significant(self):
        # 差异更大、样本更大 -> 显著
        r = two_proportion_ztest(480, 10000, 600, 10000)
        self.assertTrue(r["significant"])
        self.assertLess(r["p_value"], 0.05)
        self.assertGreater(r["diff"], 0)

    def test_no_difference(self):
        # 完全相同 -> z=0, p=1
        r = two_proportion_ztest(50, 1000, 50, 1000)
        self.assertAlmostEqual(r["z"], 0.0, places=4)
        self.assertAlmostEqual(r["p_value"], 1.0, places=3)
        self.assertFalse(r["significant"])

    def test_ci_contains_diff(self):
        r = two_proportion_ztest(48, 1000, 60, 1000)
        self.assertLessEqual(r["ci_low"], r["diff"])
        self.assertLessEqual(r["diff"], r["ci_high"])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            two_proportion_ztest(5, 0, 5, 100)

    def test_interpret_significant(self):
        r = two_proportion_ztest(480, 10000, 600, 10000)
        msg = interpret(r)
        self.assertIn("显著", msg)

    def test_interpret_not_significant(self):
        r = two_proportion_ztest(48, 1000, 60, 1000)
        msg = interpret(r)
        self.assertIn("不显著", msg)


if __name__ == "__main__":
    unittest.main()
