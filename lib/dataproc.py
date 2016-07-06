import os
import logging
import datetime as dt

from lib.myparser import sanitize_dir
from lib.myparser import is_hex_string16
from decla import Sensor, Base, Time, Register
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import event

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class dataproc():
	def __init__(self,_file):
		logger.info('__init__')
		self.__file = _file
		self.__fl = None
		self.__sql = sqlhelp()
		self.size = 0
		self.read = 0
		
		self.sensors = []
		
		
		#event.listen(Sensor,'after_insert',self._beford_insert_listener)
		#pass
	
	#def _beford_insert_listener(self,mapper, connection, target):
		#sensors.append(target)
		#print(target)
		pass
	
	def __iter__(self):
		return self
	
	def load(self):
		logger.info('upload')
		self.__sql.prepare()
		self.__fl = fileload(self.__file)
		self.size = self.__fl.get_size()
		
		
	def __next__(self): # Tiene que ser un iterador 
		
		line = self.__fl.next() 	
		if  line != "":
			self.__sql.add(line)
			self.read = self.__fl.get_data_read()
			#logger.info(str(self.read/self.size * 100))
		
		else:
			self.__sql.commit()
			raise StopIteration()
			logger.info('end upload')				
		
	def get_data(self,_id):# id de sensor
		
		return self.__sql.getdata(_id)
		pass

	def getSensorAll(self):
		
		for s in self.__sql.sensorAll():
			self.sensors.append(s)
		return self.sensors	
		
class sqlhelp():
	
		
	def __init__(self):
		
		self.i = 0
		self.engine = create_engine('sqlite:///db/dbobj.db')
		Base.metadata.bind = self.engine
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()
		
		pass
	
	def commit(self):
		#logger.debug("connect")
		#sqlhelp.conn = sqlite3.connect('db/data.db')
		self.session.commit()
		pass
		
	def prepare(self):
	
		Base.metadata.create_all(self.engine)
		Base.metadata.drop_all(self.engine)
		Base.metadata.create_all(self.engine)
		
		
	def add(self,_reg):
		
		
		#logger.info("Pre Try")
		try:
			
			_time = dt.datetime.strptime(_reg[0],'%Y-%m-%d %H:%M:%S') # convertir primer registro en timepos
			_reg.pop(0) # removemos el 0 que es el timepo
			obj_time = Time(value = _time) # Crea obj Timepo con el valor del tiempo
			
		
			self.session.add(obj_time)
			#session.commit()
			 
		except ValueError as e:
			logger.debug(e)
			
		#try:
		#logger.info("Pre for")
		for _part in _reg:
			if is_hex_string16(sanitize_dir(_part)) == True:
				_hw = sanitize_dir(_part)
				
				obj_sensor = self.session.query(Sensor).filter_by(hwdir = _hw).first()
				#logger.info("if")
				if obj_sensor is None:
					obj_sensor = Sensor(hwdir = _hw)
					self.session.add(obj_sensor)
					#session.commit()
			else:
				#logger.info("else")
				_temp = float(_part)
								
				obj_register = Register(value = _temp)
				obj_register.time = obj_time
				obj_register.sensor = obj_sensor
				
				self.session.add(obj_register)
				#logger.info(obj_register)
				#self.session.commit()
				pass
			
			if self.i == 1000:
				self.i = 0	
				self.session.commit()
			else:
				self.i = self.i + 1
		#except:
			
		pass
		
	def sensorAll(self):
		_list = []
		for s in self.session.query\
			(Sensor).all():
			_list.append(s)
		return _list
			
		#print(self.session.query(Register).join(Sensor).filter(Sensor.id == 1).count())
		
	pass
	
	def getdata(self,_id):
		li = []
		
		logger.info('call getdata')
		for r,s,t in self.session.query\
			(Register.value,Sensor.id,Time.value)\
			.filter(Sensor.id == Register.sensor_id)\
			.filter(Sensor.id == _id)\
			.filter(Register.time_id == Time.id).\
			all():
			tupla = [t,r]	
			li.append(tupla)
			
		return li

class fileload():
	
	def __init__(self,file):
		self.open = None
		self.f = file
		self.open = open(self.f, 'r')
		self._data_read = 0
	
	def get_data_read(self):
		return self._data_read
		
	def get_size(self):
		if self.f == '':
			return 0
		else:
			self.open.seek(0, os.SEEK_END)
			_s = self.open.tell()
			self.open.seek(0)
			return _s 
					
	def next(self):
		
		line = self.open.readline()
		
		if line != "":
			
			self._data_read += len(line)
			return line.rstrip('\n').split(';')
		
		else:
			self.open.close()
			return ""
			#raise StopIteration()		

