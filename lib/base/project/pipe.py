from shotgun_api3 import Shotgun
import dBase as db
import os
import shutil

class Pipe(object):
    
    def __init__(self, pName):
        self.pName = pName
        
    def getName(self):
        return self.pName
    

            
            