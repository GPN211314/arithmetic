# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:04:49 2019

@author: 陈加珂
"""
import random
import operator
import math

class Tree_node:
    def __init__(self, ch):
        self.ch = ch
        self.lchild = None
        self.rchild = None

class Generate:
    max_operator_number = 10 #除括号外的运算符的个数最多为10
    arithmetic_number = 1000 #运算式的个数为1000
    operator_list = ['+', '-', '*', '/', '(', ')']
    operator_list_length = 7 #运算符一共7个（包括乘方）
    max_number = 100 #数字最大为100，即100以内运算    
    priority = {'+': 1,'-': 1,'*': 2,'/': 2,'^': 3}# 运算符优先
    max_result = 10000 #计算结果的上限为10000，防止出现数字过大难以计算
    min_result = -10000 #计算结果的下限为10000
    min_presentation_set = set()
    
    def __init__(self, power_symbol):
        if(power_symbol == "**"):
            Generate.operator_list.append("**")
        else:
            Generate.operator_list.append('^')
    
    def generate_arithmetic(self):        
        
        ari_num = 0
        while ari_num < Generate.arithmetic_number :
            operator_number = random.randint(1, Generate.max_operator_number) #除括号外的运算符的个数在1到10之间
            arithmetic = "" #运算式
            brackets_number = 0 #没匹配的左括号的数量
            
            #运算式的开始可以是若干个连续的左括号           
            while(4 == random.randint(0, Generate.operator_list_length - 1)):
                arithmetic += '('
                brackets_number += 1
            
            #添加第一个数
            arithmetic += str(random.randint(0, Generate.max_number))            
            
            ope_num = 0
            while ope_num < operator_number :
                operator = Generate.operator_list[random.randint(0, Generate.operator_list_length - 1)]
                               
                if operator == '(' : #如果是左括号(
                    #数字不能紧挨着左括号，所以重新选择
                    continue
                elif operator == ')': #如果是右括号)
                    #如果有还没有配对的左括号，可以加上右括号
                    if brackets_number > 0 :
                        add_rightbracket = True
                        
                        #首先判断数字左边是不是左括号
                        index = -1
                        while arithmetic[index] >= '1' and arithmetic[index] <= '9':
                            index -= 1
                            if(arithmetic[index] == '('):
                                #如果数字左边是左括号，直接加上右括号没有意义
                                add_rightbracket = False
                        
                        #数字左侧不是左括号
                        if add_rightbracket ==True:                            
                            arithmetic += ')'
                            brackets_number -= 1
                        
                        #无论有没有加上右括号，后面都需要加上一个运算符                        
                        operator = Generate.operator_list[random.randint(0, Generate.operator_list_length - 1)]
                        #运算符不能是左括号，否则不符合运算式的规则
                        #也不能是右括号 1.两个连续的右括号没有意义 2.本身就不能加上右括号
                        while operator == '(' or operator == ')':
                            operator = Generate.operator_list[random.randint(0, Generate.operator_list_length - 1)]
                        arithmetic += operator
                        
                        while(4 == random.randint(0, Generate.operator_list_length - 1)):
                            arithmetic += '('
                            brackets_number += 1
                    #如果没有需要配对的左括号，就重新选择
                    elif brackets_number == 0:
                        continue
                else:
                    arithmetic += operator
                    #可能会有若干个连续的左括号
                    while(4 == random.randint(0, Generate.operator_list_length - 1)):
                        arithmetic += '('
                        brackets_number += 1
                
                ope_num += 1
                arithmetic += str(random.randint(0, Generate.max_number))
            
            while brackets_number > 0:
                arithmetic += ')'
                brackets_number -= 1
            
            postfix_arithmetic = self.infix2postfix(arithmetic)
            result = self.calculate(postfix_arithmetic)
                        
            #如果运算式出现错误或过大，就重新生成
            if result == False :
                continue
                        
            result = self.postfix2tree(postfix_arithmetic)
            if result == False:
                continue
            
            self.handle_brackets(postfix_arithmetic)
            print(arithmetic)
            ari_num += 1 
      
    #中缀表达式转后缀表达式    
    def infix2postfix(self, arithmetic):
        postfix_arithmetic = []
        stack = []
        
        index = 0
        while index < len(arithmetic):
            ch = arithmetic[index]
            if ch >= '0' and ch <= '9':#数字
                while index + 1 < len(arithmetic) and arithmetic[index + 1] >= '0' and arithmetic[index + 1] <= '9':
                    ch += arithmetic[index + 1]
                    index += 1
                postfix_arithmetic.append(ch)
            elif ch == '(':#左括号
                stack.append(ch)
            elif ch == ')':#右括号
                while len(stack) > 0:
                    operator = stack.pop()
                    if operator == '(':
                        break
                    else:
                        postfix_arithmetic.append(operator)
            else:#其他运算符
                while len(stack) >= 0:
                    if len(stack) == 0:
                        stack.append(ch)
                        break
                    operator = stack.pop()               
                    if operator == '(' or Generate.priority[ch] > Generate.priority[operator]:
                        stack.append(operator)
                        stack.append(ch)
                        break
                    else:
                        postfix_arithmetic.append(operator)
            index += 1
            
        while len(stack) > 0:
            postfix_arithmetic.append(stack.pop())
 
        return postfix_arithmetic

    #判断运算式中是否有错误，比如除0，底数为负指数为分数等情况
    #判断计算的结果是否过大，设置上限为10000
    #判断乘方是否出现指数过大的情况，设置一次乘方结果的上限也为10000
    #如果出现上述三种情况就返回false重新生成题目
    def calculate(self, postfix_arithmetic):
        stack = []
        for i in postfix_arithmetic:
            if i in "+-*/^":
                try:
                    n2 = stack.pop()
                    n1 = stack.pop()
                    if i == '+':
                        result = n1 + n2
                    elif i == '-':
                        result = n1 - n2
                    elif i == '*':
                        result = n1 * n2
                    elif i == '/':
                        result = n1 / n2
                    elif i == '^':             
                        #如果底数是0或1，指数不管是多少都可以进行乘方操作
                        if n1 == 0 or n1 == 1:
                            result = n1**n2
                        elif n2 < 14 and math.modf(n2)[0] == 0:
                            result = n1**n2
                        else:
                            return False
                except Exception : #所有运算上的错误
                    return False
                stack.append(result)
            else:
                stack.append(int(i))
        
        return stack[0] <= 10000 and stack[0] >= -10000
        
    def postfix2tree(self, postfix_arithmetic):        
        stack = []
        for ch in postfix_arithmetic:
            node = Tree_node(ch)
            if ch in "+-*/^":
                right = stack.pop()
                left = stack.pop()
                node.rchild = right
                node.lchild = left
                stack.append(node)
            else:
                stack.append(node)
        
        min_presentation_arithmetic = self.tree2min_presentation(stack[0])  

        if min_presentation_arithmetic in Generate.min_presentation_set:
            return False
        else:
            return True
               
    def tree2min_presentation(self, node):
        if node.lchild == None and node.rchild == None:
            return node.ch + ' '
        elif node.ch in "-/^":
            return node.ch + self.tree2min_presentation(node.lchild) + self.tree2min_presentation(node.rchild)
        else :
            lchild_result = self.tree2min_presentation(node.lchild)
            rchild_result = self.tree2min_presentation(node.rchild)
            if(operator.le(lchild_result, rchild_result)): #如果左子树的最小表示小于等于右子树的最小表示
                return node.ch + lchild_result + rchild_result
            else:
                return node.ch + rchild_result + lchild_result
        
                
                        
                    