#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import dka_common

addressList = []

fileName = 'index.html'
courseName = ''
resultForFileList = []

if __name__ == "__main__":

    tmp = dka_common.returnFile( fileName )
    
    courseName = dka_common.recoverLinesFromFile( 'All videos', 0, fileName, 2 )[1].split('<')[1].split('>')[1]
    fileHandle = open(courseName, "w")
    for i in tmp:
        if '<option' in i:
            result = [ i.split('<')[1].split('>')[0].split('\"')[1], i.split('<')[1].split('>')[1] ]
            addressList.append( result )
            fileHandle.writelines( str(result[1]) + '<>' + str( str(result[0]) + '\n' ) )

    fileHandle.close()


