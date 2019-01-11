#!/usr/bin/env python3
# coding:utf-8

from fractions import Fraction

# 定义优先级
def precedence(x):
    if x == "+":
        return 2
    if x == "-":
        return 2
    if x == "*":
        return 3 
    if x == "/":
        return 3
    if x == "^":
        return 4
    if x == "(":
        return 1
    if x == ")":
        return 1

# 调度场算法
def SYA(i, num_stack, ops_stack):                    
    if i == "(":
        ops_stack.append(i)
    elif i == ")" and ops_stack[-1] == "(":
        ops_stack.pop()
    elif precedence(i) <= precedence(ops_stack[-1]) and (i != "^" or ops_stack[-1] != "^"):
        b = num_stack.pop()
        a = num_stack.pop()
        op = ops_stack.pop()
        tmp = calculate(a, b, op)
        num_stack.append(tmp)
        SYA(i, num_stack, ops_stack)
    else:
        ops_stack.append(i)

def calculate(a, b, op):
    if op == "+":
        return a+b
    if op == "-":
        return a-b
    if op == "*":
        return a*b
    if op == "/":
        return a/b
    if op == "^":
        return a**b

def main():
    with open('question.txt') as qst:
        for line in qst:
            line = line.split('\n')[0]
            print(line, end='=')
        
            expression = "(" + line + ")"

            exps_list = []

            # 将数字与符号分离
            for i in expression:
                if i.isdigit():
                    exps_list[-1] = 10*exps_list[-1] + int(i)
                else:
                    exps_list.append(i)
                    exps_list.append(0)
            exps_list.pop()

            # 操作数栈与符号栈
            num_stack = []
            ops_stack = []

            for i in exps_list:
                if type(i) == int:
                    num_stack.append(Fraction(i))
                else:
                    SYA(i, num_stack, ops_stack)                    

            standard_answer = num_stack.pop()
            answer = input()
            if Fraction(answer) == standard_answer:
                print("正确！")
            else:
                print("错误！")

if __name__ == '__main__':
    main()
