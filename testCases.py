import numpy as np
import os
import generator as gen


def cat(f,dbg=False):
    '''
    Performs a unix like cat on a file and removes the trailing newline
    debug option pretty prints the contents of the file
    '''
    ffile = open(f,'r')
    text = ffile.read()[:-1] # remove trailing newline from EOF
    if dbg:
        print("Program: ", f)
        print("==========")
        print(text)
        print("==========")
    return text


def runATest(f,dbg=False):
    '''
    Calls cat and then runs an expected Eidos type program.
    Calls 'run' in generator.py which in turn runs 'runProgram' in parser.py. 
    Debug option in run will call the yacc debug
    '''
    f_input = cat(f,dbg)
    gen.run(f_input,dbg=False)

def main():
    '''
    Main program. Hard code set the test directory for a set of Eidos programs
    that are located in a directory
    '''
    testDir = "../eidos-test/unit/no_error_expected/"
    testFiles = np.asarray(os.listdir(testDir))
    failed = 0
    for test in testFiles:
        try:
            runATest(testDir + test,dbg=True)
            print()
        except:
            failed += 1
            print("\nWARNING:")
            print("Could not run program: ",test)
            print()
    print("Test complete: ",failed,"/",len(testFiles)," failed")

if __name__ == '__main__':
    main()
