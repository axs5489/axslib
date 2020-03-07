from ctypes import *

__all__ = [ 'Adu2xx' ]

_AduHidDll = WinDLL('H:\Python\l3hlib\Instruments\AduHidTest64\AduHid64.dll')


#void * __stdcall OpenAduDevice(unsigned long iTimeout);
_OpenAduDevice_Proto = WINFUNCTYPE(c_void_p,c_ulong)
_OpenAduDevice_Params = ((1,'iTimeout',1),)
_OpenAduDevice = _OpenAduDevice_Proto(
    ('OpenAduDevice',_AduHidDll),
    _OpenAduDevice_Params)

#void * __stdcall OpenAduDeviceByProductId(int iProductId, 
#                                          unsigned long iTimeout);
_OpenAduDeviceById_Proto = WINFUNCTYPE(c_void_p,c_int,c_ulong)
_OpenAduDeviceById_Params = (
    (1,'iProductId',0),
    (1,'iTimeout',1))
_OpenAduDeviceById = _OpenAduDeviceById_Proto(
    ('OpenAduDeviceByProductId',_AduHidDll),
    _OpenAduDeviceById_Params)

#void * __stdcall OpenAduDeviceBySerialNumber(const char* psSerialNumber,
#                                             unsigned long iTimeout);
_OpenAduDeviceBySN_Proto = WINFUNCTYPE(c_void_p,c_char_p,c_ulong)
_OpenAduDeviceBySN_Params = (
    (1,'psSerialNumber',0),
    (1,'iTimeout',1))
_OpenAduDeviceBySN = _OpenAduDeviceBySN_Proto(
    ('OpenAduDeviceBySerialNumber',_AduHidDll),
    _OpenAduDeviceBySN_Params)
    
#int __stdcall ReadAduDevice(void * hDevice, 
#                   void * lpBuffer, 
#                   unsigned long nNumberOfBytesToRead,
#                   unsigned long * lpNumberOfBytesRead,
#                   unsigned long iTimeout);
_ReadAduDevice_Proto = WINFUNCTYPE(
    c_int,
    c_void_p,
    c_void_p,
    c_ulong,
    POINTER(c_ulong),
    c_ulong)
_ReadAduDevice_Params = (
    (1,'hDevice',0),
    (1,'lpBuffer',0),
    (1,'nNumberOfBytesToRead',0),
    (1,'lpNumberOfBytesRead',0),
    (1,'iTimeout',0))
_ReadAduDevice = _ReadAduDevice_Proto(
    ('ReadAduDevice',_AduHidDll),
    _ReadAduDevice_Params)

#int __stdcall WriteAduDevice(void * hDevice, 
#                   const void * lpBuffer, 
#                   unsigned long nNumberOfBytesToWrite,
#                   unsigned long * lpNumberOfBytesWritten,
#                   unsigned long iTimeout);
_WriteAduDevice_Proto = WINFUNCTYPE(
    c_int,
    c_void_p,
    c_void_p,
    c_ulong,
    POINTER(c_ulong),
    c_ulong)
_WriteAduDevice_Params = (
    (1,'hDevice',0),
    (1,'lpBuffer',0),
    (1,'nNumberOfBytesToWrite',0),
    (1,'lpNumberOfBytesWritten',0),
    (1,'iTimeout',0))
_WriteAduDevice = _WriteAduDevice_Proto(
    ('WriteAduDevice',_AduHidDll),
    _WriteAduDevice_Params)

#void __stdcall CloseAduDevice(void * hDevice);
_CloseAduDevice_Proto = WINFUNCTYPE(None,c_void_p)
_CloseAduDevice_Params = ((1,'hDevice',0),)
_CloseAduDevice = _CloseAduDevice_Proto(
    ('CloseAduDevice',_AduHidDll),
    _CloseAduDevice_Params)


class Adu2xx(object):
    def __init__(self,sn=None,prod_id=None,read_timeout=1,write_timeout=1):
        super(Adu2xx,self).__init__()
        self._read_timeout = read_timeout
        self._write_timeout = write_timeout
        if sn != None:
            print("sn!",sn)
            self._handle = _OpenAduDeviceBySN(c_char_p(sn.encode('utf-8')),c_ulong(1))
            print("self.handle", self._handle)
        elif prod_id != None:
            print("prod_id!",prod_id)
            self._handle = _OpenAduDeviceById(c_int(prod_id),c_ulong(1))
        else:
            self._handle = _OpenAduDevice(c_ulong(1))
        
    def __del__(self):
        self.close()
    
    def close(self):
        if self._handle:
            _CloseAduDevice(c_void_p(self._handle))
            self._handle = None
            
    def get_write_timeout(self):
        return self._write_timeout 
        
    def set_write_timeout(self,x):
        self._write_timeout = x

    def get_read_timeout(self):
        return self._read_timeout 
        
    def set_read_timeout(self,x):
        self._read_timeout = x
        
    def read(self):
        if not self._handle:
            return None
        h = c_void_p(self._handle)
        buf = create_string_buffer('\0' * 9)
        bufLen = c_ulong(8)
        nRead = c_ulong(0)
        iTimeout = c_ulong(int(self._read_timeout * 1000 + 0.5))
        _ReadAduDevice(h,buf,bufLen,byref(nRead),iTimeout)
        return buf.value
        
    def write(self,msg):
        if not self._handle:
            print("_WriteAduDevice FAILED no _handle")
            return 0
        assert len(msg) <= 7, \
            'Device only supports messages of 7 or fewer characters'
        h = c_void_p(self._handle)
        buffer = c_char_p(msg.encode('utf-8'))
        nWrite = c_ulong(len(msg))
        nWritten = c_ulong(0)
        iTimeout = c_ulong(1000)
        rtn = _WriteAduDevice(h,buffer,nWrite,byref(nWritten),iTimeout)
        if(rtn == 0) :
            print("_WriteAduDevice FAILED::::",rtn)
        return rtn
    
    def k0_open(self):
        return self.write('RK0')

    def k0_close(self):
        return self.write('SK0')

    def k1_open(self):
        return self.write('RK1')

    def k1_close(self):
        return self.write('SK1')

    def k2_open(self):
        return self.write('RK2')

    def k2_close(self):
        return self.write('SK2')

    def k3_open(self):
        return self.write('RK3')

    def k3_close(self):
        return self.write('SK3')

    def k4_open(self):
        return self.write('RK4')

    def k4_close(self):
        return self.write('SK4')

    def k5_open(self):
        return self.write('RK5')

    def k5_close(self):
        return self.write('SK5')

    def k6_open(self):
        return self.write('RK6')

    def k6_close(self):
        return self.write('SK6')

    def k7_open(self):
        return self.write('RK7')

    def k7_close(self):
        return self.write('SK7')
        