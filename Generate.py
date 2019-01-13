import random

class Generate:
    max_operator_number = 10 #除括号外的运算符的个数最多为10
    arithmetic_number = 1000 #运算式的个数为1000
    operator_list = ['+', '-', '*', '/', '(', ')']
    operator_list_length = 7 #运算符一共7个（包括乘方）
    max_number = 100 #数字最大为100，即100以内运算    
    
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
            
            print(arithmetic)
            ari_num += 1 
                          