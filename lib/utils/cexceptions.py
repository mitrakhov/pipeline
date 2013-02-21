import pweb
reload(pweb)
import inspect
ID_ERROR = '2'
ID_FATAL = '1'
ID_WARN = '3'

RED_MESSAGE = '\033[1;31m%s\033[1;31m'


class WarningException(Exception):
    def __init__(self, value):
        self.value = value
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_WARN,' ')
    
    def __str__(self):
        return repr(self.value) 

class FatalException(Exception):
    def __init__(self, value):
        self.value = value
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_FATAL,' ')
    
    def __str__(self):
        return repr(self.value) 

class Exception(Exception):
    def __init__(self, value):
        self.value = value
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
    
    def __str__(self):
        return repr(self.value) 

#----------Exception classes---------------------
class Error(Exception):
    pass


#---------- Common
class NotImplementedYet(Error):
    pass

class LenArgsError(Error):
    def __init__(self, len_actual, len_need):
        self.mess = "Needs arguments %s, actually - %s"%(len_need,len_actual)
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.mess),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.mess) 

#---------- Assets
class AssetError(Error):
    def __init__(self, assetname):
        self.assetname = assetname
        self.value = assetname
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str(RED_MESSAGE%self.assetname) 
        
class AssetExistsError(Error):
    def __init__(self, assetname):
        self.assetname = assetname
        self.value = assetname
        stack = inspect.stack()
        self.value += '\nPossible solution:\nYou have to create new asset under new name or remove old one.'
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str(RED_MESSAGE%self.assetname) 

class ParentOrTypeNotExistsError(AssetError):
    def __init__(self, assetname):
        AssetError.__init__(self,assetname)

class AssetDoesntExistError(AssetError):
    pass

class AssetVersionNotFoundError(AssetError):
    def __init__(self, assetname, version):
        self.version = version
        AssetError.__init__(self,assetname)

class InfoNotFoundError(Exception):
    def __init__(self, assetname):
        self.filename = assetname
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filename),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.filename) 

class ProjectDoesNotExists(Exception):
    def __init__(self, projects_lst,name=None):
        self.projects_lst = projects_lst
        self.name = name
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.name),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        if self.name:
            return str(self.name + ' name project not found\n\033[1;37m\033[1;33mSelect name projects:\033[1;31m\n'+'\n'.join(self.projects_lst) + '\033[1;m')
        return str('name project not found\n\033[1;37m\033[1;33mSelect name projects:\033[1;31m\n'+'\n'.join(self.projects_lst) + '\033[1;m')

class SequenceDoesNotExists(Exception):
    def __init__(self, sequences_lst,name=None,project_name=None):
        self.sequences_lst = sequences_lst
        self.name = name
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\nProject name: %s\nScene name: %s'%(stack[1][2],stack[1][1],project_name,self.name),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        if self.name:
            return str(self.name + ' name sequence not found\n\033[1;37m\033[1;33mSelect name sequences:\033[1;31m\n'+'\n'.join(self.sequences_lst) + '\033[1;m')
        return str('name sequence not found\n\033[1;37m\033[1;33mSelect name sequences:\033[1;31m\n'+'\n'.join(self.sequences_lst) + '\033[1;m')

class ShotDoesNotExists(Exception):
    def __init__(self, shots_lst):
        self.shots_lst = shots_lst
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.shots_lst),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str('name shot not found\n\033[1;37m\033[1;33mSelect name shots:\033[1;31m\n'+'\n'.join(self.shots_lst) + '\033[1;m')

class SequenceExists(Exception):
    def __init__(self, name):
        self.sequence = name
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.sequence),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str(RED_MESSAGE%self.sequence)

#-------------- Files
class FileDoesntExistsError(Error):
    def __init__(self, filename):
        self.filename = filename
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filename),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str(RED_MESSAGE%self.filename) 
        
class FiledError(Error):
    def __init__(self, filedname):
        self.filedname = filedname
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filedname),type(self).__name__,ID_ERROR,' ')
        
class FieldExistsError(FiledError):
    pass

class ShotExistsError(AssetError):
    def __init__(self, assetname):
        self.filename = assetname
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filename),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str(RED_MESSAGE%self.filename)  
        
class ShotDoesNotCreate(Error):
    def __init__(self, filedname):
        self.filedname = filedname
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filedname),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return str(RED_MESSAGE%self.filename)
#--------------- Gentoo
class CategoryDoesntExistsError(Error):
    def __init__(self, filename):
        self.filename = filename
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filename),type(self).__name__,ID_ERROR,' ')
        
#--------------- Encoder
class EncoderError(Error):
    def __init__(self, filename):
        self.filename = filename
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.filename),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.filename)

#--------------- DB
class RecordError(Error):
    def __init__(self, value):
        self.value = value
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
class FieldExistsError(Error):
    def __init__(self, value):
        self.value = value
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
#--------------- Maya
class UntitledFileFound(Error):
    def __init__(self):
        self.value = 'Untitled!!!'
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
    
    def __str__(self):
        return repr(self.value)

class MaterialError(Error):
    def __init__(self, message):
        self.value = message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
    
    def __str__(self):    
        return repr(self.value)

class PublishError(Error):
    def __init__(self, message, scene_name, name_project):
        self.value = 'Publish error for ' + message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\nScene name: %s\nProject name: %s'%(stack[1][2],stack[1][1],self.value,scene_name,name_project),type(self).__name__,ID_ERROR,' ')
    
    def __str__(self):
        return repr(self.value)

class NoFoundsEdlCameras(Error):
    def __init__(self, message):
        self.value = 'No found EDL attribute on cameras. Attribute "EDL" is required!!!'
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
    
    def __str__(self):
        return repr(self.value)

class ModelError(Error):
    def __init__(self, message):
        self.value = 'Could not checkin. ' + message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.value)

class NoSelectionFound(Error):
    def __init__(self, message):
        self.value = 'No selection found!!! ' + message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.value)

#---------------- Pipe
class UnknownError(Error):
    def __init__(self, message):
        self.value = '...!!! ' + message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.value)

#---------------- Rig
class selectionError(Error):
    def __init__(self, message):
        self.value = message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.value)
class objectError(Error):
    def __init__(self, message):
        self.value = message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.value)
class argumentsError(Error):
    def __init__(self, message):
        self.value = message
        stack = inspect.stack()
        pweb.logger_add_row('%s %s\n%s'%(stack[1][2],stack[1][1],self.value),type(self).__name__,ID_ERROR,' ')
        
    def __str__(self):
        return repr(self.value)

