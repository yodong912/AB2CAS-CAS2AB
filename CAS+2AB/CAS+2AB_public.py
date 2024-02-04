
# -*- coding: utf-8 -*-
"""
CAS2AB_public_key

@author: Yodong
"""

import re
import os
import sys


def PreProcess(text):
    text = text.replace( "PKA'","sk(A)")
    text = text.replace( "PKB'","sk(B)")
    text = text.replace( "PKA","pk(A)")
    text = text.replace("PKB","pk(B)")
    identifiers_index = text.index("identifiers")
    text = text[:identifiers_index]+text[identifiers_index:].replace( "G","g()")
    return text

def ExtractNum(text):
    lines = text.split('\n')
    found = False
    line_number = 0
    for i, line in enumerate(lines):
        if ":number" in line:
            found = True
            line_number = i  # 行号从1开始计数
            break
    line_three = lines[line_number]
    values = line_three.split(":")[0]
    num = values.split(",")
    return num

def AdjustStructure(text):
    identifiers_index = text.index("identifiers")
    messages_index = text.index("messages")
    knowledge_index = text.index("knowledge")
    goal_index = text.index("goal")
    session_index = text.index("session")
    if knowledge_index < session_index:
        text = text[:identifiers_index]+text[knowledge_index:session_index]+text[messages_index:knowledge_index]+text[goal_index:]+"\nend"
    else:
        text = text[:identifiers_index] + "knowledge\n" +"not defined\n" +text[messages_index:session_index]+text[goal_index:]+"\nend"
    return text

def AdjustSym(text):
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        cleaned_line = re.sub(r"\d\.", "", line)
        cleaned_lines.append(cleaned_line.strip())
    text = "\n".join(cleaned_lines)
    messages_index = text.index("messages")
    goal_index = text.index("goal")
    text = text[:messages_index] + re.sub(r"\,", '.', text[messages_index:goal_index]) + text[goal_index:]
    return text

def AbActions(text,num):
    messages_index = text.index("messages")
    goal_index = text.index("goal")
    lines = text[messages_index:goal_index].split('\n')
    length1 = 0
    ac = 0
    t = 0
    for i, line in enumerate(lines):
        if ":" in line and length1 < len(num):
            parts = line.split(":")
            before_colon = parts[0]
            after_colon = parts[1]
            ac = ac + 1
            prefix1 = "[ac" + str(ac) + "] "
            if num[t] != '':
                prefix2 = "(" + num[t] + "):"
                lines[i] = prefix1 + before_colon + prefix2 + after_colon
            else:
                prefix2 =":"
                lines[i] = prefix1 + before_colon +  prefix2 + after_colon
            length1 = length1 + 1
            t = t+1
    modified = "\n".join(lines)
    text = text[:messages_index] + modified + text[goal_index:]
    messages_index = text.index("messages")
    goal_index = text.index("goal")        
    lines = text[messages_index:goal_index].split('\n')
    for i, line in enumerate(lines):
        if ("-" in line) and ("[ac" not in line):
            ac = ac + 1
            prefix1 = "[ac" + str(ac) + "] "
            lines[i] = prefix1 + lines[i]
    modified = "\n".join(lines)
    text = text[:messages_index] + modified + text[goal_index:]
    messages_index = text.index("messages")
    goal_index = text.index("goal")        
    lines = text[messages_index:goal_index].split('\n')
    for i, line in enumerate(lines):
        if "{" in line:
            parts = line.split("{")
            before_colon = parts[0]
            after_colon = parts[1]
            prefix1 = "aenc{"
            lines[i] = before_colon + prefix1 + after_colon
    modified = "\n".join(lines)
    text = text[:messages_index] + modified + text[goal_index:]
    return text

def AbGoals(text):
    goal_index = text.index("goal")
    end_index = text.index("end")
    lines = text[goal_index:end_index].split('\n')
    sec,auth,nauth = 0,0,0
    for i, line in enumerate(lines):
        if "secrecy" in line:
            sec = sec + 1
            prefix1 = "[secret" + str(sec) + "] "
            lines[i] = prefix1 + lines[i]
        if "non-" in line:
            nauth = nauth + 1
            prefix1 = "[authNonInj" + str(nauth) + "] "
            lines[i] = prefix1 + lines[i]
        if ("authenticates" in line) and ("non-" not in line):
            auth = auth + 1
            prefix1 = "[authInj" + str(auth) + "] "
            lines[i] = prefix1 + lines[i]
    modified = "\n".join(lines)
    text = text[:goal_index] + modified + text[end_index:]
    return text

def AdjustStructName(text):
    text = text.replace( "protocol","Protocol")
    text = text.replace( "knowledge","Knowledge")
    text = text.replace( "messages","Actions")
    text = text.replace( "goal","Goals")
    return text

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

    text = PreProcess(text)#预处理
    num = ExtractNum(text)#提取number
    text = AdjustStructure(text)#结构调整
    text = AdjustSym(text)#符号调整
    text = AbActions(text,num)#抽象actions
    text = AbGoals(text)#抽象goals
    text = AdjustStructName(text)

    print(text)
    # 询问用户是否继续
    answer = input("是否继续翻译？(y/n): ")

    # 根据用户输入判断是否继续循环
    if answer.lower() == "n":
        break

os.system("pause")