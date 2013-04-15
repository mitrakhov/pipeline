import pyqt_thread_helper
import sys
import os

def writeObjectsToCache_Menu():   
     
    def writeObjectsToCacheDiaglogInThread():
        from PyQt4 import QtCore
        from PyQt4 import QtGui

        import hou
        import cache_utils

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
                self.connect(self.selectFormatComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateUi)
                
                #framerange
                self.frameRangeLabel = QtGui.QLabel('Frame Range')
                layout.addWidget(self.frameRangeLabel, 1, 0)

                self.startFrameSpinBox = QtGui.QSpinBox()
                self.startFrameSpinBox.setRange(int(frameRange[0]), int(frameRange[1]))
                self.startFrameSpinBox.setValue(int(frameRange[0]))
                self.connect(self.startFrameSpinBox, QtCore.SIGNAL("valueChanged()"), self.updateUi)
                layout.addWidget(self.startFrameSpinBox, 1, 1)
                
                self.endFrameSpinBox = QtGui.QSpinBox()
                self.endFrameSpinBox.setRange(int(frameRange[0]), int(frameRange[1]))
                self.endFrameSpinBox.setValue(int(frameRange[1]))
                self.connect(self.startFrameSpinBox, QtCore.SIGNAL("valueChanged()"), self.updateUi)
                layout.addWidget(self.endFrameSpinBox, 1, 2)

                #mode
                self.writeModeLabel = QtGui.QLabel('Write Mode')
                layout.addWidget(self.writeModeLabel, 2, 0)

                self.selectWriteModeComboBox = QtGui.QComboBox()
                self.selectWriteModeComboBox.addItems(writeMode)
                layout.addWidget(self.selectWriteModeComboBox, 2, 1)
                self.connect(self.selectWriteModeComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateUi)
                
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

            def updateUi(self):
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




def loadObjectsFromCache_Menu():

    def loadObjectsFromCacheDiaglogInThread():
        from PyQt4 import QtCore
        from PyQt4 import QtGui
        
        import filesys
        import hou

        class Form(QtGui.QDialog):
            def __init__(self, parent = None): 
                QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
           
                layout = QtGui.QVBoxLayout()

                self.setGeometry(150, 300, 250, 50)
                self.setStyleSheet("background-color: rgb(50, 50, 50);")
                self.setWindowTitle("Load Objects from Cache")

                objColumnLayout = QtGui.QGridLayout()

                scenePath = os.path.join(hou.getenv('HIP'), hou.getenv('HIPNAME'))
                dataPath = hou.getenv('CACHE')
                cacheScene = filesys.cache(scenePath, dataPath)
                #cacheScene = filesys.cache('/home/sim/Documents/untitled.v005.hip', '/home/sim/Documents/geo')
                OBJ = cacheScene.getAllSceneData(fullPath = False)

                columnName = ('Object', 'Version')
                for n in columnName:
                    self.columnNameLabel = QtGui.QLabel(n)
                    objColumnLayout.addWidget(self.columnNameLabel, 0, columnName.index(n))


                for k, v in zip(OBJ.keys(), OBJ.values()):
                    self.kLabel = QtGui.QLabel(k)
                    self.vLabel = QtGui.QLabel(max(v))
                    lineNum = sorted(OBJ.keys()).index(k) + 1

                    objColumnLayout.addWidget(self.kLabel, lineNum, 0)
                    #objColumnLayout.addWidget(self.vLabel, lineNum, 1)

                    self.vComboBox = QtGui.QComboBox()
                    self.vComboBox.addItems(v)
                    self.vComboBox.setCurrentIndex(int(max(v)))
                    objColumnLayout.addWidget(self.vComboBox, lineNum, 1)
                    self.connect(self.vComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateUi)

                    vCheckBox = QtGui.QCheckBox()
                    objColumnLayout.addWidget(vCheckBox, lineNum, 2)
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

            def updateUi(self):
                    print str(self.vComboBox.currentText())

                
            def pushOk(self):
                cache_utils.cacheWrite(self.startFrameSpinBox.value(), self.endFrameSpinBox.value(), 1, str(self.selectFormatComboBox.currentText()), str(self.selectWriteModeComboBox.currentText()))
   

        app = pyqt_thread_helper.getApplication()
        form = Form()
        form.show()
        app.exec_()

    pyqt_thread_helper.queueCommand(loadObjectsFromCacheDiaglogInThread)


#node = hou.node('/obj').createNode('geo', 'NODE')
#node.children()[0].destroy()
#bgeoLoader = hou.node(node.path()).createNode('file')
#abcLoader = hou.node(node.path()).createNode('alembic')
#bgeoLoader.parm('file').set('/home/vlad/')