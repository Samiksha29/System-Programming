#!/usr/bin/env python
import sys
from sys import argv
from subprocess import call

if __name__=="__main__":
    fname=sys.argv[1]
    object_name=sys.argv[2]

    if object_name=='-s':
        print("\n\t\t\t\t SYMBOL TABLE")
        call(["python3","symbol_table.py",fname])
        print('\n')
    
    if object_name=='-l':
        print("\n\t\t\t\t LITERAL TABLE")
        call(["python3","literal_table.py",fname])
        print('\n')

    if object_name=='-i':
        print("\n\t\t\t\t INTERMEDIATE CODE")
        call(["python3","intermediate.py",fname])
        print('\n')
    
    if object_name=='-lst':
        print("\n\t\t\t\t LST")
        call(["python3","lst.py",fname])
        print('\n')
     
    if object_name=='-a':
        print("\n\n\t\t\t\t SYMBOL TABLE")
        call(["python3","symbol_table.py",fname])
        print("\n\n\t\t\t\t LITERAL TABLE")
        call(["python3","literal_table.py",fname])
        print("\n\n\t\t\t\t INTERMEDIATE CODE")
        call(["python3","intermediate.py",fname])
        print("\n\n\t\t\t\t LST")
        call(["python3","lst.py",fname])
        print('\n')


     
