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
    operator_list = ['+', '-', '*', '/', '(', ')', '^']
    operator_list_length = 7 #运算符一共7个（包括乘方）
    max_number = 100 #数字最大为100，即100以内运算    
    priority = {'+': 1,'-': 1,'*': 2,'/': 2,'^': 3}# 运算符优先
    max_result = 10000 #计算结果的上限为10000，防止出现数字过大难以计算
    min_result = -10000 #计算结果的下限为10000
    min_presentation_set = set()
    power_symbol = '^' #表示乘方的符号
    
    def __init__(self, power_symbol):
        if(power_symbol == "**"):
            Generate.power_symbol = "**"
        self.question_file = open('question.txt', 'w')
    
    def generate_arithmetic(self):        
        
        ari_num = 0 #运算式的个数，共需要1000个
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
            
            ope_num = 0 #运算符的个数
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
                            #可以有若干个连续的右括号，但需要保证有未匹配的左括号
                            while brackets_number > 0 and 5 == random.randint(0, Generate.operator_list_length - 1):
                                arithmetic += ')'
                                brackets_number -= 1
                        
                        #无论有没有加上右括号，后面都需要加上一个运算符                        
                        operator = Generate.operator_list[random.randint(0, Generate.operator_list_length - 1)]
                        #运算符不能是左括号，否则不符合运算式的规则
                        #也不能是右括号，因为之前已经添加过了
                        while operator == '(' or operator == ')':
                            operator = Generate.operator_list[random.randint(0, Generate.operator_list_length - 1)]
                        arithmetic += operator
                        
                        while 4 == random.randint(0, Generate.operator_list_length - 1):
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
            
            #如果运算式出现错误或过大，就重新生成
            postfix_arithmetic = self.infix2postfix(arithmetic)
            result = self.calculate(postfix_arithmetic)                                    
            if result == False :
                continue
            
            #如果运算式重复，就重新生成            
            result, infix_arithmetic = self.postfix2tree(postfix_arithmetic)
            if result == False:
                continue
            
            self.question_file.write(infix_arithmetic + '\n')
            ari_num += 1 
            
        self.question_file.close()
      
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
    
    #将后缀表达式转化为树
    #再调用tree2minpresentation_and_infix将树转化为最小表示和中缀表达式
    #返回值为最小表示是否重复和中缀表达式
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
        
        min_presentation_arithmetic, infix_arithmetic = self.tree2minpresentation_and_infix(stack[0])  

        if min_presentation_arithmetic in Generate.min_presentation_set:
            return False, None
        else:
            return True, infix_arithmetic
    
    #返回的第一个参数是树的最小表示
    #返回的第二个参数是由树转换成的中缀表达式           
    def tree2minpresentation_and_infix(self, node):        
        if node.lchild == None and node.rchild == None:#叶节点
            return '\''+ node.ch + '\'', node.ch
        else:#非叶节点
            temp_min_left, temp_infix_left = self.tree2minpresentation_and_infix(node.lchild)
            temp_min_right, temp_infix_right = self.tree2minpresentation_and_infix(node.rchild)            
            temp_infix_left, temp_infix_right = self.add_brackets(temp_infix_left, temp_infix_right, node)
            
            if node.ch in "-/^":
                if node.ch == '^':
                    node.ch = Generate.power_symbol
                return node.ch + temp_min_left + temp_min_right, temp_infix_left + node.ch + temp_infix_right                    
            else : # node.ch in "+*"
                if(operator.le(temp_min_left,  temp_min_right)): #如果左子树的最小表示小于等于右子树的最小表示
                    return node.ch + temp_min_left + temp_min_right, temp_infix_left + node.ch + temp_infix_right 
                else:
                    return node.ch + temp_min_right + temp_min_left, temp_infix_left + node.ch + temp_infix_right 
    
    #为中缀表达式加上括号
    def add_brackets(self, infix_left, infix_right, node):
        #如果左子节点是运算符，且优先级小于当前节点，则给左子树的中缀表达式加括号
        if node.lchild.ch in "+-*/":
            if Generate.priority[node.lchild.ch] < Generate.priority[node.ch]:
                infix_left = '(' + infix_right + ')'
        #如果右子节点是运算符，且优先级小于等于当前节点，则给右子树的中缀表达式加括号
        if node.rchild.ch in "+-*/^":
            if Generate.priority[node.rchild.ch] <= Generate.priority[node.ch]:
                infix_right = '(' + infix_right + ')'
        return infix_left, infix_right
        
        
                
                        
                    
