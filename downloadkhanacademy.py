#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------
# Libraries
# ------------------------------------------------------------
import os
import sys


# ------------------------------------------------------------
# Variables and Constants
# ------------------------------------------------------------
addressList = []

wget = 'wget -c --quiet --output-document'
getflash = 'get_flash_videos --quiet --quality 240p --filename'
youtube = "http://www.youtube.com/watch?v="


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------
def returnFile(fileName): 
	""" 
		Retorna o arquivo selecionado por fileName 
	""" 
	fileHandle = open(fileName, "r") 
	lines = (fileHandle.read()).splitlines() 
	fileHandle.close() 
	return lines 


def download():

    # Get file with all class from a course
    fileindex = returnFile('index')
    for line in fileindex:
        courseIndexFile = line.split('<>')[0]
        courseDirName = line.split('<>')[1] 
        courseFileName  = '.' + courseDirName 

        print( '\n\nGetting ' + courseFileName + ' <---------------------------------------------------')
        courseFileName = courseFileName.replace(' ','_').lower()

        tmp = wget + ' ' + courseFileName + ' ' + courseIndexFile
        print(tmp)
        os.system(tmp)
        
        # Create a list with all links from a course
        for i in returnFile( courseFileName ):
            if '<option ' in i:
                result = [ i.split('<')[1].split('>')[0].split('\"')[1], i.split('<')[1].split('>')[1] ]
                addressList.append( str( str(result[0]) ) + '<>'  + str(result[1]) )

        # Clean
        print('\n\nRemoving useless files')
        os.system( 'rm -f ' + courseFileName )

        # Download the files naming them
        tmp = 'mkdir -p ' + courseDirName
        print(tmp)
        os.system(tmp)
        
        counter = 0
        for i in addressList:
            address = i.split('<>')[0]
            classroom = ' "' + str(counter).zfill(3) + '_' + i.split('<>')[1].replace(' ','_') + '" '
        
            tmp = getflash + classroom + youtube + address
            print( tmp )
            counter = counter + 1

            tmp = 'mv -f ' + classroom + ' ' + courseDirName
            print( tmp )
            #os.system( tmp )

        

        sys.exit()


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":

    download()


