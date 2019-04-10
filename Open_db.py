from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from loguru import logger

engine = create_engine('sqlite:///weather.db', echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
rtl = Base.classes.rtl_433
session = sessionmaker(bind=engine)
session = session()

class WeatherStationData(Base):
    __tablename__ = 'rtl_433'
    __table_args__ = {'autoload': True}

def loadSession(message):
        messageUnpacked = rtl(**message)
        session.add(messageUnpacked)
        session.commit()
        return session

def insertValue(session, person):
    pass

if __name__ == "__main__":
    #res = session.query(WeatherStationData).all()
    message = {'time': '2019-01-12 17:00:43', 'model': 'Fine Offset Electronics WH1080/WH3080 Weather Station', 'msg_type': 0, 'id': 50, 'temperature_C': 9.9, 'humidity': 65, 'direction_str': 'E', 'direction_deg': '90', 'speed': 4.896, 'gust': 8.568, 'rain': 407.4, 'battery': 'OK'}
    session = loadSession(message)
