#!/usr/bin/python3
import sc
import string
import sys
import asx64

#define minimum executable requirements
machine_lang_x64 = ['',"section .data\n","section .bss\n","section .text\n","global main\n","main:\n","push rbp\nmov rbp, rsp\n","sub rsp, 8\n","and rsp, 0xffffffffffffffff\n","mov rsp, rbp\npop rbp\n","ret\n"]
machine_lang_x64l = len(machine_lang_x64)
ins_entry = 10;
#for linux
cpu_regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
ret_reg = "rax"

def push_x64(string):
    global machine_lang_x64
    machine_lang_x64.insert(0,string)

def dumpfunction():
    for func in sc.funclst:
        with open("./func/{}.asm".format(func), "r", encoding = "utf-8") as file:
            data = file.readlines()
        for ins in range(len(data)-1,0,-1):
            push_x64(data[ins])

def dumpfunctioncall(line):
    global ins_entry
    func = str()
    for char in line:
        if char != "(":
            func += char
        else:
            break
    callfunc = "call " + func + "\n";
    args = line[len(func) : ].strip("(").rstrip(")").split(":") #extract args in a form of a list
    for arg in zip(args,cpu_regs):
        machine_lang_x64.insert(ins_entry, "mov {}, {}\n".format(arg[1],arg[0]))
        ins_entry += 1;

    if func in sc.funclst:
        machine_lang_x64.insert(ins_entry, callfunc)
        ins_entry +=1
    else:
        sys.stdout.write("compiler Crashed! ==> undefined function");sys.exit(-1)

def linestartswithchr(line): #checks wether the line starts with a letter
    for char in string.ascii_letters:
        if line.startswith(char): continue
        else: return False
    return True

def dumpglobalvars(gblist):
    ins = str()
    stroage, name, value = str(), str(), str()
    for allocation in gblist:
        for key in allocation:
            if key == "byte": storage = "db"
            elif key == "word": storage = "dw"
            elif key == "dword": storage = "dd"
            elif key == "qword": storage = "dq"
            elif not key[0].isnumeric(): name = key
            else: value = key
        ins = name + " " + storage + " " + value + "\n"
        machine_lang_x64.insert(2, ins)
        ins = str()
        

#decode NoRe instructions
def decode():
    global ins_entry;
    lines, global_vars = sc.scan()
    dumpglobalvars(global_vars)
    machine_lang_x64[0] = ";created with NoRe;\n"
    lswc = False #line starts with char
    isfuncc = False #is function call
    #print(sc.lowlevel, sc.vamd64_abi)
    dumpfunction()
    ins_entry += len(machine_lang_x64) - 1 - machine_lang_x64l
    for line in lines:
        if linestartswithchr(line): lswc = True;
        #resolve functions
        if "(" in line and line.endswith(")"):
            if sc.vamd64_abi:
                dumpfunctioncall(line)
            else:
                assert False, "only v amd64 abi calling convention works for now, please use it or wait for futur releases"
    file = open(sc.args[0] + ".asm", "w", encoding = "utf-8")
    file.writelines(machine_lang_x64)
    file.close() #write machine instructions

