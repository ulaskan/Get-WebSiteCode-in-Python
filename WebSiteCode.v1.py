#! /usr/bin/python3
####### UPLOAD VERSION 1
"""
Author: Ulas Askan
Date: 10 Oct 2016
Python version: 3.4
This program takes a web page URL in the form of www.... and retrieves the html code of the front page.
The program creates folders Pages and CSS. The main page is stored in Pages and all the .css files obtaind from
the main page are retrieved in the CSS folder. Next time the program is run the existeing folders are re-written.
"""

import os
import shutil
import urllib.request
import re

##### Function that Creates necessary folders. If they exist, they are deleted and re-written with no files
def MakeDirs(RootDir):
	if not os.path.exists(RootDir):
		os.mkdir(RootDir)
		os.chdir(RootDir)
		os.mkdir('Pages')
		os.mkdir('CSS')
	else:
		option = input("The Directories for this program to run already exists would you like to over-write them? (y/n): ")
		while option not in ('y', 'n', 'Y', 'N'):
			option = input("The Directories for this program to run already exists would you like to over-write them? (y/n): ")
		if option in ('y', 'Y'):
			shutil.rmtree(RootDir, ignore_errors=True, onerror=None)
			os.mkdir(RootDir)
			os.chdir(RootDir)
			os.mkdir('Pages')
			os.mkdir('CSS')
		if option in ('n', 'N'):
			print('Program exiting ...\n')

##### The Web page Class
class WebPage:
	def __init__(self, URL):	### initializing the web page name, like a function input
		self.URL = URL

	def GetCSS(self, PageIn):
		cssLinks = []
		with open(PageIn, 'r') as Contents:
			for line in Contents:
				if ".css\"" in line:
					TextSet = re.split(r'["]"*', line)
					for i in TextSet:
						if re.search("\.css", i):
							if 	i.startswith(r'http://'):
								cssLinks.append(i)
							elif i.startswith(r'https://'):
								cssLinks.append(i)
							elif i.startswith(r'//'):
								cssLinks.append('http:'+i)
							elif not i.startswith(r'http' or '//'):
								cssLinks.append(self.URL+'/'+i)
		return(cssLinks)

def Main():
	Location = input('Type the website whose code you want to download: ')
	site = WebPage('http://'+Location)
	print("\n\tProcessing... "+site.URL)
	MakeDirs(Location)

##### Getting the main page contents of the website
	MainPage = urllib.request.urlopen(site.URL)						### Get the main page and save it
	mainFolder = os.path.join(os.getcwd(), "Pages")
	with MainPage as page:
		with open(mainFolder+"/Main.html", 'w') as f:
			for line in page:
				line = line.decode('utf-8')
				f.write(line)

##### Getting the CSS files from the main page of the website:
	cssFolder = os.path.join(os.getcwd(), "CSS")
	cssFile = site.GetCSS(mainFolder+"/Main.html")
	for link in cssFile:
		CSSPage = urllib.request.urlopen(link)
		with CSSPage as page:
			linkName = link.replace("/","-")
			with open(cssFolder+"/"+linkName, 'w') as f:
				for line in page:
					line = line.decode('utf-8')
					f.write(line)

if __name__ == "__main__":
	print ('\n')
	Main()
	print ('\n')
