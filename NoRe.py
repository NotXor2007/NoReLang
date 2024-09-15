import decprog
print("compiling and linking, please wait...")
if __name__ == "__main__":
    decprog.decode()
    try:
        decprog.asx64.assemble()
    except Exception:
        sys.exit(1)
    try:
        decprog.asx64.link()
        decprog.asx64.rem()
    except Exception:
        sys.exit(1)
