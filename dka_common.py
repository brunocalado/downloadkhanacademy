# -*- coding: UTF-8 -*-
import os, sys, glob 

debug = 0
 
#---------------------------------------------------------- 
#Funções 
#---------------------------------------------------------- 
def returnFile(fileName): 
	""" 
		Retorna o arquivo selecionado por fileName 
	""" 
	fileHandle = open(fileName, "r") 
	lines = (fileHandle.read()).splitlines() 
	fileHandle.close() 
	return lines 
 
def stringExists(string, fileName): 
	"""	 
		Procura uma linha que tenha uma string string no arquivo fileName 
		Se encontrar retorna True caso contrário False 
	"""  
	lines = returnFile(fileName) 
	for line in lines: 
		if string in line: 
			return True 
	return False 

def recoverLine(string, jumpLines, lines): 
	"""	 
		Procura uma linha que tenha uma string string no objeto lines 
		Então retorna a linha que esta jumpLines 
	""" 
	for i, line in enumerate(lines): 
		if string in line: 
			return lines[i+jumpLines] 
 
def recoverLineFromFile(string, jumpLines, fileName): 
	"""	 
		Procura uma linha que tenha uma string string no arquivo fileName 
		Então retorna a linha que esta jumpLines a frente 
	""" 
	lines = returnFile(fileName)
	return recoverLine(string, jumpLines, lines) 

def recoverLinesFromFile(string, startLine, fileName, lines=1):
	tmp = []
	for i in range(0, lines):
		tmp.append( recoverLineFromFile(string, startLine+i, fileName) )
	return tmp

def writeFile(fileName, string): 
	""" 
		Cria ou substitui o arquivo fileName pelo conteúdo de string 
	""" 
	fileHandle = open(fileName, "w") 
	fileHandle.writelines( str(string) + "\n" ) 
	fileHandle.close() 

def printLines(lines):
	""" 
		Imprime linhas uma após a outra 
	"""
	for line in lines:
		print( line )

def appendFile(fileName, string): 
	""" 
		Cria ou adiciona o arquivo fileName pelo conteúdo de string 
	""" 
	fileHandle = open(fileName, "a") 
	fileHandle.writelines( str(string) + "\n" ) 
	fileHandle.close()  





