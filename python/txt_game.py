#!/usr/bin/python
import random
secret =random.randint(1,20)
print("========Hello, World!,重复猜测并给出数值大小范围，答案随机=======")
tmp = input("心里想的第一个数字：")
guess = int(tmp)
if guess > secret:
    print("数值大了")
else:
    print("数值小了")
while guess != secret:
    tmp = input("猜错咯，请重新输入：")
    guess = int(tmp)
    if guess == secret:
        print("厉害了，你是我肚子里的蛔虫么？")
    else:
        if guess > secret:
            print("数值大了")
        else:
            print("数值小了")
print("========end, World!,游戏结束=======")