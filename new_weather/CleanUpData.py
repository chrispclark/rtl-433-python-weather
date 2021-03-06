from loguru import logger
import json
import Open_db
# import snoop

class CleanData:
    def __init__(self):
        pass
    
    def massageData(self, body):
        try:
            message : dict = json.loads(body.decode('utf-8').replace("'",'"'))
        except Exception as e:
            failed = {"Failed": 0, "Failed" : 0}
            message['DetectedModelType'] = 'Nothing'
            return(failed)

        if 'Fine Offset Electronics WH1080/WH3080 Weather Station' in str(message):
            # logger.info("Found: " + str(message))
            rest = Open_db.loadSession(message)
            message['DetectedModelType'] = 'WH1080/WH3080'
            return(message)
        else:
            # logger.info("Not Found: " + str(body))
            message['DetectedModelType'] = 'Unknown'
            return(message)
