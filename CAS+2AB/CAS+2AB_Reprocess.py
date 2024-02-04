# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 13:04:51 2023

@author: Lenovo
"""
import os
import sys
while True:
    a = input("please input protocol:")
    script_path = os.path.abspath(sys.argv[0])
    folder_path = os.path.dirname(script_path)
    file_path = os.path.join(folder_path, a)
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            # 处理读取到的文件内容
    except FileNotFoundError:
        print("文件不存在")
    line_number = 0
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "not: defined;" in line:
            line_number = i + 1
            break
    if line_number > 1:
        del(lines[line_number-1])
        del(lines[line_number-2])
    text ='\n'.join(lines)
    print(text)
    
    # 询问用户是否继续
    answer = input("是否继续翻译？(y/n): ")

    # 根据用户输入判断是否继续循环
    if answer.lower() == "n":
        break
os.system("pause")



