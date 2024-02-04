# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 19:56:41 2023

@author: Lenovo
"""

import re
import os
import sys

def PreTreat(text):
    text = text.replace("pk(I)", "PKI")
    text = text.replace("pk(R)", "PKR")
    text = text.replace("pk(A)", "PKA")
    text = text.replace("pk(B)", "PKB")
    text = text.replace("sk(A)", "PKA'")
    text = text.replace("sk(B)", "PKB'")
    text = text.replace("g()", "G")
    text = text.replace("g()", "G")
    text = text.replace("'g'", "G")
    declarations_index = text.index("declarations")
    knowledge_index = text.index("knowledge")
    text = text[:declarations_index] + re.sub(r"g", 'G', text[declarations_index:knowledge_index]) + text[knowledge_index:]
    ga = re.compile(r'\_')
    protocol_index = text.index("protocol")
    declaration_index = text.index("declarations")
    text = text[:protocol_index] + ga.sub('', text[protocol_index:declaration_index]) + text[declaration_index:]
    return text

def ExtractKey(text):
    pk = [];
    pk = pk+[re.findall(r'PKR', text)]
    pk = pk+[re.findall(r'PKI', text)]
    pk = pk+[re.findall(r'PKA', text)]
    pk = pk+[re.findall(r'PKB', text)]
    return pk
    
            
def ExtractNumber(text):
    pattern2 = r'\((.*?)\)\s*:'
    match = re.findall(pattern2, text)
    match = [word.capitalize() for word in match]
    match2 = re.findall(pattern2, text)
    length2 = len(match)
    knowledge_index = text.index("knowledge")
    for i in range(0,length2):
        text = text[:knowledge_index] + re.sub(match2[i],match[i],text[knowledge_index:])
    lines = text.split('\n')
    #观察是否有G
    found = False
    line_number = 0
    for i, line in enumerate(lines):
        if "G" in line:
            found = True
            line_number = i + 1  # 行号从1开始计数
            break
    if line_number != 0:
        match = match + ["G"]
    return match,text

def ExtractUser(text):
    pattern = r'(\w+)\s*:'
    knowledge = re.findall(pattern, text)
    knowledge = list(set(knowledge))
    return knowledge

def AbIdentifiers(text):
    identifier = "identifiers\nA,B:user;\n"
    flag2 = 0
    flag3 = 0
    length2 = len(match)
    for i in range(0,length2):
        identifier = identifier + str(match[i])
        if i != length2-1:
            identifier = identifier + ","
    if match != []:
        identifier = identifier + ":number;\n"
    for i in range(0,length1):
        if pk[i] != []:
            identifier = identifier + str(pk[i][0])
            flag2 = flag2+1
            if flag2 != flag1:
                identifier = identifier + ","

    if (pk[0]!=[] or pk[1]!=[] or pk[2]!=[] or pk[3]!=[]):
        identifier = identifier + ":public_key;\n"
    else:
        identifier = identifier
    return identifier

def AbSession(text,length2):
    chac = 0;
    session = "session_instances\n [A:a,B:b,"
    for i in range(0,length2):
        session = session + str(match[i]) + ":" + zmb[chac]
        chac = chac+1
        if i != length2-1:
            session = session + ","
    if pk!= [[],[],[],[]]:
        session = session + ","
    flag2 = 0;
    for i in range(0,length1):
        if pk[i] != []:
            session = session + str(pk[i][0]) + ":" + zmb[chac]
            chac = chac + 1
            flag2 = flag2+1
            if flag2 != flag1:
                session = session + ","
    session = session + "];"
    return session,chac

def AbIntruder(text):
    intruder = "intruder_knowledge\n a,b,"
    for i in range(0,chac):
        intruder = intruder + zmb[i]
        if i != chac-1:
            intruder = intruder + ","
    intruder = intruder + ";"
    return intruder

def Rewrite(text):
    protocol_index = text.index("protocol")# 找到 "Protocol;" 和 "declarations" 的索引位置
    declarations_index = text.index("declarations")
    text = text[:declarations_index] + "\n" + identifier + "\n" + text[declarations_index:]# 写入indentifier
    goal_index = text.index("goal")#调序
    messages_index = text.index("messages")
    knowledge_index = text.index("knowledge")
    text = text[:knowledge_index] + text[messages_index:goal_index] + text[knowledge_index:messages_index] + text[goal_index:]
    goal_index = text.index("goal")#写入session_knowledge
    text = text[:goal_index] + "\n" + session + "\n\n" + intruder + "\n\n" + text[goal_index:]#写入intruder_knowledge
    return text

def ReProcess(text):
    identifiers_index = text.index("identifiers")
    arrow_pos = text.find("->")
    flag = 0
    if arrow_pos != -1:
        flag = 1
    left_char = text[arrow_pos-2]
    right_char = text[arrow_pos+3]
    if flag == 1:
        if (left_char != right_char):
            text = text[:identifiers_index] + re.sub(left_char,"A",text[identifiers_index:])
            text = text[:identifiers_index] + re.sub(right_char,"B",text[identifiers_index:])
        else:
            text = re.sub(left_char,"A",text)
    goal_index = text.index("goal")#去掉不符合CAS+语言规范的括号
    text = re.sub(r'\([^()]*\) :', ':', text[:goal_index]) + text[goal_index:]

    text = re.sub(r"'.*?'.", '', text)#重新调整messages语句
    messages_index = text.index("messages")
    knowledge_index = text.index("knowledge")
    text = text[:messages_index] + re.sub(r"\.", ',', text[messages_index:knowledge_index]) + text[knowledge_index:]
    text = text.replace(r"aenc", '')
    text = text.replace(r"senc", '')
    declarations_index = text.index("declarations")
    messages_index = text.index("messages")
    text = text[:declarations_index] + text[messages_index:]
    text = re.sub(r"\,  ", '.', text)
    lines = text.split('\n')#去掉不必要的声明
    found = False
    line_number = 0

    for i, line in enumerate(lines):
        if "None"in line or "none" in line:
            found = True
            line_number = i + 1  # 行号从1开始计数
            break
    if line_number > 1:
        del(lines[line_number-1])
        del(lines[line_number-2])
    text ='\n'.join(lines)
    pattern_sec = re.compile(r'secrecy', re.IGNORECASE)
    pattern_senc = re.compile(r'senc', re.IGNORECASE)
    pattern_aenc = re.compile(r'aenc', re.IGNORECASE)
    pattern_nin = re.compile(r'non-injectively authenticates', re.IGNORECASE)
    pattern_in = re.compile(r'injectively authenticates', re.IGNORECASE)
    pattern_on = re.compile(r'on', re.IGNORECASE)
    pattern_au = re.compile(r'authenticity', re.IGNORECASE)
    # 将匹配到的内容替换为全小写形式
    text = pattern_sec.sub('secrecy', text)
    text = pattern_senc.sub('senc', text)
    text = pattern_aenc.sub('aenc', text)
    text = pattern_nin.sub('non-injectively authenticates', text)
    text = pattern_in.sub('injectively authenticates', text)
    text = pattern_on.sub('on', text)
    text = pattern_au.sub('Authenticity', text)
    
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
    zmb = ["c","d","e","f","g","h","i","j","k","l","m","n","o","p","q"]
    # python预处理
    text = PreTreat(text)

    #提取公钥
    pk = ExtractKey(text)
    flag1 = 0;
    length1 = len(pk)
    for i in range(0,length1):#得到pk长度
        if pk[i] != []:
            flag1 = flag1+1

    #提取number并将number转换成CAS+描述的形式
    match,text = ExtractNumber(text)


    #提取user
    knowledge = ExtractUser(text)

    pattern_know = re.compile(r'knowledge', re.IGNORECASE)
    text = pattern_know.sub('knowledge', text)

    #抽象identifier
    identifier = AbIdentifiers(text)


    #抽象session_knowledge
    length2 = len(match)
    [session,chac] = AbSession(text,length2)

    #抽象intruder
    intruder = AbIntruder(text)

    #重写并调整顺序
    text = Rewrite(text)

    #协议语言三次处理
    text = ReProcess(text)

    print(text)
    # 询问用户是否继续
    answer = input("是否继续翻译？(y/n): ")

    # 根据用户输入判断是否继续循环
    if answer.lower() == "n":
        break

os.system("pause")


