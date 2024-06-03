DEBUG = True

def show(*arguments, seperator=" ", eol="\n"):
    if DEBUG:
        for arg in arguments:
            print(arg, sep=seperator, end="")
        print(end=eol)
