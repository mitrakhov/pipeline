def writeObjectsToCache_Menu():
    import pyqt_thread_helper
     
    def writeObjectsToCacheDiaglogInThread():
        import sys
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

                formats = ('abc', 'bgeo')
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
