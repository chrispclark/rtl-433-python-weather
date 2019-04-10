from loguru import logger
import json
import Open_db

class CleanData:
    def __init__(self):
        pass

    def massageData(self, body):
        print(body)
        try:
            message = json.loads(body.decode('utf-8').replace("'",'"'))
        except Exception as e:
            print("Error: " + str(e))
            failed = {"Failed": 0, "Failed" : 0}
            return(failed)

        if 'Fine Offset Electronics WH1080/WH3080 Weather Station' in str(message):
            # logger.info("Found: " + str(message))
            rest = Open_db.loadSession(message)
            return(message)
        else:
            # logger.info("Not Found: " + str(body))
            return(message)
