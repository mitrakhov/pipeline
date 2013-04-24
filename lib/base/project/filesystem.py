import os


class PipeFolders(object):

    def __init__(self):

        self.repo = os.environ['REPO']
        
        self.foldDict = {
                    'rootList': ['film', 'out', 'ref', 'src', 'temp'],
                    'filmList': ['assets', 'sequences'],
                    'shotList': ['anim', 'comp', 'data', 'fx', 'light', 'out', 'src', 'tmp', 'proxy'],
                    'seqList': ['anim', 'comp', 'data', 'fx', 'light', 'out', 'shots'],
                    'assetList': ['light', 'material', 'mattepaint', 'model', 'rig', 'shader', 'textures'],
                    'dataList': ['cache', 'geo', 'render', 'shadowmap', 'sim', 'track', 'photonmap'],
                    'outList': ['dailies', 'hires'],
                    'srcList': ['plates', 'editRef']
                    }

    def addProject(self, projName):

        projPath = os.path.join(self.repo, projName)

        os.makedirs(projPath)

        for rf in self.foldDict['rootList']:
            os.makedirs(os.path.join(projPath, rf))
        for ff in self.foldDict['filmList']:
            os.makedirs(os.path.join(projPath, 'film', ff))
        for af in self.foldDict['assetList']:
            os.makedirs(os.path.join(projPath, 'film', 'assets', af))
        for of in self.foldDict['outList']:
            os.makedirs(os.path.join(projPath, 'out', of))

if __name__ == '__main__':
    test = PipeFolders()
    test.addProject('NewTest')