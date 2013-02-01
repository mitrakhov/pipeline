""" Script for checking if any files in script are not on the fileserver"""

def checkIfNotOnAServer(fileServer='/mnt/karramba'):
    
    nodesClassesList = ['Read', 'ReadGeo', 'ReadGeo2', 'Camera', 'Camera2']
    localList = []
    
    for nodeClass in nodesClassesList:
        for node in nuke.allNodes(nodeClass):
            path = node['file'].value()
            if path and path[:len(fileServer)] != fileServer:
                localList.append(node['name'].value())
                
    if localList:
        print nuke.message('\n'.join(localList) + '\nare not on a fileserver')
    else:
        nuke.message('Everything seems to be on a fileserver')
        