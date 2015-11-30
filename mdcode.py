#!/usr/bin/env python3

import sys

def extract(filename):
    incode = False
    count = 1
    with open(filename) as mdfile, open(filename + ".code", 'w') as codefile:
        for l in mdfile:
            if l.find("```") > -1:
                incode = not incode
                if incode: 
                    codefile.write("### Block {} ###\n".format(count))
                    count += 1
                else: codefile.write("\n")
            elif incode:
                codefile.write(l)
                

if __name__ == "__main__":
     success = [extract(f) for f in sys.argv]
     print("Extracted code for all markdownfiles into file.md.code.")
