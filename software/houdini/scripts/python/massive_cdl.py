###################################################################################
# 
import re
import os
import filesys
reload(filesys)

###################################################################################
# CDL Material
###################################################################################
# Materials patterns
pat = re.compile(r"^material\s(.+?)\n((?:.+\n)+)",re.MULTILINE)
# work shaders
pat_shader = re.compile(r"\"(.+?)(?:\")")
pat_shader_overrides = re.compile(r"\s\"([^\"].+?)\"\s((?:.[^\[]+\]))")
pat_shader_ovveride_value = re.compile(r"\[(.+)\]")
###################################################################################
class CDL_Material(object):
    def __init__(self,name,body,*args):
		self.name = name
		body = body.replace('\t','    ')
		body_dict = [x[4:] for x in body.split('\n') if len(x) > 4]
		try:
			body_dict = filter(lambda x: len(x.split(' ', 1)) > 1, body_dict)
			self.params = params = dict([x.split(' ', 1) for x in body_dict if x])
		except:
			print body_dict
			raise Exception("Error figure out with dictionary")
		self.__dict = {}
		self.__old_dict = {}
		self.__keys = []
		for key in params.keys():
		    self.__keys.append(key)
		    o = MaterialStatementsMeta(key,params[key])
		    o1 = MaterialStatementsMeta(key,params[key])
		    self.__dict[key] = o
		    self.__old_dict[key] = o1
    
    def values(self):
        return [self.__dict[key] for key in self.__keys]
    
    def keys(self):
        return self.__keys[:]

    def __setitem__(self, key, value):
    	if not key in self.__keys:
    		self.__keys.append(key)
        self.__dict[key] = value
    
    def __getitem__(self, key):
        return self.__dict[key]
        
    def get_loaded(self):
        ret = 'material ' + self.name + '\n'
        for k in self.__keys:
            ret += str(self.__old_dict[k]) + '\n'
        return ret
    
    def __str__(self):
        ret = 'material ' + self.name + '\n'
        for k in self.__keys:
            ret += str(self.__dict[k]) + '\n'
        return ret

# Default statement classes
class MaterialStatementsMeta(object):
    def __new__(cls, statement_name, value):
        if 'MaterialStatement_' + statement_name in globals().keys():
            return globals()['MaterialStatement_' +statement_name](value)
        else:
            class MS(object):
                def __init__(self,statement_name,value):
                    self.name = statement_name
                    self.body = value
                def __str__(self):
                    return '    ' + self.name + ' ' + self.body
          
            obj = type('MaterialStatement_' + statement_name ,
                       (MS,),
                       {'__init__': MS.__init__, '__str__': MS.__str__})
            return obj(statement_name,value)

# Override statement classes
class MaterialStatement_shader(object):
    def __init__(self,param_str):
        param_shader = param_str.split(' ', 1)
        to_shader = [param_shader[0]]
        for m in pat_shader.finditer(param_shader[1]):
            to_shader.append(m.groups(0)[0])
        to_shader = to_shader[:3]
        
        overrides = param_shader[1].split(to_shader[2])[1]
        dict_overrides = {}
        for m in pat_shader_overrides.finditer(overrides[1:]):
            name, value = m.groups()
            found_values = pat_shader_ovveride_value.search(value)
            if not found_values:
                print "Error! In %s value not found!" % name
                continue
            dict_overrides.update({name:found_values.groups(0)[0]})
        del m
        to_shader.append(dict_overrides)
        self.index = to_shader[0]
        self.renderpass = to_shader[1]
        self.shader_name = to_shader[2]
        self.overrades = dict_overrides

    def __str__(self):
        overrades = ''
        for key in self.overrades.keys():
            overrades +=' "%s" [%s]'%(key, self.overrades[key])
        return '    shader %s "%s" "%s" %s'%(self.index,self.renderpass,self.shader_name, overrades)
###################################################################################
# CDL Geometry
pat_geo = re.compile(r"^geometry\s(.+?)\n((?:.+\n)+)",re.MULTILINE)
class CDL_Geometry(object):
	def __init__(self,name,body,*args):
	    self.name = name
	    body = body.replace('\t','    ')
	    body_dict = [x[4:] for x in body.split('\n') if len(x) > 4]
	    try:
	    	body_dict = filter(lambda x: len(x.split(' ', 1)) > 1, body_dict)
	    	self.params = params = dict([x.split(' ', 1) for x in body_dict if x])
	    except:
	    	print body_dict
	    	raise Exception("Error figure out with dictionary")
	    self.__dict = {}
	    self.__old_dict = {}
	    self.__keys = []
	    for key in params.keys():
	        self.__keys.append(key)
	        o = MaterialStatementsMeta(key,params[key])
	        o1 = MaterialStatementsMeta(key,params[key])
	        self.__dict[key] = o
	        self.__old_dict[key] = o1
    
	def values(self):
	    return [self.__dict[key] for key in self.__keys]
	
	def keys(self):
	    return self.__keys[:]
	
	def __setitem__(self, key, value):
		if not key in self.__keys:
			self.__keys.append(key)
		self.__dict[key] = value
	
	def __getitem__(self, key):
	    return self.__dict[key]
	    
	def get_loaded(self):
	    ret = 'geometry ' + self.name + '\n'
	    for k in self.__keys:
	        ret += str(self.__old_dict[k]) + '\n'
	    return ret
	
	def __str__(self):
	    ret = 'geometry ' + self.name + '\n'
	    for k in self.__keys:
	        ret += str(self.__dict[k]) + '\n'
	    return ret

# Default statement classes
class GeometryStatementsMeta(object):
    def __new__(cls, statement_name, value):
        if 'GeometryStatement_' + statement_name in globals().keys():
            return globals()['GeometryStatement_' +statement_name](value)
        else:
            class MS(object):
                def __init__(self,statement_name,value):
                    self.name = statement_name
                    self.body = value
                def __str__(self):
                    return '    ' + self.name + ' ' + self.body
          
            obj = type('GeometryStatement_' + statement_name ,
                       (MS,),
                       {'__init__': MS.__init__, '__str__': MS.__str__})
            return obj(statement_name,value)

###################################################################################

###################################################################################
# CDL Cloth
pat_cloth = re.compile(r"^cloth\s(.+?)\n((?:.+\n)+)",re.MULTILINE)
class CDL_Cloth(object):
	def __init__(self,name,body,*args):
	    self.name = name
	    body = body.replace('\t','    ')
	    body_dict = [x[4:] for x in body.split('\n') if len(x) > 4]
	    try:
	    	body_dict = filter(lambda x: len(x.split(' ', 1)) > 1, body_dict)
	    	self.params = params = dict([x.split(' ', 1) for x in body_dict if x])
	    except:
	    	print body_dict
	    	raise Exception("Error figure out with dictionary")
	    self.__dict = {}
	    self.__old_dict = {}
	    self.__keys = []
	    for key in params.keys():
	        self.__keys.append(key)
	        o = MaterialStatementsMeta(key,params[key])
	        o1 = MaterialStatementsMeta(key,params[key])
	        self.__dict[key] = o
	        self.__old_dict[key] = o1
    
	def values(self):
	    return [self.__dict[key] for key in self.__keys]
	
	def keys(self):
	    return self.__keys[:]
	
	def __setitem__(self, key, value):
		if not key in self.__keys:
			self.__keys.append(key)
		self.__dict[key] = value
	
	def __getitem__(self, key):
	    return self.__dict[key]
	    
	def get_loaded(self):
	    ret = 'cloth ' + self.name + '\n'
	    for k in self.__keys:
	        ret += str(self.__old_dict[k]) + '\n'
	    return ret
	
	def __str__(self):
	    ret = 'cloth ' + self.name + '\n'
	    for k in self.__keys:
	        ret += str(self.__dict[k]) + '\n'
	    return ret

# Default statement classes
class ClothStatementsMeta(object):
    def __new__(cls, statement_name, value):
        if 'ClothStatement_' + statement_name in globals().keys():
            return globals()['ClothStatement_' +statement_name](value)
        else:
            class MS(object):
                def __init__(self,statement_name,value):
                    self.name = statement_name
                    self.body = value
                def __str__(self):
                    return '    ' + self.name + ' ' + self.body
          
            obj = type('ClothStatement_' + statement_name ,
                       (MS,),
                       {'__init__': MS.__init__, '__str__': MS.__str__})
            return obj(statement_name,value)
###################################################################################
# CDL Variable
pat_variable = re.compile(r'(?<=variable\s)(.+)')
pat_range = re.compile(r'(?<=\[)(.+)(?=\])')
class CDL_Variable(object):
	def __init__(self,name,body=None,*args):
		self.name = name
		self.body = None
		self.__default, self.__min, self.__max = 0.0000, 0.0000, 0.0000
		if body:
			self.__min, self.__max = pat_range.search(body).group(0).split(' ')
			self.__min = float(self.__min)
			self.__max = float(self.__max)
			self.body = body.split(" ")
			self.__default = (len(self.body) > 0 and float(self.body[1]) or 0)
	
	def setMin(self,value):
		self.__min = value
	
	def setMax(self,value):
		self.__max = value
	
	def setDefault(self,value):
		self.__default = value
	
	def getSubMask(self):
		return '%f [%f %f'%(self.__default,self.__min, self.__max)
	
	def getMin(self):
		return self.__min
	
	def getMax(self):
		return self.__max
	
	def getDefault(self):
		return self.__default 
	
	def __str__(self):
		ret = '		variable %s %f [%f %f]'%(self.name,self.__default,self.__min, self.__max)
		if not self.body: return ret
		if len(self.body) > 4:
			ret += ' ' + ' '.join(self.body[4:])
		return  ret
###################################################################################

class MassiveCDL(object):
    def __init__(self,*args):
        #Example work with geometry CDL statements
        self.geometries = {}
        self.materials = {}
        self.clothes = {}
        self.variables = {}
        self.__buffer = ''
        self.__replaces = []
        self.__file_path = ''
        
        
    def open(self,file_path):
        self.__file_path = file_path
        fl = open(file_path,'r')
        self.__buffer = fl.read()
        fl.close()
        
        # Fill Materials
        for match in pat.finditer(self.__buffer):
            title, body = match.groups()
            self.materials['material ' + title] = CDL_Material(title,body)
        
        # Fill Geometry
        for match in pat_geo.finditer(self.__buffer):
           title, body = match.groups()
           self.geometries['geometry ' + title] = CDL_Geometry(title,body)
   		
   		# Fill Cloth
        for match in pat_cloth.finditer(self.__buffer):
           title, body = match.groups()
           self.clothes['cloth ' + title] = CDL_Cloth(title,body)
          
        # Fill Variables
        for m in pat_variable.finditer(self.__buffer):
			txt = m.groups(0)[0]
			temp = txt.split(" ")
			self.variables[temp[0]] = CDL_Variable(temp[0], txt)
    
    def save(self,other=None):
		if not os.path.exists(self.__file_path): raise Exception("File does not excist")
		buff = self.__buffer
		# Replace materials
		for key in self.materials.keys():
			rep_pat = re.compile(r"^material\s" + '\s'.join(key.split(" ")[1:]) + r"\n((?:.+\n)+)",re.MULTILINE)
			buff = rep_pat.sub(str(self.materials[key]),buff)
		
		# Replace geometries
		#...
		    
		# Replace variables
		# Replace only for default, min, max
		for key in self.variables.keys():
			pat_variable2 = re.compile("(?<=variable\s"+ key  +"\s)(.+)(?=\])")
			buff = pat_variable2.sub(self.variables[key].getSubMask(),buff)
		# Write file
		
		#Create backup
		path, file_name = self.__file_path.rsplit(os.sep,1)
		#filesys.file_new_version(path, file_name)
		
		#Write
		file_name = self.__file_path
		if other: file_name = other
		fl = open(file_name,'w')
		fl.write(buff)
		fl.close()
    

###################################################################################
# Example usage with replaces materials statements
###################################################################################
#file_path = '/mnt/karramba/research/massive/crowd01/agent/_man_v02.cdl'

"""
CDL = MassiveCDL()
CDL.open(file_path)


for key in CDL.materials.keys():
    CDL.materials[key]['shader'].overrades['string colorMap'] = '/mnt/karramba/'

CDL.save()
"""



 
 
 
 
 
 