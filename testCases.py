import numpy as np
import os
import generator as gen
import time
import signal # For timeouts

#testDir = "../eidos-test/unit/no_error_expected/"
testDir = "../eidos-test/sandbox/thunderHamsters/"
timeout = 5

def timeoutHandler(signum, frame):
    raise Exception("WARNING: Program has timed out")

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
    testFiles = np.asarray(os.listdir(testDir))
    nPass = 0
    notRun = 0
    failed = 0
    for test in testFiles:
        try:
            signal.signal(signal.SIGALRM, timeoutHandler)
            signal.alarm(timeout)
            runATest(testDir + test,dbg=True)
            print()
            nPass += 1
        except FileNotFoundError as e:
            print(e)
            notRun += 1
        except Exception as e:
            failed += 1
            print("WARNING: ",e)
            print("Could not run program: ",test)
            print()
            input()
    passRate = round(nPass/len(testFiles),3)*100
    print("Test complete: ",nPass,"/",len(testFiles),"passed (", passRate, "% pass )")
    print("Failed: ",failed)
    print("Files not found: ",notRun)

def singularProgram(testString):
    '''
    run a single program
    '''
    try:
        signal.signal(signal.SIGALRM, timeoutHandler)
        signal.alarm(timeout)
        gen.run(testString)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    #main()
    #singularProgram("x = 5.0:10.1;")
    #singularProgram("x = 5 + 10.2; y = (x*2)%2; z = (5 + 2/3 *7 + 6 -1)%7; a = 5:12;")
    #singularProgram("if (1==1) break; else x=2; x;")
    singularProgram("x = 5.0:10.1;")

