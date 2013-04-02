#!/usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
from dBase import DBase

class Projects(QDialog):

    def __init__(self, parent=None):
        super(Projects, self).__init__(parent)

        #Window title
        self.setWindowTitle("ProjectsUtil v0.001")

        #dBase connection
        self.db = DBase()
        self.projectsDict = self.db.getProjects()
        self.sequencesDict = {}

        #combo boxes
        self.projectsBox = QComboBox()
        self.sequencesBox = QComboBox()
        self.shotsBox = QComboBox()

        #combo boxes items
        self.projectsBox.addItems(self.projectsDict.keys())

        #combo boxes connections
        self.connect(self.projectsBox, SIGNAL("currentIndexChanged(int)"), self.updateSequences)
        self.connect(self.sequencesBox, SIGNAL("currentIndexChanged(int)"), self.updateShots)

        #labels
        projectLabel = QLabel("Project:")
        sequenceLabel = QLabel("Sequence:")
        shotLabel = QLabel("Shot:")

        
        #layout
        layout = QGridLayout()
        
        layout.addWidget(projectLabel, 0, 0)
        layout.addWidget(self.projectsBox, 0, 1)
        layout.addWidget(sequenceLabel, 1, 0)
        layout.addWidget(self.sequencesBox, 1, 1)
        layout.addWidget(shotLabel, 2, 0)
        layout.addWidget(self.shotsBox, 2, 1)

        self.setLayout(layout)

    def updateSequences(self):

        projName = unicode(self.projectsBox.currentText())
        projId = self.projectsDict[projName]
        self.sequencesDict = self.db.getSequences(projId)
        self.sequencesBox.clear()
        self.shotsBox.clear()
        self.sequencesBox.addItems(self.sequencesDict.keys())

    def updateShots(self):

        seqName = unicode(self.sequencesBox.currentText())
        seqId = self.sequencesDict[seqName]
        self.shotsBox.clear()
        self.shotsBox.addItems(self.db.getShots(seqId).keys())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Projects()
    form.show()
    app.exec_()