from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///weather.db', echo=True)
Base = declarative_base()

from loguru import logger

########################################################################
class rtl(Base):
    """"""
    __tablename__ = "rtl_433"

    sequence = Column(Integer, autoincrement = True, primary_key=True)
    id = Column(Integer)
    time = Column(String)
    model = Column(String)
    msg_type = Column(String)
    temperature_C = Column(Float)
    humidity = Column(Integer)
    direction_str = Column(String)
    direction_deg = Column(Integer)
    speed = Column(Float)
    gust = Column(Float)
    rain = Column(Float)
    battery = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, time, model, msg_type, temperature, humidity, direction_str, direction_deg, speed, gust, rain, battery):
        """"""
        self.time = time
        self.model = model
        self.msg_type = msg_type
        self.temperature = temperature
        self.humidity = humidity
        self.direction_str = direction_str
        self.direction_deg = direction_deg
        self.speed = speed
        self.gust = gust
        self.rain = rain
        self.battery = battery

# create tables
Base.metadata.create_all(engine)