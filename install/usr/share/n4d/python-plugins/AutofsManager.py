import os
import tempfile
import re


class AutofsManager:
	
	def __init__(self):
		
		self.auto_master_dir="/etc/auto.master.d/"
		self.auto_master_options="--timeout 60"
		
		self.default_options="-rw,hard,intr,rsize=8192,wsize=8192,nosuid,nfsvers=3"
		self.default_dest="/net/server-sync/&"
		
	#def init
	
	
	def startup(self,options):
		
		pass
		
	#def startup
	
	
	def create_master_file(self,mount_dest,mount_script,options=None):

		try:
		
			if not os.path.exists(self.auto_master_dir):
				os.makedirs(self.auto_master_dir)
			
			if options==None:
				options=self.auto_master_options
			
			mount_dest=mount_dest.rstrip("/")
			dest_path=self.auto_master_dir+mount_dest.lstrip("/").rstrip("/").replace("/","_")+".autofs"
			data="%s\t%s\t%s\n"%(mount_dest,mount_script,options)
			
			fd, tmpfilepath = tempfile.mkstemp()
			new_export_file = open(tmpfilepath,'w')
			new_export_file.write(data)
			new_export_file.close()
			os.close(fd)
			
			os.rename(tmpfilepath,dest_path)
			
			return {"status": True, "msg": "autofs master.d file created"}
			
		except Exception as e:
			
			return {"status": False, "msg": str(e)}
		
		
	#def create_master_file
	
	
	def create_mount_script(self,mount_script_fname,subdir_dest,mount_source,options=None):

		try: 
			
			if options==None:
				options=self.default_options
				
			data="%s\t%s\t%s\n"%(subdir_dest,options,mount_source)
			
			fd, tmpfilepath = tempfile.mkstemp()
			new_export_file = open(tmpfilepath,'w')
			new_export_file.write(data)
			new_export_file.close()
			os.close(fd)
			
			os.rename(tmpfilepath,mount_script_fname)
		
			return {"status": True, "msg": "autofs mount script created"}
			
		except Exception as e:
			
			return {"status": False, "msg": str(e)}
		
	#def create_mount_script
	
	
#class AutofsManager

if __name__=="__main__":
	
	autofs=AutofsManager()
	
	autofs.create_master_file("/net/server-sync/","/etc/auto.nfs")
	autofs.create_mount_script("/tmp/auto.master.d/wawa","*","172.20.10.19:/net/server-sync/&")
	
