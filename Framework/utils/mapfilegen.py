'''
This is the map file generator for any URL that is provided.

'''
import argparse
from HTMLParser import HTMLParser

from selenium import webdriver

class MapFileGenerator(HTMLParser):
    def __init__(self, url, mapfilepath, filename='_mapfile_', fileprefix=''):
        self.url = url
        self.mapfilepath = mapfilepath
        self.mapfilename = fileprefix+filename

    def htmldomparser(self):
        pass

    def writetomap(self):
        pass

if __name__ == '__main__':
    #create the mapfilegen object with URL
    genobj = MapFileGenerator("http://m5dbweb-qa.m5colo.local", "./")
    #parse through the page for the objects
    #generate the map file for the page