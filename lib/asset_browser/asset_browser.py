import sys
#from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_asset_browser import Ui_AssetBrowser
import asset_browser_functions as abf

class AssetBrowserMain(QMainWindow, Ui_AssetBrowser):

#===============================================================================
# 
# CONSTRUCTOR
#
#===============================================================================

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #QApplication.setStyle(QStyleFactory.create('Plastique'))
        #QApplication.setPalette(QApplication.style().standardPalette())

#PROJECT combobox. Get all projects
        projects = abf.getAllProjects()
        self.combo_proj.addItem("")
        for proj in projects:
            self.combo_proj.addItem(proj['name'], QVariant(proj['id']))
        self.combo_proj.currentIndexChanged[int].connect(self.onProjSelected)

#ASSET TYPE combobox. Define asset types
        #------------------------------------- assetTypes = [{'name':'','id':0},
                      #-------------------------------- {'name':'Model','id':2},
                      #---------------------------------- {'name':'Rig','id':4},
                      #--------------------------------- {'name':'Anim','id':2},
                      #----------------------------------- {'name':'Fx','id':4},
                      #-------------------------------- {'name':'Light','id':5}]
        assetTypes = ['Model','Rig','Anim','Fx','Light']
        for type in assetTypes:
            self.combo_asset_type.addItem(type)
#            self.combo_asset_type.addItem(type['name'])
        self.combo_asset_type.setDisabled(True)
        self.combo_asset_type.currentIndexChanged[str].connect(self.onAssetTypeSelected) 

#SEQUENCE combobox.
        self.combo_seq.setDisabled(True)
        self.combo_seq.currentIndexChanged[int].connect(self.onSeqSelected)

#SHOT combobox.
        self.combo_sh.setDisabled(True)

#===============================================================================
# 
# METHODS
#
#===============================================================================

#Load SEQUENCES    
    def onProjSelected(self, proj_index):
        self.combo_seq.clear()
        self.combo_sh.clear()
        if proj_index!=0:
            self.combo_asset_type.setEnabled(True)
            self.combo_seq.setEnabled(True)
            proj_id = self.combo_proj.itemData(proj_index).toInt()[0]
            sequences = abf.getSequencesByProjId(proj_id)
            for seq in sequences:
                self.combo_seq.addItem(seq['code'], QVariant(seq['id']))
        else:
            self.combo_asset_type.setDisabled(True)

#Load ASSETS
    def onAssetTypeSelected(self, text):
        if text == '':
            None #self.combo_asset_type.setDisabled(True)
        elif text == 'Model':
            None
        elif text == 'Anim': 
            None
        elif text == 'Fx': 
            None
        elif text == 'Light':
            None
        else:
            None

#Load SHOTS    
    def onSeqSelected(self, seq_index):
        self.combo_sh.clear()
        
        self.combo_sh.setEnabled(True)
        seq_id = self.combo_seq.itemData(seq_index).toInt()[0]
        shots = abf.getShotsBySeqId(seq_id)
        for sh in shots:
            self.combo_sh.addItem(sh['code'])



            
        #self.label_asset_type.setText(str(text))
    
    #def getProjectsList(self):
        
    
if __name__ == "__main__":
    import sys
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtGui import *

    app = QtGui.QApplication(sys.argv)
    window = AssetBrowserMain()
    window.show()
    sys.exit(app.exec_())
    