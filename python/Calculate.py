#!/usr/bin/env python3
# coding:utf-8

from fractions import Fraction
import sys

# 将**替换为^
def instead(expression):
    tmp_ls = expression.split("**")
    return "^".join(tmp_ls)


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

# 表达式计算
def exps_cal(exps_list):
    # 操作数栈与符号栈
    num_stack = []
    ops_stack = []
    for i in exps_list:
        if type(i) == int:
            num_stack.append(Fraction(i))
        else:
            SYA(i, num_stack, ops_stack)
    return num_stack.pop()


def calculate(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b
    if op == "^":
        return a ** b

# 将数字与符号分离
def separate(expression):
    exps_list = []
    for i in expression:
        if i.isdigit():
            exps_list[-1] = 10 * exps_list[-1] + int(i)
        elif i != " ":
            if len(exps_list) >= 2:
                if (i == "(" and not exps_list[-2].isdigit()) or \
                        (not i.isdigit() and exps_list[-2] == ")"):
                    exps_list[-1] = i
                    exps_list.append(0)
                else:
                    exps_list.append(i)
                    exps_list.append(0)
            else:
                exps_list.append(i)
                exps_list.append(0)
    exps_list.pop()
    return exps_list

# 判断对错并统计
def tof(standard_answer, count, right_count):
    answer = input()
    if answer == "":
        print("共完成{0}道，正确{1}道".format(count, right_count))
        sys.exit(0)
    elif Fraction(answer) == standard_answer:
        print("正确！")
        right_count += 1
    else:
        print("错误！")
    return count, right_count

def main():
    count = -1
    right_count = 0
    with open('question.txt') as qst:
        for line in qst:
            count += 1
            line = line.split('\n')[0]
            print(line, end='=')

            expression = "(" + line + ")"

            expression = instead(expression)

            exps_list = separate(expression)

            standard_answer = exps_cal(exps_list)
            count ,right_count = tof(standard_answer, count, right_count)
    print("共完成{0}道，正确{1}道".format(count + 1, right_count))

