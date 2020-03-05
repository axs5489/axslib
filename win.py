import sys
import ctypes
import glob
import serial
from serial.serialutil import SerialException
import shutil
import time
import win32api

def listSerialPorts():
	""" Cross-platform available serial port lister """
	if sys.platform.startswith('win'):
		ports = ['COM' + str()]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else: raise EnvironmentalError('Unsupported platform')
	
	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, SerialException):
			print("")
	return result
	
def driveReady(drive):
	""" Validates a drive """
	returnValue = 0
	oldError = win32api.SetErrorMode(1)
	try:
		win32api.GetVolumeInformation(drive)
	except:
		returnValue = 0
	else:
		returnValue = 1
	
	win32api.SetErrorMode(oldError)
	return returnValue

def getDrives():
	""" Generates a list of volume drives """
	# Generate list of active drive letters
	drives = win32.GetLogicalDriveStrings().split('\000')[:-1]
	
	list = [drive for drive in drives if driveReady(drive)] # Parse drives and return list of volume names
	return list

def getDriveVolumeName(driveLetter):
	""" Returns the volume name for a given drive letter, 'E://' """
	volumeNameBuffer = ctypes.create_unicode_buffer(1024)
	filesystemNameBuffer = ctypes.create_unicode_buffer(1024)
	serial = None
	max_component_len = None
	file_system_flags = None
	rc = ctypes.windll.kernel32.GetVolumeInformationW(ctypes.c_wchar_p(driveLetter),
		volumeNameBuffer, ctypes,sizeof(volumeNameBuffer),
		serial, max_component_len, file_system_flags,
		filesystemNameBuffer, ctypes,sizeof(filesystemNameBuffer)
	)
	return volumeNameBuffer

def findDrive(search, timeout=20):
	""" Basic search of drives by name """
	for retries in range(1,timeout):
		for drive in getDrives():
			volume = getDriveVolumeName(drive)
			if(volume.find(search)) :
				return drive
		time.sleep(1)
	return -1

def copyFile(src,dst):
	""" Copies a file from src to base directory of dst drive """
	if(dst not in getDrives()) : dst = findDrive(dst)
	if(dst in getDrives()) :
		src = os.path.normpath(src)
		dir,file = os.path.split(src)
		if file : shutil.copyfile(src,os.path.join(dst,file))
		return 1
	return 0

def transferFile(src,dst,filename):
	""" Copy file from drive to PC filesystem """
	if(src not in getDrives()) : src = findDrive(src)
	if(src in getDrives()) :
		try:
			dir,tail = os.path.split(dst)
			shutil.copyfile(os.path.join(src,filename),os.path.join(dir,filename))
			return 1
		except:
			print("File not found")
			return 0
	else: print("Drive not found")
	return -1
