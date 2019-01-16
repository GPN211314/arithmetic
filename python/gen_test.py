# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 17:17:57 2019

@author: 陈加珂
"""

import unittest
from unittest.mock import patch
import Generate

class TestGenerate(unittest.TestCase):
    
    #测试中缀表达式转后缀表达式
    def test_infix2postfix(self):
        arithmetic = "(11+12)*13/14^15"
        expected_postfix_arithmetic = ['11', '12', '+', '13', '*', '14', '15', '^', '/']
        gen = Generate.Generate("^")
        postfix_arithmetic = gen.infix2postfix(arithmetic)
        self.assertEqual(expected_postfix_arithmetic, postfix_arithmetic)
        
    #测试0^0，不合法算式的等价类
    def test_calculate1(self):
        arithmetic = "(1-1)^(2/2-1)"
        gen = Generate.Generate("^")
        postfix = gen.infix2postfix(arithmetic)
        self.assertEqual(gen.calculate(postfix), False)
    
    #测试底数为0或1的情况
    def test_calculate2(self):
        arithmetic = "1^(22*33/44+55)"
        gen = Generate.Generate("^")
        postfix = gen.infix2postfix(arithmetic)
        self.assertEqual(gen.calculate(postfix), True)
        
    #测试指数过大的情况   
    def test_calculate3(self):
        arithmetic = "2^14-10000"
        gen = Generate.Generate("^")
        postfix = gen.infix2postfix(arithmetic)
        self.assertEqual(gen.calculate(postfix), False)
        
    #测试乘方计算超过10000，但指数为-3—3的情况  
    def test_calculate4(self):
        arithmetic = "200^2-35000"
        gen = Generate.Generate("^")
        postfix = gen.infix2postfix(arithmetic)
        self.assertEqual(gen.calculate(postfix), True)
    
    #测试最后结果超过10000的情况    
    def test_calculate5(self):
        arithmetic = "1000*222"
        gen = Generate.Generate("^")
        postfix = gen.infix2postfix(arithmetic)
        self.assertEqual(gen.calculate(postfix), False)
    
    #判断3+(2+1)和1+2+3的最小表示是否相同（题中的例子）
    def test_tree2minpresentation1(self):
        arithmetic1 = "3+(2+1)"
        arithmetic2 = "1+2+3"
        gen = Generate.Generate("^")
        postfix1 = gen.infix2postfix(arithmetic1)
        postfix2 = gen.infix2postfix(arithmetic2)
        tree_root1 = gen.postfix2tree(postfix1)
        tree_root2 = gen.postfix2tree(postfix2)
        self.assertEqual(gen.tree2minpresentation_and_infix(tree_root1), gen.tree2minpresentation_and_infix(tree_root1))

    #判断3+(2+1)和1+2+3的最小表示是否相同（题中的例子）
    def test_tree2minpresentation2(self):
        arithmetic1 = "3+2+1"
        arithmetic2 = "1+2+3"
        gen = Generate.Generate("^")
        postfix1 = gen.infix2postfix(arithmetic1)
        postfix2 = gen.infix2postfix(arithmetic2)
        tree_root1 = gen.postfix2tree(postfix1)
        tree_root2 = gen.postfix2tree(postfix2)
        self.assertEqual(gen.tree2minpresentation_and_infix(tree_root1)[0] == gen.tree2minpresentation_and_infix(tree_root2)[0], False)
    
    #测试是否生成正确的中缀表达时
    def test_tree2infix(self):
        arithmetic = "(1+((2+(((3+4))))))"
        gen = Generate.Generate("^")
        postfix = gen.infix2postfix(arithmetic)
        tree_root = gen.postfix2tree(postfix)
        self.assertEqual(gen.tree2minpresentation_and_infix(tree_root)[1], "1+(2+(3+4))")

    #测试乘方符号
    def test_power_symbol(self):
        arithmetic = "((2^2)^2)^2"
        gen = Generate.Generate("**")
        postfix = gen.infix2postfix(arithmetic)
        tree_root = gen.postfix2tree(postfix)
        self.assertEqual(gen.tree2minpresentation_and_infix(tree_root)[1], "((2**2)**2)**2")

if __name__ == '__main__':
	unittest.main()