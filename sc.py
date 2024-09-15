#!/usr/bin/python3
import prs
#<>
args = prs.parse() #returns output and input files in a form of a list
#define constants
lowlevel = False
vamd64_abi = False
funclst = list()

def fetch_directs(codearray, strdirect, enddirect):
    cmddirectlst = list()
    buffer = ""
    for direct in range(strdirect, enddirect+1):
        directarray = codearray[direct]
        if directarray == "enddirective": return cmddirectlst
        elif directarray == "begindirective": continue
        else:
            if directarray.startswith("{"): buffer += directarray + " "
            elif directarray.endswith("}"): cmddirectlst.append(buffer + directarray);buffer = ""
            else: buffer += directarray + " "

def get_cmd(cld):
    if cld.startswith("include"): return 0;
    elif cld.startswith("using"): return 1;
    elif cld.startswith("dump"): return 2;

def action_cmd(cmd, cld):
    global lowlevel
    global vamd64_abi
    global funcstr
    match cmd:
        case 0:
            if cld[8 : ] == "lowlevel": lowlevel = True
            if cld[8 : ] == "vamd64_abi": vamd64_abi = True
        case 1:
            pass #TODO
        case 2:
            funclst.append(cld[5 : ])

def Directive(codearray, strdirect, enddirect):
    directs = fetch_directs(codearray, strdirect, enddirect) 
    for direct in directs:
        cld = direct.removeprefix("{").removesuffix("}")
        cmd = get_cmd(cld)
        action_cmd(cmd, cld)

def fetch_prog(codearray, strprog, endprog):
    cmdproglst = list()
    buffer = ""
    for prog in range(strprog, endprog+1):
        progarray = codearray[prog]
        if progarray == "endprogram": return cmdproglst
        elif progarray == "beginprogram": continue
        else:
            if progarray.startswith("{") and progarray.endswith("}"): cmdproglst.append(progarray)
            elif progarray.endswith("}"): cmdproglst.append(buffer + progarray);buffer = ""
            elif progarray.startswith("{"): buffer += progarray + " "
            else: buffer += progarray + " "

def corrector(pld):
    ignorestr,ignoreend = False, False
    for p in pld:
        if ignorestr:
            pld[pld.index(p) - 1] += p
            pld.remove(p)
        if "(" in p: ignorestr = True;ignoreed = False;
        if ")" in p: ignorestr = False;ignoreend = True;

def get_prog(pld, ligns):
    pld = pld.split(",")
    corrector(pld)
    mx = int(pld[-1]) + 1
    r = mx - len(ligns)
    if r > 0:
        for i in range(r):  ligns.append("")
    for item in pld[1:len(pld)]:    ligns[int(item)] = pld[0]

def action_prog(cmd, cld):
    match cmd:
        case 0:
            if cld[8 : ] == "lowlevel": lowlevel = True
        case 1:
            pass #TODO


def Program(codearray, strprog, endprog):
    lines = list()
    progs = fetch_prog(codearray, strprog, endprog)
    for prog in progs:
        pld = prog.removeprefix("{").removesuffix("}")
        pmd = get_prog(pld, lines)
    return lines

def fetch_global(codearray, strglobal, endglobal) -> list:
    strins, endins, compact = False, False, False
    ins = str()
    ins_array = list()
    for s in codearray[strglobal+1 : endglobal]:
        if s.startswith("{") and not s.endswith("}"): strins = True;endins = False;
        elif s.endswith("}") and not s.startswith("{"): strins = False;endins = True;
        elif s.startswith("{") and s.endswith("}"): ins_array.append(ins);
        if strins and not endins: ins += s
        elif not strins and endins: ins += s;ins_array.append(ins);ins = "";endins = False;
    for i in range(len(ins_array)):
        ins_array[i] = ins_array[i].removeprefix("{").removesuffix("}")
    return ins_array

def decode_global(global_list):
    gblist = global_list.copy()
    ins_list = list()
    for ins in gblist:
        if ins.startswith("byte"):
            ins_list.append("byte")
            ins_list.append(ins[4 : ins.find("<-")])
            ins_list.append(ins[ins.find("<-") + 2 : ])
        elif ins.startswith("word"):
            ins_list.append("word")
            ins_list.append(ins[4 : ins.find("<-")])
            ins_list.append(ins[ins.find("<-") + 2 : ])
        elif ins.startswith("dword"):
            ins_list.append("dword")
            ins_list.append(ins[5 : ins.find("<-")])
            ins_list.append(ins[ins.find("<-") + 2 : ])
        elif ins.startswith("qword"):
            ins_list.append("qword")
            ins_list.append(isn[5 : ins.find("<-")])
            ins_list.append(ins[ins.find("<-") : ])
        gblist[gblist.index(ins)] = ins_list.copy()
        ins_list.clear()
    return gblist

def Global(codearray, strglobal, endglobal):
    global_list = fetch_global(codearray, strglobal, endglobal) #list of global vars
    return decode_global(global_list)

#this function must be called
def scan():
    codearray = None
    comment = False
    begin,strdirective,strprog,strglobal = False, 0, 0, 0
    end,enddirective,endprog,endglobal = False, 0, 0, 0
    directives = list()
    global_vars,program = None, None
    with open(args[1], "r") as code: #read input files to get instructions
        codearray = code.read().split()

    for code in codearray:
        codearray[codearray.index(code)] = code.lower() #eradicate differences between lower case & upper case
    #search for flags in the input file
    for code in codearray.copy():
        if code == "begindirective": begin = True;end = False
        elif code == "enddirective": begin = False;end = True
        elif code == "beginglobal": begin = True;end = False
        elif code == "endglobal":begin = False;end = True
        elif code == "beginprogram": begin = True;end = False
        elif code == "endprogram": begin = False;end = True

        if begin == True and end == False and code == "begindirective":
            strdirective = codearray.index(code)
        elif end == True and begin == False and code == "enddirective":
            enddirective = codearray.index(code)
            Directive(codearray, strdirective, enddirective)
            being = False;end = False;

        elif begin == True and end == False and code == "beginglobal":
            strglobal = codearray.index(code)
        elif end == True and begin == False and code == "endglobal":
            endglobal = codearray.index(code)
            global_vars = Global(codearray, strglobal, endglobal)

        elif begin == True and end == False and code == "beginprogram":
            strprog = codearray.index(code)
        elif end == True and begin == False and code == "endprogram":
            endprog = codearray.index(code)
            program =  Program(codearray, strprog, endprog) #return
            being = False;end = False
	#get rid of comments in input file 
        if code.startswith(";"): comment = True #mark the start of the comment
        if comment:
            codearray.remove(code)
        if code.endswith(";"): comment = False #mark it's end
    return program,global_vars

#Entry Point
if __name__ == "__main__":
    scan()
