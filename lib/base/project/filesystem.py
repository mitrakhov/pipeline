import os


class PipeFolders(object):

    def __init__(self, repo=os.environ['REPO']):

        self.repo = repo
        
        self.foldDict = {
                    'rootList': ['film', 'out', 'ref', 'src', 'temp'],
                    'filmList': ['assets', 'sequences'],
                    'shotList': ['anim', 'assets', 'comp', 'data', 'fx', 'light', 'out', 'src', 'tmp', 'proxy'],
                    'seqList': ['anim', 'assets', 'comp', 'data', 'fx', 'light', 'out', 'shots'],
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

    def addSequence(self, projName, seqName):

        seqPath = os.path.join(self.repo, projName, 'film', 'sequences', seqName)

        os.makedirs(seqPath)

        for sf in self.foldDict['seqList']:
            os.makedirs(os.path.join(seqPath, sf))
        for af in self.foldDict['assetList']:
            os.makedirs(os.path.join(seqPath, 'assets', af))
        for df in self.foldDict['dataList']:
            os.makedirs(os.path.join(seqPath, 'data', df))
        for of in self.foldDict['outList']:
            os.makedirs(os.path.join(seqPath, 'out', of))

    def addSequences(self, projName, seqList):

        for sq in seqList:
            self.addSequence(projName, sq)

    def addShot(self, projName, seqName, shName):

        shPath = os.path.join(self.repo, projName, 'film', 'sequences', seqName, 'shots', shName)

        os.makedirs(shPath)

        for sf in self.foldDict['shotList']:
            os.makedirs(os.path.join(shPath, sf))
        for af in self.foldDict['assetList']:
            os.makedirs(os.path.join(shPath, 'assets', af))
        for df in self.foldDict['dataList']:
            os.makedirs(os.path.join(shPath, 'data', df))
        for of in self.foldDict['outList']:
            os.makedirs(os.path.join(shPath, 'out', of))


if __name__ == '__main__':
    test = PipeFolders()
    sList = ['SQ07', 'SQ06', 'SQ08']
    test.addSequences('test_zzz', sList)