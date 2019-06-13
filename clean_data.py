from loguru import logger

logger.info("In clean_data ")

class Clean:
    def __init__(self):
        pass

    def massage(self, output, counter):
        global returnDict
        output = output.strip()
        data = output.replace('\t', '')
        data = data.split(" ")

        # The first line of 11 from the sensor contains WH1080/WH3080
        if ('WH1080/WH3080') in data:
            counter = 12
            valueWeather = {}
        if counter > 1:
            data.insert(0, "WH1080 ")
            counter = counter - 1
            try:
                valueWeather
            except NameError:
                valueWeather = None
            if valueWeather is None:
                logger.error("value just initialised again")
                valueWeather = {}
            returnDict = insertData(self, data, valueWeather)
        logger.info("Dict: " + str(returnDict))

        logger.info(data + str(type(data)))
        return(data, counter)


def insertData(self, data, valueWeather):

    if "gust:" in data:
        gustValue = (str(data[3]))
        valueWeather.update({'gust': gustValue})

    if "Weather" in data:
        dateValue = (str(data[2]))
        valueWeather.update({'time': dateValue})

    if "speed:" in data:
        speedValue = (str(data[4]))
        valueWeather.update({'speed': speedValue})

    if "string:" in data:
        compassValue = (str(data[3]))
        valueWeather.update({'compass': compassValue})

    if "rainfall:" in data:
        rainfallValue = (str(data[3]))
        valueWeather.update({'rainfall': rainfallValue})

    if "degrees:" in data:
        degreesValue = str(data[3])
        valueWeather.update({'degrees': degreesValue})

    if "Temperature:" in data:
        temperatureValue = str(data[2])
        valueWeather.update({'temperature': temperatureValue})

    return(valueWeather)





