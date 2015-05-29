#========Thomas June 2014
#
#	DESCRIPTION
#		This program permit to read the needed file directly in the #		supercomputer tupa!!!!!
#========

#===== Library
import paramiko

#===== User input
Username='fps8.thomas'
Servername='tupa.cptec.inpe.br'
Password='BvCY6J'
PublicKey='/home/.keys/users/martin.thomas/martin.thomas.crt'

#====== Connection to Tupa
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(Servername, username=Username, password=Password, key_filename=PublicKey)
sftp = ssh.open_sftp()


#====== open a file
#File = "/scratchin/projetos/fpsp0008/home/fps8.thomas/sim_140212/realexp/out300m_V2.2_netcdf"
#File = sftp.open(remote_file).read()

#open netcdf file

var = 'r300m.net036000'
var= 'r9km.bin039600'
#filename
LenDateFormat=6# length of the hours (date) format
Pref=var[0:(len(var)-LenDateFormat)] # Prefix of the file
Date=var[(len(var)-LenDateFormat):] # hours
filename=Pref+Date # complete file name
hour=Date # initializing counting

InputDirPath='/scratchin/projetos/fpsp0008/home/fps8.thomas/sim_140212/realexp/out9km/'

File=InputDirPath+filename

Data = sftp.open(File).read()






#############TRASH 

local_file_data=open(local_file, "rb").read()
sftp.stat(local_file)
remote_file_data = sftp.open('/scratchin/projetos/fpsp0008/home/fps8.thomas/testtupa').read()

#------- Execute command and see the results 
stdin, stdout, stderr = ssh.exec_command('uptime')
stdout.readlines()


ssh.stat()

sftp = ssh.open_sftp()
