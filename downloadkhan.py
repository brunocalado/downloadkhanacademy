#!/usr/bin/python3            
# -*- coding: UTF-8 -*-

import sys, os

useFileCourses = '(Off)'
useFileFormat = '(Off)'
msgtmp =''


for i in range(0, 5):
    opt = 0

    os.system('clear')
    print('Download Khan Academy')
    print('        1: Download All')
    print('        2: Use a file (mycourses) with selected courses ' + useFileCourses  )
    print('        3: Use a file (myformats) with the desired format ' + useFileFormat  )
    print('        4: Help')
    print('        0: Exit')
    msgtmp = 'Please choose your option typing the corresponding number:'
    opt = input(msgtmp)

    if opt=='1':
        print('All Videos will be downloaded')
    elif opt=='2':
        if useFileCourses == '(On)':
            useFileCourses = '(Off)'
        else: 
            useFileCourses = '(On)'
    elif opt=='3':
        if useFileFormat == '(On)':
            useFileFormat = '(Off)'
        else: 
            useFileFormat = '(On)'
    elif opt=='4':
        print('helping')

    elif opt=='0':
        sys.exit()


