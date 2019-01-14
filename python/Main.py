import sys
import Generate
import Calculate

def help():
    print("-c  根据提示选择乘方符号，生成1000道不重复的四则运算题目\n"
            "-s  用户输入结果，判断对错，输入为空时退出并给出统计结果\n-h  显示当前信息")


def main(argv):
    if len(argv) != 2:
        help()
    else:
        if argv[1] == "-c":
            while True:
                powers = input("请输入乘方符号（**或^）：")
                if powers == "**" or powers == "^":
                    break
                else:
                    print("输入无效！！！")
            ob = Generate.Generate(powers)
            ob.generate_arithmetic()
        elif argv[1] == "-s":
            Calculate.main()
        else:
            help()
            

if __name__ == '__main__':
    main(sys.argv)
