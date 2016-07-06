from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative  import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()




class Register(Base):
	""" Class  """
	__tablename__ = "register"
	
	sensor_id = Column(Integer, ForeignKey('sensor.id'), primary_key=True)
	time_id = Column(Integer, ForeignKey('time.id'), primary_key=True)
	value = Column(Float)

	sensor = relationship("Sensor", back_populates = "times")
	time = relationship("Time" ,back_populates = "sensors")
	
	
	def __repr__(self):
		return "<Register(value = '%5.2f')>" % self.value

	
class Sensor(Base):
	__tablename__ = 'sensor'
	id = Column(Integer, primary_key = True)
	hwdir = Column(String(16), nullable = False)
	times = relationship("Register",back_populates="sensor")
	
	def __repr__(self):
		return "<Sensor(id = %d, hwdir = %s)>" % (self.id,self.hwdir)


	
class Time(Base):
	__tablename__ = 'time'
	id = Column(Integer,primary_key = True)
	value = Column(DateTime(timezone = False))
	sensors = relationship("Register",back_populates="time")
	

#Sensor.time = relationship("Sensor", order_by = Sensor.id, back_populates = "time")
#Time.sensor = relationship("Time", order_by = Time.id, back_populates = "sensor")
#engine = create_engine('sqlite:///db/dbobj.db')
#Base.metadata.create_all(engine)

