from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///weather.db', echo=False)
Base = declarative_base(engine)
from loguru import logger

class WeatherStationData(Base):
    __tablename__ = 'rtl_433'
    __table_args__ = {'autoload': True}

def loadSessionResults():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def returnTemp():
    session = loadSessionResults()
    restemperature_c = session.query(WeatherStationData.temperature_C).all()
    restemperature_cTime = session.query(WeatherStationData.time).all()
    restemperature_c = [value for value, in restemperature_c]
    restemperature_cTime = [item[0] for item in restemperature_cTime]
    '''
    for x in range(len(res)):
        #print(x)
        print(res[x].temperature_C,  ' ' , end='')
    '''
    # logger.info(restemperature_cTime)
    return(restemperature_c, restemperature_cTime)

def returnRain():
    session = loadSessionResults()
    # Return a List of items from the database
    resrain = session.query(WeatherStationData.rain).all()
    resrainTime = session.query(WeatherStationData.time).all()
    resrainData = [item[0] for item in resrain]
    resrainTimeData = [item[0] for item in resrainTime]
    #logger.info(resrainTimeData)
    return(resrainData, resrainTimeData)



if __name__ == "__main__":
    returnTemp()
    #res = session.query(WeatherStationData).all()

    #message = {'time': '2019-01-12 17:00:43', 'model': 'Fine Offset Electronics WH1080/WH3080 Weather Station', 'msg_type': 0, 'id': 50, 'temperature_C': 9.9, 'humidity': 65, 'direction_str': 'E', 'direction_deg': '90', 'speed': 4.896, 'gust': 8.568, 'rain': 407.4, 'battery': 'OK'}
    #session = loadSession(message)
