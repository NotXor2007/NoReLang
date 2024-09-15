import sc
import subprocess
import os

x64 = sc.args[0] + ".asm"
commandasm = ["nasm", "-f", "elf64", "-o", x64[ : -4]+".o", x64]
commandlink = ["gcc", "-o", x64[ : -4], x64[ : -4]+".o"]
def assemble():
    subprocess.run(commandasm)

def link():
    subprocess.run(commandlink)

def rem():
    os.remove(sc.args[0] + ".asm")
    os.remove(sc.args[0] + ".o")
