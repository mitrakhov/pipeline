"""@file filesys.py
@package com.filesys
Work with file system - copy, create dirs, move, directory structure e.t.c.
""" 
import warnings
warnings.simplefilter("ignore",DeprecationWarning)
from cexceptions import *
import cdebug, popen2, shutil, subprocess
import os, platform, commands, shlex, getopt, re
import stat 
import time
import socket

if os.getenv('DEVMODE') != 0:
    reload(cdebug)
    
from xml.dom import minidom

HOST = socket.gethostname()

PARENTTASK_ASSET = 0
PARENTTASK_SHOT = 1
PARENTTASK_PROJECT = 2
PARENTTASK_SEQUENCE = 3

TYPE_EXTRA_EVENT = 0

PS_TEST = 0
PS_PROGRESS = 1
PS_STOP = 2
PS_PEND_ARCH = 3
PS_ARCHIVED = 4
PROJECT_STATUS = [PS_TEST,PS_PROGRESS,PS_STOP,PS_PEND_ARCH,PS_ARCHIVED]

MODE_DEFAULT = 'default'
MODE_MAX = 'max'
MODE_MAYA = 'maya'
MODE_HOUDINI = 'houdini'
MODE_NUKE = 'nuke'
MODE_PHOTOSHOP = 'psd'
MODE_AFTER = 'after'

CONSOLE_Black =  "\033[0;30m%s\033[1;m"     
CONSOLE_Dark_Gray     =  "\033[1;30m%s\033[1;m"
CONSOLE_Blue        =  "\033[0;34m%s\033[1;m"   
CONSOLE_Light_Blue   =  "\033[1;34m%s\033[1;m"
CONSOLE_Green       =  "\033[0;32m%s\033[1;m"  
CONSOLE_Light_Green   =  "\033[1;32m%s\033[1;m"
CONSOLE_Cyan        =  "\033[0;36m%s\033[1;m" 
CONSOLE_Light_Cyan   =  "\033[1;36m%s\033[1;m"
CONSOLE_Red        =  "\033[0;31m%s\033[1;m"
CONSOLE_Light_Red   =  "\033[1;31m%s\033[1;m"
CONSOLE_Purple     =  "\033[0;35m%s\033[1;m"
CONSOLE_Light_Purple =  "\033[1;35m%s\033[1;m"
CONSOLE_Brown      =  "\033[0;33m%s\033[1;m" 
CONSOLE_Yellow       =  "\033[1;33m%s\033[1;m"
CONSOLE_Light_Gray =  "\033[0;37m%s\033[1;m"
CONSOLE_White      =  "\033[1;37m%s\033[1;m"

QT_SETTINGS_GRP = 'Terminal.fx'

URL_TRACKER = 'http://pipeline'

ENVS = ['REPO','PYTHONPATH','SHOW_OUT_DAILIES','ICONS','PROJ_ANIM_PATH','PROJ_FX_PATH','PROJ_ASSET_PATH','PROJ_COMP_PATH']

JOB_LOCAL = 'job.local'

PROJECTS_STATUS = [(0,'test'),(1,'progress'),(2,'finish')]

mdebug = cdebug.cdebug()

class ImageSequences(object):
    """Return class of _imageSequence list
    usage: ImageSequences("/path/to/files/")
    """
    def __init__(self,path,parent=None):
        self.__dict = {}
        self.__keys = []
        lst = filter(lambda x: os.path.isfile(path + os.sep + x), os.listdir(path))
        pat = re.compile('.*([_]|[\.])(\d{1,10})\.(.*)')
        lst_f = [(x,pat.search(x)) for x in lst if pat.search(x)]
        self.sequences = []
        if not lst_f: return
        while lst_f:
            filename, match = lst_f[0]
            seq = ImageSequence(path + os.sep + filename)
            if seq: self.sequences.append(seq)
            sep = match.group(1)
            sep_index = match.start(1)
            pat1 = re.compile('%s.*'%filename[:sep_index])
            lst_f = filter(lambda x: not pat1.search(x[0]), lst_f)
    
    def get_sequences(self):
        return self.sequences

class ImageSequence(object):
    def __new__(cls,path,parent=None):
        try:
            if os.path.isdir(path):
                lst = os.listdir(path)
                lst_f = filter(lambda x: os.path.isfile(path + os.sep + x), lst)
                if not lst_f or len(lst_f) == 1: return None
            elif os.path.isfile(path):
                name_fl = path
                path1 = name_fl.rsplit(os.sep,1)[0]
                lst_f = [name_fl]
                lst = os.listdir(path1)
                lst_ftemp = filter(lambda x: os.path.isfile(path1 + os.sep + x), lst)
                if not lst_ftemp or len(lst_ftemp) == 1: return None
            else:
                raise Exception("Error! Not known type:"+path)
        except:
            raise Exception('Wrong image sequence from path: ' + path)
        return _imageSequence(path)
        
class _imageSequence(object):
    def __init__(self,path,parent=None):
        pat = re.compile('.*([_]|[\.])(\d{1,10})\.(.*)')
        name_fl = ''
        start_file = ''
        end_file = ''
        lst_padd = None
        try:
            if os.path.isdir(path):
                lst = os.listdir(path)
                lst_f = filter(lambda x: os.path.isfile(path + os.sep + x), lst)
                if not lst_f: return None
                lst_f = filter(lambda x: pat.search(x), lst)
                lst_padd = [int(pat.search(x).group(2)) for x in lst if pat.search(x)]
                lst_f.sort()
                name_fl = path + os.sep + lst_f[0]
                start_file =  min(lst_padd)
                end_file = max(lst_padd)
                lst_f = [path + os.sep + lst_f[0]] 
            elif os.path.isfile(path):
                name_fl = path
                path, filename = name_fl.rsplit(os.sep,1)
                match = pat.search(filename)
                sep = match.group(1)
                sep_index = match.start(1)
                pat1 = re.compile('%s.*'%filename[:sep_index])
                lst_f = filter(lambda x: pat1.search(x), os.listdir(path))
                lst_padd = [int(pat.search(x).group(2)) for x in lst_f if pat.search(x)]
                start_file =  min(lst_padd)
                end_file = max(lst_padd)
            else:
                raise Exception("Error! Not known type:"+path)
        except Exception, e:
            print e
            raise Exception('Wrong image sequence from path: ' + path)
            
        srch = pat.search(name_fl)
        sep_index = srch.start(1)
        self.__sep = srch.group(1)
        self.__name = lst_f[0].rsplit(self.__sep,1)[0]
        self.__ext =  srch.group(3)
        self.__lenOfpadding = len(srch.group(2))
        self.__range = (0,1)
        self.__length = len(lst_f)
        self.__start = start_file
        lst_f = [x for x in lst_f if x[len(self.__ext)*(-1):] == self.__ext]
        self.__filepath = path + os.sep + lst_f[0]
        srch = pat.search(lst_f[-1])
        self.__end = end_file
        self.__files = lst_f
        self.root_path = path
        self.tag = []
        self.__omissions = [x for x in xrange(start_file,end_file) if not x in lst_padd]
        self.__filename = name_fl[len(self.root_path)+1:sep_index]
        self.__first_file = name_fl.split(os.sep)[-1]
        
    def _sort_by_time(self,a,b):
        file_stats_a = os.stat(a)
        file_stats_b = os.stat(b)
        if time.localtime(file_stats_a[stat.ST_MTIME]) > time.localtime(file_stats_b[stat.ST_MTIME]):
            return 1
        elif time.localtime(file_stats_a[stat.ST_MTIME]) == time.localtime(file_stats_b[stat.ST_MTIME]):
            return 0
        else:
            return -1
    
    def getFilePath(self):
        return self.__filepath
    
    def getFirstFile(self):
        return self.__first_file
    
    def getPath(self):
        return self.root_path
    
    def    fix_padding(self):
        fls = map(lambda x:  self.root_path + os.sep + x, self.__files)
        fls.sort(self._sort_by_time)
        if not test_access(self.root_path): raise Exception('Error: you do not have permission READ WRITE')
        
        for i, f in zip(xrange(len(fls)),fls):
            new_fl = self.root_path + os.sep + self.__name +'.' + padding(i,4) + '.' +  self.__ext
            os.system('mv %s %s'%(f, new_fl))
    
    def getOmissions(self):
        return self.__omissions
    
    def getContent(self):
        return self.__files
    
    def    getFileName(self):
        return self.__filename
    
    def getName(self):
        return self.__name
    
    def getExt(self):
        return self.__ext
    
    def getRange(self):
        return (self.__start,self.__end)
    
    def getLenght(self):
        return len(self)
    
    def getLengthOfPadding(self):
        return self.__lenOfpadding
    
    def getSep(self):
        return self.__sep
    
    def __len__(self):
        return self.__length

    def __str__(self):
        return "name: %s, padding separator: %s, length: %s, extension: %s, start: %s, end: %s"%(self.__filename,self.__sep,len(self),self.__ext,self.__start,self.__end)
        #return str(self.__files) 
    
class ImageReader(object):
    def __new__(cls, mode):
        if 'imageFormatMode_' +mode in globals().keys():
            return globals()['imageFormatMode_' +mode]()
        else:
            return object.__new__(cls,mode)
            
    def __init__(cls,mode,parent=None):
        super(ImageReader, cls).__init__(mode)

    def get_format(self):
        return 'jpg'

    def get_ext(self):
        return '.jpg'
    
    def get_format_number(self):
        return 8

class imageFormatMode_maya(object):
    def __init__(self,parent=None):
        self.__format = 'png'
        self.__ext = '.'+self.__format

    def get_format(self):
        return self.__format

    def get_ext(self):
        return self.__ext
    
    def get_format_number(self):
        return 32 
    

def get_resources(path):

    ignore = ['tmp']
    resources = []
    dict_resources = {}
    
    def get_resource(path):
        seqs = ImageSequences(path)
        return seqs.get_sequences()
    
    def get_dirs(path):
        res = []
        for x in filter(lambda x: os.path.isdir(path + os.sep + x), os.listdir(path)):
            if x in ignore: continue
            res.append(path + os.sep + x)
            res.extend(get_dirs(path + os.sep + x))
        return res 
    
    for x in filter(lambda x: os.path.isdir(path + os.sep + x) and x.isdigit(), os.listdir(path)):
        comp = []
        comp.append(path + os.sep + x)
        comp.extend( get_dirs(path + os.sep + x))
        resources.append((x,comp))
    
    for x, y in resources:
        comp = map(lambda z: get_resource(z), y)[0]
        if not comp: continue
        for z in comp:
            name = z.getFileName()
            if name in dict_resources.keys():
                dict_resources[name].append((x,z,)) # apended (0002,<ImageSequence object>,)
            else:
                #z.tag.append(x)
                dict_resources[name] = [(x,z,)]
    
    return dict_resources

def mkdirs(full_path):
    os.makedirs(full_path)
    return True

def copyfile(src,dst):
    shutil.copy(src,dst)
    os.system('chmod 766 %s'%dst)
    return True

def test_access(src):
    """Return true if RW access is OK
    @param[in] src is list.
    """
    ret = True
    if not os.path.exists(src): raise Exception('Directory not exists: ' + src)
    
    def __get_files(_src):
        _ret = []
        _lst = [_src + os.sep + x for x in os.listdir(_src)]
        for x in _lst:
            if os.path.isdir(x): 
                _ret.extend(__get_files(x))
                _ret.append(x)
            else: _ret.append(x)
        return _ret
    lst = __get_files(src)
    for i in lst:
        ret = ret and os.access(i, os.R_OK|os.W_OK)
    return ret

def frange(start, stop=None, step=1.0, delta=0.0000001):
    """a range generator that handles floating point numbers
    uses delta fuzzy logic to avoid float rep errors
    eg. stop=6.4 --> 6.3999999999999986 would slip through
    """
    # if start is missing it defaults to zero
    if stop == None:
        stop = start
        start = 0.0
    # allow for decrement
    if step <= 0:
        while start > (stop + delta):
            yield start
            start += step
    else:
        while start < (stop - delta):
            yield start
            start += step
            
def padding(num, size):
    """Return string that padding for file
    @param[in] num Number to padding.
    @param[in] size Size for padding.
    """
    padd = "%(#)0"+str(size)+"d"
    return padd%{"#":int(num)}

def check_file_name(file_name):
    MASKS = ['\s','\.','\;','\W',]
    p = re.compile('|'.join(['(%s)'%x for x in MASKS]))
    if p.search(file_name): raise Exception('File name mast be content only characters and numbers w/o space!')
    return True

def file_new_version(folder,file_name):
    """Return name file with new vesion
    @param[in] folder Directory contained file.
    @param[in] file_name Name of file.
    """
    # for 'file.1.ext'
    if folder[-1] == os.sep: folder = folder[:-1]
    if not os.path.exists(folder+os.sep+file_name): raise Exception('Path ' +folder+os.sep+file_name+ ' not exists')
    
    if file_name.count('.') >= 2 and file_name.rsplit('.')[-2].isdigit():
        file_wo_padding = file_name.rsplit('.',2)[0]
        file_ext = file_name.split('.')[-1]
        #learn version file
        dirlist = filter(lambda s: re.match(file_wo_padding+'[.]\d*[.]'+file_ext,s),os.listdir(folder))
        if not dirlist: raise Exception("Files not exists")
        next_vers = 0
        for item in dirlist:
            mdebug(item.split('.')[-2])
            if (int(item.split('.')[-2]) > next_vers):
                next_vers = int(item.split('.')[-2])
        next_vers += 1
        #learn padding file
        pad = 1
        for item in dirlist:
            if (int(item.split('.')[-2]) < pad):
                pad = int(item.split('.')[-2])
        dirlist = filter(lambda s: re.match(file_wo_padding+'[.]\d*'+str(pad)+'[.]'+file_ext,s),os.listdir(folder))
        if not dirlist: raise Exception("File for padding not found")
        pad = len(dirlist[0].split('.')[-2])
        #return (full file name, version)
        return (folder + os.sep + file_wo_padding + '.' + str(padding(next_vers, pad)) + '.' + file_ext,next_vers,)
    # for 'file_1.ext'
    #elif (file_name.count('.') == 1) and (file_name.find('_') > 1) and (file_name.find('.') > file_name.find('_')):
    #    raise Exception('not emplemented yet')
    elif file_name.count('.') == 1:
        file_wo_padding, file_ext = file_name.rsplit('.',1)
        pat = re.compile('\.(\d*)\.')
        loc_path = folder
        index = 1
        lst_vers = [(int(pat.search(x).group(1)),loc_path+os.sep+x) for x in filter(lambda x: pat.search(x), os.listdir(loc_path))]
        if lst_vers:
            #mdebug(lst_vers)
            #if len(lst_vers) > 4: Obj_system.remove_file(min(lst_vers)[1]) #os.system('rm %s'%min(lst_vers)[1])
            index = max(lst_vers)[0] + 1
        
        Obj_system.copy_file(loc_path + os.sep + file_name, loc_path+os.sep+file_wo_padding+'.'+str(index)+'.'+file_ext)
    else:
        raise Exception('not yet')

class os_platform(object):
    def __init__(self,*args):
        self.name = ''
    
    def get_local_path(self):
        return None
    
    def get_alt_tmp_path(self):
        return None
    
    def get_home(self):
        return None    

    def get_locale(self):
        return None

    def get_tmp_path(self):
        return None
    
    def get_user_name(self):
        return None
    
    def sys_open_document(self,item):
        return None
    
    def mk_link(self,src,dst):
        return None
    
    def copy_resolved(self,src,dst):
        return None
    
    def copy_file(self,src,dst):
        return None
    
    def get_log_path(self):
        return None
    
    def remove_file(self,src):
        return None
    
    def chmod(self,perm,src):
        return None
    
    def sudo_cp(self,src,dst,usr):
        return None
    
    def sudo_chmod(self,mod,src):
        return None
    
    def chmod_R(self,mod,src):
        return None
    
    def chown_R(self,mode,src):
        return None
        
class os_Windows(os_platform):
    def __init__(self,*args):
        os_platform.__init__(self,args)
        import win32file
        import win32api
        from win32com.shell import shell, shellcon
        self.w32 = win32file
        self.w32api = win32api
        self.shell = shell
        self.shellcon = shellcon
    
    def get_tmp_path(self):
        return 'C:\\Windows\Temp'
    
    def get_local_path(self):
        return os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + os.sep + JOB_LOCAL

    def get_home(self):
        return os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')   

    def get_locale(self):
        return 'English_United States.1252'
    
    def get_user_name(self):
        return os.getenv('USERNAME')
    
    def sys_open_document(self,item):
        subprocess.Popen('start %s'%item,  shell=True, stdout=subprocess.PIPE, )
    
    def get_log_path(self):
        return 'C:\\'
    
    def copy_file(self,src,dst):

        shutil.move(src, dst)
        try:
            shutil.copy2(src, dst)
        except:
            pass
        #src = self.w32api.GetShortPathName(src)
        #dst = self.w32api.GetShortPathName(dst)
        #os.system ('xcopy "%s" "%s"' % (src, dst))
        #self.shell.SHFileOperation(0, self.shellcon.FO_COPY, src, dst, 0, None, None)
        #self.w32.CopyFile (src, dst, 0)
        return True
    
    def remove_file(self,src):
        os.system('del "%s"'%src)
        return True
    
    def sudo_cp(self,src,dst,usr):
        shutil.copy(src, dst)
        
class os_Microsoft(os_Windows):
    def __init__(self,*args):
        os_Windows.__init__(self,args)
        
class os_Linux(os_platform):
    def __init__(self,*args):
        os_platform.__init__(self,args)
    
    def get_tmp_path(self):
        return '/tmp'
    
    def get_alt_tmp_path(self):
        return '/var/tmp'
    
    def get_local_path(self):
        return os.getenv('HOME')   + os.sep + JOB_LOCAL

    def get_home(self):
        return os.getenv('HOME') 

    def get_locale(self):
        return 'C'

    def get_user_name(self):
        return commands.getoutput("whoami")
    
    def sys_open_document(self,item):
        if not os.path.exists(str(item)): 
            mdebug.error('Object not found: %s'%str(item))
        (r,w,e) = popen2.popen3('xdg-open %s'%item)
        try:
            comments = r.readlines()
        except Exception, e:
            mdebug.error(str(e))
            
        #os.system('xdg-open %s'%item)
    
    def mk_link(self,src,dst):
        os.system('ln -sf %s %s'%(src,dst))
        return True
    
    def copy_resolved(self,src,dst):
        copyCommand = "cp --preserve=timestamps -r -L %s %s" % (src,dst)
        os.system(copyCommand)
        return True
    
    def get_log_path(self):
        return '/usr/pipeline/log'
    
    def copy_file(self,src,dst):
        os.system ("cp %s %s" % (src, dst))
        return True
    
    def remove_file(self,src):
        os.system('rm %s'%src)
        return True
    
    def chmod(self,perm,src):
        os.system('chmod %s %s'%(perm,src))
        
    def chmod_R(self,perm,src):
        os.system('chmod -R %s %s'%(perm,src))
        
    def    chown_R(self,mode,src):
        os.system('chmod %s -R %s'%(mode,src))
    
    def sudo_cp(self,src,dst,usr):
        (r,w,e) = popen2.popen3("/usr/bin/sudo -u %s /usr/pipeline/bin/sudo/tfxcp %s %s"%(usr,src,dst))
        comments = r.readlines()
        errors = e.readlines()
        if errors:
            mdebug.error('\n'.join(errors))    
            raise Exception(repr('Sudo error %s'%' '.join(errors))) 
    
    def sudo_chmod(self,mod,src):
        (r,w,e) = popen2.popen3("/usr/bin/sudo /usr/pipeline/bin/sudo/tfxrm %s"%(src))
        comments = r.readlines()
        errors = e.readlines()
        if errors:
            mdebug.error('\n'.join(errors))    
            raise Exception(repr('Sudo error %s'%' '.join(errors)))
            
class os_Darwin(os_Linux):
    def __init__(self,*args):
        os_Linux.__init__(self,args)
    
    def copy_resolved(self,src,dst):
        copyCommand = "cp -r -p -L %s %s" % (src,dst)
        os.system(copyCommand)
        return True
    
    def sudo_cp(self,src,dst,usr):
        (r,w,e) = popen2.popen3("/usr/bin/sudo -u %s /usr/pipeline/bin/sudo/tfxcp %s %s"%(usr,src,dst))
        comments = r.readlines()
        errors = e.readlines()
        if errors:
            mdebug.error('\n'.join(errors))    
            #raise Exception(repr('Sudo error %s'%' '.join(errors)))
    
def get_icons_path():
    return os.getenv(ENVS[3])

def get_repository():
    return os.getenv(ENVS[0])

def get_pythonpath():
    return os.getenv(ENVS[1])

def get_out_dailies():
    return os.getenv(ENVS[2])

def get_program_path():
    return os.getenv('PROGRAM_PATH')
##
#@var MODEL 
#Name folder which contained models
#   
MODEL = 'model'
##
#@var RIG 
#Name folder which contained rigs
#   
RIG = 'rig'
##
#@var TEXTURES 
#Name folder which contained textures
#   
TEXTURES = 'textures'
ANIM = 'anim'
ANIMATION = 'animation'
COMP = 'comp'
FX = 'fx'
LIGHT = 'light'
ASSETS = 'assets'
DATA = 'data'
SEQUENCE = 'sequences'
SHOTS = 'shots'
FILM = 'film'
MATTEPAINT = 'mattepaint'
DOC = 'doc'
REF = 'ref'
SRC = 'src'
PREVIZ = 'previz'
OUT = 'out'
PROXY = 'proxy'
SETTING = 'datafile'
SEQUENCE_DEFAULT = 'SQ01'
SEQUENCE_DATA = 'datasequence'
SET = 'set'
LAYOUT = 'layout'
STATIC = 'static'
TRACKS = 'tracks'
RENDER = 'render'
GEO = 'geo'
CACHE = 'cache'
MOVE = 'move'
SUBMIT = 'submit'
SAVE = 'save'
MIPROXY = 'miproxy'
DB_SEPARATOR_PATH = '/'
CHECKIN = 'checkin'
MATERIALS = 'materials'
FOOTAGES = 'footages'

# Do you have any idea? :)
MATERIALSMENTAL = 'materialsmental'
MATERIALSMAYA = 'materialsmaya'
MATERIALSHOUDINI = 'materialshoudini'
MATERIALS3DLIGHT = 'materials3dlight'

RENDER_SUCCESS = 'render_success'
TEMP = 'temp'
DAILIES = 'dailies'
PUBLISH = 'publish'
OBJ = 'obj'

TYPE_OF_ASSETS = [MODEL,RIG,TEXTURES,LIGHT,LAYOUT,SET,STATIC,COMP,FX,ANIM,MATTEPAINT]

######## TYPE_OF_EVENTS
TYPE_OF_EVENTS = [MOVE,SUBMIT,SAVE,RENDER,GEO,CACHE,CHECKIN,RENDER_SUCCESS,DAILIES]

#Add type of asset:
#SOMETYPE = 'sometype'
#add to database
#add class

class type_of_events(object):
    def __init__(self,*args):
        self.typ = ""
    
    def GetRenderData(self,*args):
        pass
    
    def StoreRenderData(self,*args):
        pass

class TOF_Meta_Class(object):
    def __new__(cls, mode):
        if 'TOF_' +mode in globals().keys():
            return globals()['TOF_' +mode]()
        else:
            return object.__new__(cls,mode)
            
    def __init__(cls,mode,parent=None):
        super(TOF_Meta_Class, cls).__init__(mode)
        setattr(cls, 'typ', mode)
    
    def GetRenderData(self,*args):
        pass
    
    def StoreRenderData(self,*args):
        pass

class TOF_submit(type_of_events):
    def __init__(self,*args):
        type_of_events.__init__(self,args)
        self.typ = SUBMIT
    
    def GetRenderData(self,*args):
        pass
    
    def StoreRenderData(self,*args):
        """param[in] args[0] folder full path
        param[in] args[1] ID event 
        param[in] args[2] folder 
        """
        if len(args) != 3: raise LenArgsError(len(args),3)
        file_name = 'render.xml'
        file_path = args[0] + os.sep + file_name
        id_event = str(args[1])
        store_path = args[2]
        name_render = ''

        if os.path.exists(file_path):
            xml = minidom.parse(file_path)
            xml.normalize()
            x2 = xml.createElement("item")
            x2.setAttribute("id", id_event)
            x3 = xml.createElement("folder")
            x3.appendChild(xml.createTextNode(str(store_path)))
            x2.appendChild(x3)
            xml.childNodes[0].appendChild(x2)
            os.remove(file_path)
        else:
            xml= minidom.Document()
            name_render = args[0].split(os.sep)[-1]
            x1 = xml.createElement("objects")
            x1.setAttribute("render", name_render)
            x2 = xml.createElement("item")
            x2.setAttribute("id", id_event)
            x3 = xml.createElement("folder")
            x3.appendChild(xml.createTextNode(str(store_path)))
            x2.appendChild(x3)
            x1.appendChild(x2)
            xml.appendChild(x1)
            
        fl = open(file_path, 'w')
        fl.write(xml.toxml())
        fl.close()
        
class TOF_render(type_of_events):
    def __init__(self,*args):
        type_of_events.__init__(self,args)
        self.typ = RENDER
    
    def StoreRenderData(self,*args):
        """param[in] args[0] folder full path
        param[in] args[1] ID event 
        param[in] args[2] folder 
        """
        if len(args) != 3: raise LenArgsError(len(args),3)
        
        file_name = 'render.xml'
        file_path = args[0] + os.sep + file_name
        id_event = str(args[1])
        store_path = args[2]
        name_render = ''
        #mdebug(file_path)
        if os.path.exists(file_path):
            xml = minidom.parse(file_path)
            xml.normalize()
            x2 = xml.createElement("item")
            x2.setAttribute("id", id_event)
            x3 = xml.createElement("folder")
            x3.appendChild(xml.createTextNode(str(store_path)))
            x2.appendChild(x3)
            xml.childNodes[0].appendChild(x2)
            os.remove(file_path)
        else:
            xml= minidom.Document()
            name_render = args[0].split(os.sep)[-1]
            x1 = xml.createElement("objects")
            x1.setAttribute("render", name_render)
            x2 = xml.createElement("item")
            x2.setAttribute("id", id_event)
            x3 = xml.createElement("folder")
            x3.appendChild(xml.createTextNode(str(store_path)))
            x2.appendChild(x3)
            x1.appendChild(x2)
            xml.appendChild(x1)
            
        if not os.path.exists(file_path): 
            print "Path not found ", file_path
            return
        fl = open(file_path, 'w')
        fl.write(xml.toxml())
        fl.close()

def get_tof_objects    (filepath):
    xml= minidom.parse(filepath)
    xml.normalize()
    data_dict = {}
    for node in xml.documentElement.getElementsByTagName('object'):
        if node.nodeType != 3:
            if node.attributes:
                for i in range(node.attributes.length):
                    a = node.attributes.item(i)
                    print a.name, a.value
            for subnode in  node.getElementsByTagName('item'):
                if subnode.nodeType != 3:
                    if subnode.attributes:
                        for i in range(subnode.attributes.length):
                            a = subnode.attributes.item(i)
                            print a.name, a.value
                print '-'*10, subnode
    return data_dict

def get_tof_events(filepath):
    #mdebug(filepath)
    xml= minidom.parse(filepath)
    xml.normalize()
    data_dict = {}
    for node in xml.documentElement.childNodes:
        if node.nodeType != 3:
            if node.attributes:
                for i in range(node.attributes.length):
                    a = node.attributes.item(i)
                    if a.name == "id": 
                        data_dict[a.value] = (get_item(node.getElementsByTagName('folder')[0].childNodes),)
    return data_dict
############################################################
class Assets_Meta_Class(object):
    def __new__(cls, mode):
        if 'A_' + mode in globals().keys():
            return globals()['A_' +mode]()
        else:
            return object.__new__(cls,mode)
            
    def __init__(cls,mode,parent=None):
        super(Assets_Meta_Class, cls).__init__(mode)
        setattr(cls, 'typ', mode)
    
    def path_data(self,name_seq=None,name_shot=None):
        seq = name_seq
        shot = name_shot
        path = FILM
        if seq != None and name_seq != '':
            path = path + os.sep + SEQUENCE + os.sep + seq
        if shot != None and shot != '':
            path = path + os.sep + SHOTS + os.sep + shot
        return path + os.sep + DATA
        
    def path_local(self,name_seq=None,name_shot=None):
        return os.path.join(FILM,ASSETS,self.typ)
    
    def path_publish(self,name_seq=None,name_shot=None):
        return self.path_data(name_seq,name_shot)
    
    def copy(self,src,dst):
        return None
    
    def template_path(self):
        return None
    
    def template_tags(self):
        return None
    
    def com_vers(self):
        return """mess = "<p align='center'>Load version <b>%s</b> asset?</p>"
reply = QMessageBox.question(self, "Browser", mess, QMessageBox.Yes|QMessageBox.No)
if reply == QMessageBox.Yes:
    self.exitApp('%s')"""

class assets(object):
    def __init__(self,*args):
        self.typ = ASSETS 
        self.data_outs = ['playblast']
    
    def path_data(self,name_seq=None,name_shot=None):
        seq = name_seq
        shot = name_shot
        path = FILM
        if seq != None and name_seq != '':
            path = path + os.sep + SEQUENCE + os.sep + seq
        if shot != None and shot != '':
            path = path + os.sep + SHOTS + os.sep + shot
        return path + os.sep + DATA
        
    def path_local(self,name_seq=None,name_shot=None):
        return os.path.join(FILM,ASSETS,self.typ)
    
    def path_publish(self,name_seq=None,name_shot=None):
        return self.path_data(name_seq,name_shot)
    
    def copy(self,src,dst):
        return None
    
    def template_path(self):
        return None
    
    def com_vers(self):
        return """mess = "<p align='center'>Load version <b>%s</b> asset?</p>"
reply = QMessageBox.question(self, "Browser", mess, QMessageBox.Yes|QMessageBox.No)
if reply == QMessageBox.Yes:
    self.exitApp('%s')"""

class materials(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = MATERIALS
    
    def path_local(self,name_seq=None,name_shot=None):
        """Return local path
        @todo If name_seq == None and If name_shot == None
        """
        seq = name_seq
        shot = name_shot
        return os.path.join(FILM,ASSETS,self.typ)
            
class model(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = MODEL
        
    def path_local(self,name_seq=None,name_shot=None):
        """Return local path
        @todo If name_seq == None and If name_shot == None
        """
        seq = name_seq
        shot = name_shot
        return os.path.join(FILM,ASSETS,self.typ)

class rig(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = RIG

class animation(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = ANIMATION

class fx(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = FX
        self.data_outs = [RENDER,'playblast']
    
    def path_local(self,name_seq=None,name_shot=None):
        """Return local path
        @todo If name_seq == None and If name_shot == None
        """
        seq = name_seq
        shot = name_shot
        if shot:
            return os.path.join(FILM,SEQUENCE,seq,SHOTS,shot,self.typ)
        else:
            return os.path.join(FILM,SEQUENCE,seq,self.typ)

class comp(fx):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = COMP
        self.data_outs = []
    
    def path_local(self,name_seq=None,name_shot=None):
        """Return local path
        @todo If name_seq == None and If name_shot == None
        """
        path = FILM
        if name_seq != None:
            path = path + os.sep + SEQUENCE + os.sep + name_seq
        if name_shot != None:
            path = path + os.sep + SHOTS + os.sep + name_shot
        return path + os.sep + COMP
    
    def template_path(self):
        #@todo: do over file path hard code
        return "/usr/pipeline/software/nuke/templates/comp.nk"
    
    def template_tags(self):
        return "abs,comp"
        
class anim(fx):
    def __init__(self,*args):
        fx.__init__(self,args)
        self.typ = ANIM
        self.data_outs = ['playblast']
        
class light(fx):
    def __init__(self,*args):
        fx.__init__(self,args)
        self.typ = LIGHT
        self.data_outs = [RENDER,'playblast']

class set(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = SET

class layout(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = LAYOUT

class static(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = STATIC

class sequences(assets):
    def __init__(self,*args):
        assets.__init__(self,args)
        self.typ = SEQUENCE
    
    def copy(self,src,dst):
        return True


class fs_template_object(object):
    def __init__(self,*args):
        self.typ = ""
    
    def getPath(self,*args):
        return None

class FS_Meta_Class(object):
    def __new__(cls, mode):
        if 'FS_' +mode in globals().keys():
            return globals()['FS_' +mode]()
        else:
            return object.__new__(cls,mode)
    
    def __init__(cls,mode,parent=None):
        super(FS_Meta_object, cls).__init__(mode)
        setattr(cls, 'typ', mode)
    
    def getPath(self,*args):
        return None
            
class FS_src(fs_template_object):
    def __init__(self,*args):
        fs_template_object.__init__(self,args)
        self.typ = SRC
    
class FS_shots(fs_template_object):
    def __init__(self,*args):
        fs_template_object.__init__(self,args)
        self.typ = SHOTS

    
PATHS_PROJECT = {MODEL:os.path.join(ASSETS,MODEL),
        RIG:os.path.join(ASSETS,RIG),
        TEXTURES:os.path.join(ASSETS,TEXTURES),
        ANIM:os.path.join(FILM)}

PATH_SHOT = [ANIM,COMP,FX,LIGHT,OUT,DATA,PROXY,SRC]

ASSETS_DIC = {
    ASSETS:{
        MATTEPAINT:{},
        MODEL:{},
        RIG:{},
        LIGHT:{},
        TEXTURES:{},
        STATIC:{},
        FOOTAGES:{}
    }
}

##
#@var CREATE_PRG_DIC 
#Folder structure for projects
#
CREATE_PRG_DIC = {
    FILM:{
        ASSETS:{
            MATTEPAINT:{},
            MODEL:{},
            RIG:{},
            LIGHT:{},
            TEXTURES:{},
            STATIC:{},
        },
        SEQUENCE:{},
        DATA:{
            PREVIZ:{},
            },
        COMP:{
            PREVIZ:{},
            },
        OUT:{
            PREVIZ:{},
            },
        },
    DOC:{},
    REF:{},
    SRC:{},
    OUT:{
        'dailies':{},
        'hires':{},
        },
    TEMP:{
        SRC:{},
        },
}


##
#@var CREATE_SEQ_DIC 
#Folder structure for sequences
#
CREATE_SEQ_DIC = {
    ASSETS:{
            MATTEPAINT:{},
            MODEL:{},
            RIG:{},
            TEXTURES:{},
            STATIC:{},
        },
    DATA:{
        RENDER:{},
        TRACKS:{},
        },
    FX:{},
    SHOTS:{},
    COMP:{},
    OUT:{},
}

##
#@var CREATE_SHOT_DIC 
#Folder structure for shots
#
CREATE_SHOT_DIC = {
    ANIM:{},
    FX:{},
    LIGHT:{},
    COMP:{},
    DATA:{
        RENDER:{},
        TRACKS:{},
        'shadowmap':{},
        'cache':{},
        'geo':{},
        },
    OUT:{ 
        'dailies':{},
        'hires':{},
    },
    SRC:{},
    PROXY:{},
}

def join_path(dic):
    """Return list which contained folders structure
    @param[in] dic The dictionary folder structure.
    """
    path = []
    for key in dic.keys():
        if len(dic[key].keys()) != 0:
            path.extend([key+os.sep+x for x in join_path(dic[key])])
        else:
            path.append(key)
    return path

def join_path_dict(dic):
    """Return dictionary which contained folders structure named at last name
    @param[in] dic The dictionary folder structure.
    @todo Implement function
    """
    path = {}
    for key in dic.keys():
        if len(dic[key].keys()) != 0:
            path.extend([key+os.sep+x for x in join_path(dic[key])])
        else:
            path.append(key)
    return path
    
###
# @var RIG_DIR 
# Directory assets rig
# @todo join_path_dict
# 
RIG_DIR = join_path(ASSETS_DIC)[3]
MODEL_DIR = join_path(ASSETS_DIC)[4]
LIGHT_DIR = join_path(ASSETS_DIC)[1]
STATIC_DIR  = join_path(ASSETS_DIC)[2]

CREATE_PRG = join_path(CREATE_PRG_DIC)

CREATE_SEQ = join_path(CREATE_SEQ_DIC)

CREATE_SHOT = join_path(CREATE_SHOT_DIC)

DIRS_REALFLOW = [
    'fx/realflow'
    ]

DIRS_MAYA_DICT = {
    LIGHT:{},
    FX:{
        MODE_MAYA:{},
        },
    RIG:{},
    MODEL:{},
    SET:{},
    LAYOUT:{},
    STATIC:{},
    ANIM:{},
    }

DIRS_HOUDINI_DICT = {
    ANIM:{},
    LIGHT:{},
    FX:{
        MODE_HOUDINI:{},
        },
    RIG:{}
    }

TYPES_SHOT = {MODE_MAX:[MODEL,RIG,ANIM,FX],
    MODE_MAYA:[MODEL,RIG,ANIM,FX],
    MODE_PHOTOSHOP:[TEXTURES],
    MODE_DEFAULT:[MODEL,RIG,ANIM],
    MODE_NUKE:[COMP]}

Obj_system = eval('os_%s()'%platform.system())

REPO = get_repository()
USERNAME = Obj_system.get_user_name()
LOCAL = Obj_system.get_local_path()
PYTHONPATH = get_pythonpath()
OUT_DAILIES = get_out_dailies()
ICONS_PATH = get_icons_path()
MAIN_LOCALE = Obj_system.get_locale()
PROGRAM_PATH = get_program_path()
USER_TMP = Obj_system.get_tmp_path()
USER_ALT_TMP = Obj_system.get_alt_tmp_path()
USER_HOME = Obj_system.get_home()
LOG_PATH = Obj_system.get_log_path()

def join_path_project():
    """Return path to folder FILM
    """
    return FILM

def join_path_sequence(name_new_sequence):
    """Return path to folder new sequence
    """
    path = os.path.join(FILM,SEQUENCE,name_new_sequence)
    return path

def get_path_shots(name_project, name_sequence):
    return os.path.join(name_project,FILM,SEQUENCE,name_sequence,SHOTS)
    #return path_sequence + os.sep + 'shots'

def get_path_sequence(name_project):
    return os.path.join(name_project,FILM,SEQUENCE)

def get_path_assets_project():
    return os.path.join(FILM,ASSETS,MODEL)

def join_path_shots(path_sequence):
    return path_sequence + os.sep + SHOTS

def join_path_shot(path_sequence, name_new_shot):
    return path_sequence + os.sep + SHOTS + os.sep + name_new_shot

def get_path_asset_light(path_asset):
    return path_asset.replace(MODEL,LIGHT)
    
def split_path_asset(path_asset):
    name_project = path_asset.split(FILM)[0]
    name_project = name_project[:-1].split(os.sep)[-1]
    name_sequence = path_asset.split(SEQUENCE)[-1]
    name_sequence =  name_sequence.split(os.sep)[0]
    return REPO, name_project, FILM, SEQUENCE, name_sequence

def delete_datafile(path):
    if os.path.exists(path + os.sep + SETTING):
        os.remove(path + os.sep + SETTING)

def set_settings(path, value):
    fl = open(path + os.sep + SETTING,'a')
    fl.write(str(value)+'\n')
    fl.close()

def get_settings(path):
    fl = open(path+ os.sep + SETTING,'r')
    values = []
    for line in fl:
        values.append(line.rstrip('\n'))
    return values

def get_current_project(file_name):
    """Return tuple (name, path)
    @param[in] file_name
    @todo Add all variable method need to this func.
    """
    return ('test_zzz','test_zzz',)

def resolve_path(path):
    """Return actual path in repository
    @param[in] path Full local path asset
    """
    info_path = path + '.info'
    if not os.path.exists(info_path): raise InfoNotFoundError(info_path)
    fl = open(info_path)
    infos = fl.readlines()
    return REPO+os.sep+infos[2].strip('\n')+infos[1].strip('\n')

def initialize_project(init_path_in_repository):
    """Return full path 
    @param[in] init_path_in_repository Path project w/o repository path.
    """
    for folder in CREATE_PRG:
        os.makedirs(REPO+os.sep+init_path_in_repository+os.sep+folder)
        
#    Obj_system.chown_R('1001:101',REPO+os.sep+init_path_in_repository)
#    Obj_system.chmod_R('777',REPO+os.sep+init_path_in_repository)

def initialize_sequence(local_path,name_sequence):
    """Return full path sequnce
    @param[in] local_path
    @param[in] name_sequence
    """
    mdebug(REPO+os.sep+local_path+os.sep+name_sequence)
    if os.path.exists(REPO+os.sep+local_path+os.sep+name_sequence): raise SequenceExists(name_sequence)
    for folder in CREATE_SEQ:
        os.makedirs(REPO+os.sep+local_path+os.sep+name_sequence+os.sep+folder)

def initialize_shot(local_path,name_shot):
    """Return full path shot
    @param[in] local_path
    @param[in] name_shot
    """
    #if not filesys.initialize_shot(self.proj_path+os.sep+self.relative_path,name): raise ShotDoesNotCreate(self.proj_path+os.sep+self.relative_path+os.sep+name)
    for folder in CREATE_SHOT:
        os.makedirs(REPO+os.sep+local_path+os.sep+name_shot+os.sep+folder)
        
def get_options(line_args_like,str_opt):
    """Return tuple contains dictionary, args
    @param[in] line_args_like String options like
    @param[in] str_opt 
    """    
    optlist, args = getopt.gnu_getopt(shlex.split(line_args_like), str_opt)
    return dict(optlist), args

def get_next_version_dir(dir_render_tmp,intpadding=4):
    """Return dir_render_tmp next tuple (string, string, int), = "/path/to/version/dir/0000", "0000", 0
    @param[in] dir_render_tmp /path/to/version/dir/
    @param[in] intpadding Padding for versions
    """
    padd_dir = 0
    padd = 0
    if os.path.exists(dir_render_tmp):
        padds = [int(y) for y in filter(lambda x: x.isdigit(), os.listdir(dir_render_tmp))]
        if padds:
            padds.sort()
            padd_dir = int(max(padds))
    padd_dir_tmp = padding(padd_dir,intpadding)
    dir_render = dir_render_tmp + os.sep + padd_dir_tmp
    # for maya skip TMP folder
    # if old path empty - return it
    lst_dir_render = []
    if os.path.exists(dir_render):
        lst_dir_render = os.listdir(dir_render)
        if len(lst_dir_render) == 1 and lst_dir_render[0] == 'tmp':
            return dir_render, padd_dir_tmp, padd_dir
        if not lst_dir_render: return dir_render, padd_dir_tmp, padd_dir
    # else return new version new folder
    padd_dir += 1
    padd_dir_tmp = padding(padd_dir,intpadding)
    dir_render = dir_render_tmp + os.sep + padd_dir_tmp
        
    return dir_render, padd_dir_tmp, padd_dir

class FilesObject():
    def __init__(self,path):
        self.__keys = []
        self.__dict = {}
        def append(value,path):
            self.__keys.append(value)
            self.__dict[value] = FileObject(path+os.sep+value)
        [append(x,path) for x in get_settings(path)]
    
    def values(self):
        return [self.__dict[key] for key in self.__keys]

    def keys(self):
        return self.__keys[:]

    def __getitem__(self, key):
        return self.__dict[key]
    
    def __str__(self):
        return ' '.join(self.__keys[:])

class FileObject():
    def __init__(self,path):
        split_path = path.rsplit(os.sep,1)
        self.ext = split_path[-1].split('.')[0]
        self.name = split_path[-1].rsplit('.',2)[0]
        self.vers = split_path[-1].rsplit('.',2)[-2]
        self.path = split_path[0]
        self.fullpath = path
    
    def get_name(self):
        return self.name 
    
    def get_version(self):
        return self.vers
    
    def set_version(self):
        pass

    def get_new_version(self):
        pass
    
    def push_datafile(self):
        pass
    
    def pop_datafile(self):
        pass
    
    def __str__(self):
        return (self.fullpath)

def get_xml(xml_file):
    xml_data = minidom.parse(xml_file)
    items = xml_data.getElementsByTagName('item')
    for item in items:
        print item.attributes['id'].value
        print get_item(item.getElementsByTagName('name')[0].childNodes)
        print get_item(item.getElementsByTagName('xform')[0].childNodes)
        
def get_item(list_nodes):
    #return ''.join([x.data for x in list_nodes if x == x.TEXT_NODE])
    rc = ''
    for node in list_nodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def GetRendersLatest(path):
    if not os.path.exists(path): raise Exception('Path "%s" not found.'%path)
    path = path + os.sep + RENDER
    file_xml = path + os.sep + 'render.xml'
    dirs_list = []
    if not os.path.exists(file_xml): return None
    xml_data = minidom.parse(file_xml)
    x0 = xml_data.getElementsByTagName('objects')[0]
    for node in x0.getElementsByTagName('object'):
        data = {}
        #node.getElementsByTagName('object').childNodes
        name_render = node.getAttribute("render")
        for item in node.getElementsByTagName('item'):
            name_item = item.getAttribute("name")
            data[name_item] = get_item(item.getElementsByTagName('folder')[0].childNodes)
        dirs_list.append((name_render,data))
        #print node.nodeName
    return dirs_list

def _storeRenderLatest(file_xml,dict_list):
    if not dict_list: return None
    xml= minidom.Document()
    x0 = xml.createElement("objects")
    for dict_dir in dict_list:
        x1 = xml.createElement("object")
        x1.setAttribute("render", dict_dir[0])
        dirs = dict_dir[1]
        for key in dirs.keys():
            x2 = xml.createElement("item")
            x2.setAttribute("name", key)
            x3 = xml.createElement("folder")
            x3.appendChild(xml.createTextNode(str(dirs[key])))
            x2.appendChild(x3)
            x1.appendChild(x2)
        x0.appendChild(x1)
    xml.appendChild(x0)
    fl = open(file_xml, 'w')
    fl.write(xml.toxml())
    fl.close()
    return dict_list

def _getRenders(path):
    IGNORE_FOLDER = ['tmp',]
    dir_dict = {}
    dirs = [x for x in os.listdir(path) if os.path.isdir(path+os.sep+x) and (x.isdigit())]
    for n in dirs:
        folders = [x for x in os.listdir(path+os.sep+n) if (os.path.isdir(path+os.sep+n+os.sep+x)) and (not x in IGNORE_FOLDER) ] 
        folders = [x for x in folders if not os.listdir(path+os.sep+n+os.sep+x) == []]
        for x in folders:
            dir_dict[x] = n
    return dir_dict

def GetAllRenderVersions(path):
    if not os.path.exists(path): raise Exception('Path "%s" not found.'%path)
    pat = re.compile(os.sep + '(\d{2,4})' + os.sep) 
    cur_vers = pat.search(path)
    if not cur_vers: return []
    cur_vers = cur_vers.group(1)
    start = path.split(os.sep+cur_vers+os.sep)[0]
    end = path.split(os.sep+cur_vers+os.sep)[1].split(os.sep,1)[0]
    all_version = [x for x in os.listdir(start) if x.isdigit()]
    ret = []
    for v in all_version:
        if os.path.exists(start + os.sep + v + os.sep + end):
            if os.listdir(start + os.sep + v + os.sep + end):
                ret.append(v)
    return start, end, ret
    
def UpdateRendersLatest(path):
    #if not os.path.exists(path): raise Exception('Path "%s" not found.'%path)
    if not os.path.exists(path): return None
    path = path + os.sep + RENDER
    if not os.path.exists(path): return None
    dirs = [x for x in os.listdir(path) if (os.path.isdir(path+os.sep+x))]
    dirs.sort()
    dirs_list = []
    for n in dirs:
        dir_dict = {}
        dir_dict = _getRenders(path+os.sep+n)
        dirs_list.append((n,dir_dict))
    
    
    
    file_xml = path + os.sep + 'render.xml'
    
    return _storeRenderLatest(file_xml,dirs_list)

def GetFolderSize(abs_path):
    folder_size = 0
    for (path, dirs, files) in os.walk(abs_path):
        for file in files:
            filename = os.path.join(path, file)
            sz = 0
            try:
                sz = os.path.getsize(filename)
            except:
                sz = 0
            folder_size += sz
    folder_size = folder_size/(1024*1024.0)
    return folder_size
