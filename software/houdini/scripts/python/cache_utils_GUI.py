import sys
import os

sys.path.append('/usr/pipeline/com')
sys.path.append('/usr/pipeline/software/houdini/scripts/python')
sys.path.append('/mnt/opt/hfs/houdini/python2.6libs')

from PyQt4 import QtCore
from PyQt4 import QtGui
import pyqt_thread_helper

import hou
import filesys
import cache_utils


def writeObjectsToCacheDialog():   
     
    def writeObjectsToCacheDiaglogInThread():

        class Form(QtGui.QDialog):
            def __init__(self, parent = None): 
                QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
                #super(Form, self).__init__(parent)
           
                layout = QtGui.QGridLayout()

                self.setGeometry(450, 300, 200, 100)
                self.setStyleSheet("background-color: rgb(50, 50, 50);")
                self.setWindowTitle("Write Objects to Cache")

                formats = ('bgeo', 'abc')
                writeMode = ('version', 'overwrite')
                frameRange = hou.playbar.playbackRange()
                
                #format
                self.formatLabel = QtGui.QLabel('Geometry Format')
                layout.addWidget(self.formatLabel, 0, 0)

                self.selectFormatComboBox = QtGui.QComboBox()
                self.selectFormatComboBox.addItems(formats)
                self.selectFormatComboBox.setFocus()
                layout.addWidget(self.selectFormatComboBox, 0, 1)
                self.connect(self.selectFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.selectScene)
                
                #framerange
                self.frameRangeLabel = QtGui.QLabel('Frame Range')
                layout.addWidget(self.frameRangeLabel, 1, 0)

                self.startFrameSpinBox = QtGui.QSpinBox()
                self.startFrameSpinBox.setRange(int(frameRange[0]), int(frameRange[1]))
                self.startFrameSpinBox.setValue(int(frameRange[0]))
                self.connect(self.startFrameSpinBox, QtCore.SIGNAL("valueChanged()"), self.selectScene)
                layout.addWidget(self.startFrameSpinBox, 1, 1)
                
                self.endFrameSpinBox = QtGui.QSpinBox()
                self.endFrameSpinBox.setRange(int(frameRange[0]), int(frameRange[1]))
                self.endFrameSpinBox.setValue(int(frameRange[1]))
                self.connect(self.startFrameSpinBox, QtCore.SIGNAL("valueChanged()"), self.selectScene)
                layout.addWidget(self.endFrameSpinBox, 1, 2)

                #mode
                self.writeModeLabel = QtGui.QLabel('Write Mode')
                layout.addWidget(self.writeModeLabel, 2, 0)

                self.selectWriteModeComboBox = QtGui.QComboBox()
                self.selectWriteModeComboBox.addItems(writeMode)
                layout.addWidget(self.selectWriteModeComboBox, 2, 1)
                self.connect(self.selectWriteModeComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.selectScene)
                
                #ok button
                okButton = QtGui.QPushButton('Ok', self)
                self.connect(okButton, QtCore.SIGNAL('clicked()'), self.pushOk)
                okButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
                layout.addWidget(okButton, 3, 1)

                #cancel button
                cancelButton = QtGui.QPushButton('Cancel', self)
                cancelButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
                layout.addWidget(cancelButton, 3, 2)
             

                self.setLayout(layout)

            def selectScene(self):
                    print ('Format  - ' + str(self.selectFormatComboBox.currentText()))
                    print ('Mode - ' + str(self.selectWriteModeComboBox.currentText()))
                    print ('Frame range - ' + str(self.startFrameSpinBox.value()) + ', ' + str(self.endFrameSpinBox.value()))
                
            def pushOk(self):
                cache_utils.cacheWrite(self.startFrameSpinBox.value(), self.endFrameSpinBox.value(), 1, str(self.selectFormatComboBox.currentText()), str(self.selectWriteModeComboBox.currentText()))


        app = pyqt_thread_helper.getApplication()
        form = Form()
        form.show()
        app.exec_()

    pyqt_thread_helper.queueCommand(writeObjectsToCacheDiaglogInThread)



def loadObjectsFromCacheDialog():

    def loadObjectsFromCacheDiaglogInThread():
        # sceneName = hou.getenv('HIPNAME').rsplit('.v',1)[0]
        # dataPath = os.path.join(hou.getenv('DATA'), 'geo')
        
        # CACHES = {}
        # shotCachesList = []
        # shotCachesList.append(os.listdir(dataPath))

        # for n in shotCachesList[0]:
        #     cacheScene = filesys.cache(n, dataPath)
        #     for n, m in zip(cacheScene.getAllSceneData(fullPath = False).keys(), cacheScene.getAllSceneData(fullPath = False).values()):
        #         CACHES[n] = m

        # print CACHES
        # OBJ = cacheScene.getAllSceneData(fullPath = False)
        # print OBJ
        selectedScene = []
        shotName = 'sh_107_112'
        dataPath = '/home/vlad/Documents/sh_107_112/data/cache'
        shotCache = filesys.data(shotName, dataPath )

        DATA = shotCache.getAllData()

        #class Form(QtGui.QDialog):
        class Form(QtGui.QWidget):
            combo = {}
            
            #selectedObjects = {}
            def __init__(self, parent = None): 
                QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
                # self.objs = []
                # self.vers = []
                # self.OBJ1 = {}
                # self.cacheScene1 = filesys.cache(sceneName, dataPath)
           
                layout = QtGui.QVBoxLayout()

                self.setGeometry(150, 300, 300, 50)
                self.setStyleSheet("background-color: rgb(50, 50, 50);")
                self.setWindowTitle("Load Objects from Cache")
                objColumnLayout = QtGui.QGridLayout()

                columnName = ('Scene', 'Object', 'Version')
                for n in columnName:
                    self.columnNameLabel = QtGui.QLabel(n)
                    objColumnLayout.addWidget(self.columnNameLabel, 0, columnName.index(n))
                
                self.sceneComboBox = QtGui.QComboBox()
                self.sceneComboBox.addItems(shotCache.getSceneName())
                objColumnLayout.addWidget(self.sceneComboBox, 1, 0)
                self.connect(self.sceneComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.selectScene)

                print self.sceneComboBox.currentIndex()

                #print self.sceneComboBox.currentIndexChanged()


                #for k, v in zip(shotCache.getSceneName(), OBJ.values()):
                #for k in selectedScene:
                    #self.kLabel = QtGui.QLabel(k)
                    # self.vLabel = QtGui.QLabel(max(v))
                    # lineNum = sorted(OBJ.keys()).index(k) + 1

                    #objColumnLayout.addWidget(self.kLabel, lineNum, 1)

                    # self.vComboBox = QtGui.QComboBox()
                    # self.combo[k] = self.vComboBox
                    # self.vComboBox.setObjectName(k + '_ComboBox')
                    # self.vComboBox.addItems(v)
                    # #self.vComboBox.setCurrentIndex(len(v)-1)
                    # objColumnLayout.addWidget(self.vComboBox, lineNum, 2)
                    # #self.connect(self.vComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.selectVersions)

                    # self.vCheckBox = QtGui.QCheckBox()
                    # self.vCheckBox.setObjectName(k)
                    # self.vCheckBox.clicked.connect(self.selectObjects)

                    # objColumnLayout.addWidget(self.vCheckBox, lineNum, 3)

                layout.addLayout(objColumnLayout)

                buttonsLayout = QtGui.QHBoxLayout()

                #ok button
                okButton = QtGui.QPushButton('Ok', self)
                self.connect(okButton, QtCore.SIGNAL('clicked()'), self.pushOk)
                okButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
                buttonsLayout.addWidget(okButton)

                #cancel button
                cancelButton = QtGui.QPushButton('Cancel', self)
                cancelButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
                buttonsLayout.addWidget(cancelButton)

                layout.addLayout(buttonsLayout) 
                self.setLayout(layout)

            def selectScene(self):
                sender = self.sender()
                selectedScene = shotCache.getData(str(sender.currentText())).keys()

            def selectObjects(self):
                sender = self.sender()
                self.objs.append(sender.objectName())

            def selectVersions(self):
                sender = self.sender()
                print str(sender.currentText())

            def pushOk(self):      
                for n in self.objs:
                    self.selectedObjects[str(n)] = str(self.combo[str(n)].currentText())
                for n, m in zip(self.selectedObjects.keys(), self.selectedObjects.values()):
                    filePath = cacheScene.getData(n, m)
                    node = hou.node('/obj').createNode('geo', n + '_CACHE')
                    node.children()[0].destroy()
                    ext = filePath.rsplit('.')[-1]
                    if ext == 'bgeo':
                        bgeoLoader = hou.node(node.path()).createNode('file', node_name = 'bgeoLoader')
                        bgeoLoader.parm('file').set(filePath)
                    if ext == 'abc':
                        abcLoader = hou.node(node.path()).createNode('alembic', node_name = 'abcLoader')
                        abcLoader.parm('fileName').set(filePath)
               
   

        app = pyqt_thread_helper.getApplication()
        form = Form()
        form.show()
        app.exec_()

    pyqt_thread_helper.queueCommand(loadObjectsFromCacheDiaglogInThread)


loadObjectsFromCacheDialog()