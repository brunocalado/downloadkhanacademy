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

# Constants
youtube = "http://www.youtube.com/watch?v="
messageIfDownloadFinished = 'Done. Saved'
messageIfAlreadyDownloaded = 'has been fully downloaded'

# Configuration
mainIndexFilename = 'index'             # File with the courses to be downloaded 
downloadOutputFilename = 'temp'
ffmpeg_threads = '-threads 4 '          # threads for ffmpeg
retryIfDownloadFail = True
convertVideos = False


# Command line
wget = 'wget -c --output-document'
getflash = 'get_flash_videos --quality low --filename'
ffmpeg_p1 = 'ffmpeg -y -benchmark ' + ffmpeg_threads + '-strict experimental -i'
ffmpeg_p2 = '-acodec aac -ab 128k -vcodec mpeg4 -b 1200k -mbd 2 -flags +mv4+aic -trellis 1 -cmp 2 -subcmp 2 -s 320x240 -metadata title='

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

def download():

    # Get file with all classes from a course
    fileindex = returnFile(mainIndexFilename)           # Load file with desired courses
    for line in fileindex:
        courseIndexFile = line.split('<>')[0]
        courseDirName = line.split('<>')[1].replace(' ','_')
        courseFileName  = '.' + courseDirName 

        message( 'Getting ' + courseFileName )
        courseFileName = courseFileName.lower()

        tmp = wget + ' ' + courseFileName + ' ' + courseIndexFile
        message(tmp)
        os.system(tmp)
        
        # Create a list with all links from a course
        for i in returnFile( courseFileName ):
            if '<option ' in i:
                result = [ i.split('<')[1].split('>')[0].split('\"')[1], i.split('<')[1].split('>')[1] ]
                addressList.append( str( str(result[0]) ) + '<>'  + str(result[1]) )

        # Clean
        message('Removing useless files')
        os.system( 'rm -f ' + courseFileName + ' ' + downloadOutputFilename )

        
        # Download class by class
        if retryIfDownloadFail: flagRetry = True
        else:                   flagRetry = False

        while flagRetry:
            counter = 0
            for i in addressList:
                address = i.split('<>')[0]
                classroom = ' "' + str(counter).zfill(3) + '_' + i.split('<>')[1].replace(' ','_') + '.flv" '
            
                tmp = getflash + classroom + youtube + address + ' 2>&1 | tee ' + downloadOutputFilename 
                message( tmp )
                os.system( tmp )
                counter = counter + 1
                
                if retryIfDownloadFail:
                    for j in returnFile( downloadOutputFilename ):
                        if messageIfAlreadyDownloaded in j:
                            flagRetry = False
                            break
                        if messageIfDownloadFinished in j:
                            flagRetry = False
                            break
                        flagRetry = True

        # Convert the files to the desired format
        if convertFiles:
            counter = 0
            for i in addressList:
                address = i.split('<>')[0]
                classroom = ' "' + str(counter).zfill(3) + '_' + i.split('<>')[1].replace(' ','_') + '.flv" '
                
                tmp = ffmpeg_p1 + classroom + ffmpeg_p2 + classroom.replace('.flv','')[1:] + classroom.replace('.flv','.mp4')[1:]
                message( tmp )                                                 
                os.system( tmp )

                counter = counter + 1 


        # Create the directory
        tmp = 'mkdir -p ' + courseDirName
        message(tmp)
        os.system(tmp)

        # Move files
        counter = 0
        for i in addressList:
            address = i.split('<>')[0]
            if convertFiles:
                classroom = ' "' + str(counter).zfill(3) + '_' + i.split('<>')[1].replace(' ','_') + '.mp4" '
            else:
                classroom = ' "' + str(counter).zfill(3) + '_' + i.split('<>')[1].replace(' ','_') + '.flv" '
            
            tmp = 'mv -f ' + classroom + ' ' + courseDirName
            message( tmp )
            os.system( tmp )

            counter = counter + 1 

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    download()



