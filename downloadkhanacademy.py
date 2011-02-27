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

# Constants
youtube = "http://www.youtube.com/watch?v="
messageIfDownloadFinished = 'Done. Saved'
messageIfAlreadyDownloaded = 'has been fully downloaded'

# Configuration
mainIndexFilename = 'index'             # File with the courses to be downloaded 
downloadOutputFilename = 'temp'
ffmpeg_threads = '-threads 4 '          # threads for ffmpeg
retryIfDownloadFail = True
convertVideos = True
debug = False

# Command line
wget = 'wget -c --output-document'
getflash = 'get_flash_videos --quality low --filename'
ffmpeg_p1 = 'ffmpeg -y -benchmark ' + ffmpeg_threads + '-strict experimental -i'
ffmpeg_p2 = '-acodec aac -ab 128k -vcodec mpeg4 -b 1200k -mbd 2 -flags +mv4+aic -trellis 1 -cmp 2 -subcmp 2 -s 320x240 -metadata title='
ffmpeg_p3 = '-metadata album='

# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------
def returnFile(fileName): 
	fileHandle = open(fileName, "r") 
	lines = (fileHandle.read()).splitlines() 
	fileHandle.close() 
	return lines 

def message(msg):
    print( '\n\n' )
    print( '#' + 80*'-' )
    print( '# ' + msg )
    print( '#' + 80*'-' )

def removeSpecialChars(string):
    print(' ')



def download():

    # Get file with all classes from a course
    fileindex = returnFile(mainIndexFilename)           # Load file with desired courses
    for line in fileindex:
        addressList = []

        courseIndexFile = line.split('<>')[0]
        courseDirName = line.split('<>')[1].replace(' ','_')
        courseFileName  = '.' + courseDirName 

        message( 'Getting ' + courseFileName )
        courseFileName = courseFileName.lower()

        tmp = wget + ' ' + courseFileName + ' ' + courseIndexFile
        message(tmp)
        if not debug: os.system(tmp)
        
        # Create a list with all links from a course
        for i in returnFile( courseFileName ):
            if '<option ' in i:
                result = [ i.split('<')[1].split('>')[0].split('\"')[1], i.split('<')[1].split('>')[1] ]
                addressList.append( str( str(result[0]) ) + '<>'  + str(result[1]) )

        # Clean
        tmp  = 'rm -f ' + courseFileName + ' ' + downloadOutputFilename
        message( tmp )
        if not debug: os.system(tmp)

        
        # Download class by class
        classroomList = []

        counter = 0
        for i in addressList:
            address = i.split('<>')[0]
            classroom = ' "' + str(counter).zfill(3) + '_' + i.split('<>')[1].replace(' ','_') + '.flv" ' 
            classroomList.append( classroom )
        
            tmp = getflash + classroom + youtube + address + ' 2>&1 | tee ' + downloadOutputFilename 
            message( tmp )
            if not debug: os.system(tmp)
            
            if retryIfDownloadFail:
                for j in returnFile( downloadOutputFilename ):
                    if messageIfAlreadyDownloaded in j:
                        flagRetry = False
                        break
                    if messageIfDownloadFinished in j:
                        flagRetry = False
                        break
                    flagRetry = True
                if flagRetry:
                    if not debug: os.system(tmp)

            counter = counter + 1

        # Convert the files to the desired format
        if convertVideos:
            counter = 0
            for classroom in classroomList:
                finalFile = classroom.replace('.flv','.mp4')[1:].replace(' ','').replace('"', '')
                
                if not os.path.exists( finalFile ):
                    tmp = ffmpeg_p1 + classroom + ffmpeg_p2 + classroom.replace('.flv','')[1:] + ffmpeg_p3 + courseDirName + ' ' + finalFile
                    message( tmp )
                    if not debug: os.system(tmp)

                    counter = counter + 1
                else:
                    message("File already converted.")
        
        # Create the directory
        tmp = 'mkdir -p ' + courseDirName
        message(tmp)
        if not debug: os.system(tmp)

        # Move files
        counter = 0
        for classroom in classroomList:
            if convertVideos: classroom = classroom + ' ' + classroom.replace('.flv','.mp4')
            
            tmp = 'mv -f' + classroom + courseDirName
            message( tmp )
            if not debug: os.system(tmp)

            counter = counter + 1 

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    download()



